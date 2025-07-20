# Will I Be Okay at 60? (MLOps Zoomcamp Final Project)

Retirement Readiness ML Pipeline

An end-to-end MLOps project that predicts whether Malaysians are financially, medically, and psychologically ready for retirement. Designed to reflect real-world production systems built using open-source and free-tier tools.

---

## Project Objectives

- Predict individual retirement readiness (OK / Not OK).
- Architect a reproducible, cloud-ready MLOps pipeline.
- Practice best practices: modular code, experiment tracking, workflow orchestration, CI/CD, and IaC.
- Using AWS Free Tier.

---

## Problem Statement

As more Malaysians face retirement without adequate planning, this ML pipeline serves as a decision-support system.  
It helps assess whether a person is “OK” or “Not OK” for retirement at 60 based on:
- Financial savings
- Health status
- Mental well-being
- Family burden
- Lifestyle

---

## Tech Stack

| Layer                | Tool                                             |
|---------------------|--------------------------------------------------|
| Cloud & Storage     | AWS Free Tier (S3, EC2, IAM)                     |
| Experiment Tracking | MLflow                                           |
| Orchestration       | Prefect                                          |
| Containerization    | Docker                                           |
| Workflow Deployment | EC2 (Dockerized Python App)                      |
| Infrastructure      | Terraform                                        |
| CI/CD               | GitHub Actions                                   |
| Monitoring          | MLflow + (Evidently planned)                     |
| Version Control     | Git + GitHub                                     |
| Notebook / Dev      | JupyterLab                                       |

---

##  Project Structure

```
retirement_project/
├── pipeline/
│   ├── __init__.py                 # Init file for the pipeline module
│   ├── training_pipeline.py        # Main MLflow-tracked training pipeline
│   ├── features.py                 # Feature engineering transformations
│   ├── model.py                    # Model training and persistence logic
│   └── evaluate.py                 # Evaluation metrics and comparison
│
├── Notebook/
│   └── eda_notebook.ipynb          # Exploratory Data Analysis + validation
│
├── Dockerfile                      # Docker image definition for EC2 containerization
├── requirements.txt                # Python dependencies for training + infra
├── .gitignore                      # Ignored files and folders (e.g., logs, .env)
│
├── terraform/                      # Infrastructure-as-Code (IaC)                  
│   └── main.tf                     # AWS EC2, S3, IAM provisioning
│
└── .github/
    └── workflows/
        └── ci.yml                  # GitHub Actions workflow for linting and testing
               

```
---

## MLflow Experiment

- Model: Random Forest Regressor

- Parameters:

n_estimators = 100

max_depth = 10

- Metrics:

MAE (Mean Absolute Error)

R² (Coefficient of Determination)

- Artifacts:

sklearn-model (logged with mlflow.sklearn.log_model())

Tracked run registered as versioned model under name retirement-readiness-model

Launch with:
```bash
mlflow ui
```

## Reproducibility
Clone and run locally:

```
git clone https://github.com/shanurwan/retirement-project.git
cd retirement-project

# Set up virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the training pipeline
python -m pipeline.training_pipeline

```

or Run Docker container:

```
# Build the Docker image
docker build -t retirement-pipeline .

# Run the container
docker run retirement-pipeline

```

## Deployment

- ML pipeline is containerized via Docker.

- Runs on AWS EC2 (Free Tier).

- S3 acts as data lake.

- Training triggered via Prefect workflow.

##  CI/CD

- Linting and formatting (black, flake8)

- Tests run via GitHub Actions

- Pre-commit hooks for clean commits

##  Security
- No credentials hardcoded.

- AWS keys securely configured via ~/.aws/credentials

- .gitignore excludes sensitive files like .env, mlruns/, AWS keys.

## Future Work

Real-time inference API via FastAPI

Weekly auto-retrain pipeline (via Prefect schedules)

## Contact 
Email : wannurshafiqah18@gmail.com
whatsapp : +60108190277
Linkedin : [Wan Shafiqah](www.linkedin.com/in/wan-shafiqah-852636223)
