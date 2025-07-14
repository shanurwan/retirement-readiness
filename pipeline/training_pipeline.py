from prefect import flow, task
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import boto3
import io
from prefect import task

@task
def load_data():
    s3 = boto3.client("s3")
    bucket = "retirement-readiness-data"
    key = "data/retirement_dataset.csv"

    obj = s3.get_object(Bucket=bucket, Key=key)
    df = pd.read_csv(io.BytesIO(obj["Body"].read()))
    
    return df

@task
def preprocess(df):
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
    mlflow.set_experiment("retirement-prediction")

    with mlflow.start_run():
        rf = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
        rf.fit(X_train, y_train)

        preds = rf.predict(X_val)
        mae = mean_absolute_error(y_val, preds)
        r2 = r2_score(y_val, preds)

        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("max_depth", 10)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2", r2)

        mlflow.sklearn.log_model(rf, "model")

        print(f"Logged to MLflow: MAE={mae:.2f}, R2={r2:.2f}")

@flow
def retirement_training_pipeline():
    df = load_data()
    X_train, X_val, y_train, y_val = preprocess(df)
    train_and_log(X_train, X_val, y_train, y_val)

# To run:
# retirement_training_pipeline()

