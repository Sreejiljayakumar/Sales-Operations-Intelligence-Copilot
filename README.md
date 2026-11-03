# Sales Operations Intelligence Copilot

An AI-powered sales intelligence platform that combines Machine Learning, Retrieval-Augmented Generation (RAG), Large Language Models (LLMs), and workflow automation to support smarter sales operations.

## Overview

The Sales Operations Intelligence Copilot helps businesses analyse sales leads, estimate conversion probability, retrieve company information, and support sales teams with AI-assisted recommendations.

The project combines predictive analytics with a knowledge-based AI assistant and an interactive dashboard.

## Key Features

- **Lead Conversion Prediction:** Predicts the probability of a sales lead converting using a trained machine learning pipeline.
- **Sales Intelligence Dashboard:** Displays lead analytics, KPIs, visualisations, filters, and prediction results.
- **AI Knowledge Assistant:** Answers company-related questions using Retrieval-Augmented Generation.
- **Hybrid Retrieval:** Combines semantic vector search and BM25 keyword retrieval.
- **LLM Integration:** Uses a locally hosted Llama 3.2 model through Ollama.
- **REST API:** Provides endpoints for health checks, predictions, and AI-assisted question answering.
- **Workflow Automation:** Integrates with n8n for lead-processing workflows, Telegram notifications, and human approval.
- **Docker Deployment:** Runs the API, dashboard, and Ollama services using Docker Compose.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Analysis | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Data Visualisation | Matplotlib, Seaborn, Plotly |
| API | FastAPI, Uvicorn |
| Dashboard | Streamlit |
| LLM | Ollama, Llama 3.2 |
| RAG | LangChain, ChromaDB, BM25 |
| Embeddings | Sentence Transformers |
| Automation | n8n, Telegram |
| Deployment | Docker, Docker Compose |
| Development | VS Code, Jupyter Notebook |

## Machine Learning Pipeline

The project uses a synthetic sales leads dataset containing 5,000 records and 11 columns.

The prediction target is `converted`.

### Input Features

**Numerical features**
- Budget
- Website visits
- Emails opened
- Calls made
- Previous interactions
- Response time in hours

**Categorical features**
- Lead source
- Industry
- Company size

### ML Workflow

1. Dataset loading and inspection
2. Data quality checks
3. Exploratory data analysis
4. Feature selection
5. Numerical and categorical preprocessing
6. Train, validation, and test splitting
7. Model training and comparison
8. Hyperparameter tuning and threshold evaluation
9. Model evaluation
10. Prediction pipeline development

The preprocessing pipeline uses median imputation and standardisation for numerical features, and most-frequent imputation and one-hot encoding for categorical features.

## RAG and AI Knowledge Assistant

The knowledge assistant retrieves information from company documents before generating answers.

### Components

- Document loading and processing
- Text chunking
- Sentence Transformer embeddings
- ChromaDB vector storage
- BM25 keyword retrieval
- Hybrid retrieval
- LLM-based response generation

The assistant uses company knowledge documents covering company information, products and services, and sales policies.

## Application Architecture

- **Streamlit:** User interface and sales analytics dashboard.
- **FastAPI:** Backend API for predictions and question answering.
- **Machine Learning:** Lead conversion prediction pipeline.
- **RAG:** Company knowledge retrieval and answer generation.
- **Ollama:** Local LLM inference.
- **ChromaDB:** Persistent vector storage.
- **n8n:** Workflow automation and human approval.

## API Endpoints

| Endpoint | Purpose |
|---|---|
| `GET /` | API information |
| `GET /health` | Health check |
| `POST /predict` | Lead conversion prediction |
| `POST /ask` | AI knowledge assistant |

Interactive API documentation is available at `/docs` when the API is running.

## Project Structure

```text
Sales-Operations-Intelligence-Copilot/
│
├── configs/
├── data/
│   ├── documents/
│   ├── raw/
│   └── vector_db/
│
├── docs/
├── logs/
├── models/
├── notebooks/
├── scripts/
│
├── src/
│   ├── api/
│   ├── automation/
│   ├── dashboard/
│   ├── data/
│   ├── features/
│   ├── llm/
│   ├── ml/
│   ├── rag/
│   └── utils/
│
├── tests/
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yaml
└── requirements.txt
```

## Installation and Setup

### Prerequisites

- Python 3.13+
- Docker Desktop
- Git
- Ollama

### Clone the repository

```bash
git clone https://github.com/Sreejiljayakumar/Sales-Operations-Intelligence-Copilot.git

cd Sales-Operations-Intelligence-Copilot
```

### Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run with Docker Compose

```bash
docker compose -f docker-compose.yaml up -d --build
```

### Access the local services

| Service | URL |
|---|---|
| Streamlit Dashboard | http://localhost:8501 |
| FastAPI | http://localhost:8000 |
| API Documentation | http://localhost:8000/docs |
| API Health | http://localhost:8000/health |
| n8n | http://localhost:5678 |

The n8n service is managed separately from the project's Docker Compose services.

## Testing

The project includes API integration tests for:
- API health checks
- ML prediction
- RAG question answering

Run tests using:

```bash
pytest -v
```

Ensure the required API services are running before executing integration tests.

## Important Limitations

- The sales dataset is synthetic and does not represent verified real-world business performance.
- Model predictions are estimates, not guarantees of customer conversion.
- RAG responses depend on the available company documents and retrieval quality.
- Human approval is required for sensitive business decisions, including discounts and customer commitments.
- The current deployment is designed for local development using Docker Compose, not a production cloud environment.

## Future Improvements

- Real CRM integration
- Larger real-world sales datasets
- Improved model evaluation and calibration
- Advanced lead scoring
- Role-based access control
- Production deployment
- Enhanced RAG evaluation and monitoring
- Expanded workflow automation

## Project Purpose

This project demonstrates how Machine Learning, Generative AI, RAG, APIs, dashboards, and workflow automation can work together to support data-driven sales operations.
