from prefect import flow, task
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.feature_extraction import DictVectorizer
import boto3
import io
import os
import pickle


@task
def load_data():
    print(" Loading data from S3...")
    s3 = boto3.client("s3")
    bucket = "retirement-readiness-data"
    key = "data/retirement_dataset.csv"

    obj = s3.get_object(Bucket=bucket, Key=key)
    df = pd.read_csv(io.BytesIO(obj["Body"].read()))

    print(f"Loaded {df.shape[0]} rows.")
    return df

@task
def preprocess(df):
    print(" Preprocessing data...")
    features = [
        'age', 'monthly_income', 'epf_balance', 'debt_amount',
        'household_size', 'medical_expense_monthly', 'mental_stress_level',
        'has_chronic_disease'
    ]
    X = df[features]
    y = df['retirement_readiness_score']
    return train_test_split(X, y, test_size=0.2, random_state=42)

@task
def train_and_log(X_train, X_val, y_train, y_val):
    print("Starting MLflow experiment...")
    mlflow.set_experiment("retirement-prediction")

    # Convert to dictionaries
    train_dicts = X_train.to_dict(orient="records")
    val_dicts = X_val.to_dict(orient="records")

    # Vectorize
    dv = DictVectorizer(sparse=False)
    X_train_vectorized = dv.fit_transform(train_dicts)
    X_val_vectorized = dv.transform(val_dicts)

    with mlflow.start_run() as run:
        rf = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
        rf.fit(X_train_vectorized, y_train)

        # Save the preprocessor (feature list in this case)
        dv = X_train.columns.tolist()

        os.makedirs("models", exist_ok=True)
        with open("models/dv.pkl", "wb") as f_out:
        pickle.dump(dv, f_out)


        preds = rf.predict(X_val_vectorized)
        mae = mean_absolute_error(y_val, preds)
        r2 = r2_score(y_val, preds)

        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("max_depth", 10)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2", r2)

        mlflow.sklearn.log_model(
            sk_model=rf,
            artifact_path="model",
            registered_model_name="retirement_rf_model"
        )

        # Save DictVectorizer locally
        os.makedirs("models", exist_ok=True)
        with open("models/dv.pkl", "wb") as f_out:
            pickle.dump(dv, f_out)

        print(f"Model and DictVectorizer saved. Run ID: {run.info.run_id}")


@flow
def retirement_training_pipeline():
    df = load_data()
    X_train, X_val, y_train, y_val = preprocess(df)
    train_and_log(X_train, X_val, y_train, y_val)

if __name__ == "__main__":
    print("Running training pipeline...")
    retirement_training_pipeline()
