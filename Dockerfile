# Dockerfile

FROM python:3.10-slim

WORKDIR /app

# 1. Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copy the exported MLflow model
COPY model ./model

# 3. Copy the FastAPI serving code
COPY src/serving ./src/serving

# 4. Expose port and launch
EXPOSE 8080
CMD ["uvicorn", "src.serving.app:app", "--host", "0.0.0.0", "--port", "8080"]
