from prefect import flow, task
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import boto3
import io

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
    print("🧹 Preprocessing data...")
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

    with mlflow.start_run() as run:
        # Train model
        rf = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
        rf.fit(X_train, y_train)

        # Predictions and metrics
        preds = rf.predict(X_val)
        mae = mean_absolute_error(y_val, preds)
        r2 = r2_score(y_val, preds)

        # Log parameters and metrics
        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("max_depth", 10)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2", r2)

        # Log and register model
        mlflow.sklearn.log_model(
            sk_model=rf,
            artifact_path="model",
            registered_model_name="retirement_rf_model"
        )

        print(f"Model registered to MLflow Registry as 'retirement_rf_model'")
        print(f"MAE = {mae:.2f}, R2 = {r2:.2f}")
        print(f" Run ID: {run.info.run_id}")

@flow
def retirement_training_pipeline():
    df = load_data()
    X_train, X_val, y_train, y_val = preprocess(df)
    train_and_log(X_train, X_val, y_train, y_val)

if __name__ == "__main__":
    print("Running training pipeline...")
    retirement_training_pipeline()
