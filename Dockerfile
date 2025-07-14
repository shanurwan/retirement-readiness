FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Fix Python path so it recognizes /app as root for custom modules
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Run training pipeline
CMD ["python", "-c", "from pipeline.training_pipeline import retirement_training_pipeline; retirement_training_pipeline()"]



