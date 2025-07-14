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

retirement_project/
├── pipeline/
│ ├── init.py
│ ├── training_pipeline.py # MLflow-tracked training logic
│ ├── features.py # Feature engineering
│ ├── model.py # Model training + saving
│ └── evaluate.py # Metrics
│
├── Notebook/
│ └── eda_notebook.ipynb # EDA + exploration
│
├── Dockerfile # Build image for EC2 container
├── requirements.txt # All Python dependencies
├── .gitignore
├── terraform/ # Infrastructure provisioning
│ ├── main.tf # EC2, IAM, S3 setup
│ └── variables.tf
│
└── .github/
└── workflows/
└── ci.yml # Lint + test pipeline


---

## MLflow Experiment

Tracked:
- Model: Logistic Regression
- Parameters: scaling, regularization
- Metrics: accuracy, recall, F1, custom retirement risk score
- Artifacts: model.pkl, confusion matrix, metrics.json

Launch with:
```bash
mlflow ui
```

## Reproducibility
Clone and run locally:

```
git clone https://github.com/shanurwan/retirement-project.git
cd retirement_project

# Set up environment
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Run pipeline locally
python -m pipeline.training_pipeline
git clone https://github.com/shanurwan/retirement-project.git
cd retirement_project

```

or Run Docker container:

```
docker build -t retirement-pipeline .
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
