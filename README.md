# Automated Support-Ticket Classifier

## Overview
End-to-end pipeline to classify support tickets into categories:
- **Data ingestion & ETL** with Airflow & DVC  
- **Model training & tracking** with Hugging Face Transformers & MLflow  
- **Serving** via FastAPI in Docker + Kubernetes (canary rollout)  
- **CI/CD** with Jenkins  
- **Monitoring & alerting** with Prometheus & Grafana  

## Setup (Windows)
1. Activate your venv:
   ```powershell
   .\venv\Scripts\Activate.ps1
