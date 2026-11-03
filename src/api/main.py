
import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.ml.predict import load_model, predict_lead
from src.rag.rag_assistant import ask_company_assistant


# ==========================================
# 1. LOGGING CONFIGURATION
# ==========================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)


# ==========================================
# 2. CREATE FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="Sales & Operations Intelligence Copilot",
    description="AI-powered Sales and Operations Backend API",
    version="1.0.0"
)


# ==========================================
# 3. REQUEST VALIDATION SCHEMAS
# ==========================================

class LeadRequest(BaseModel):

    lead_source: str
    industry: str
    company_size: str

    budget: float = Field(ge=0)
    website_visits: int = Field(ge=0)
    emails_opened: int = Field(ge=0)
    calls_made: int = Field(ge=0)
    previous_interactions: int = Field(ge=0)
    response_time_hours: float = Field(ge=0)


class QuestionRequest(BaseModel):

    question: str = Field(
        min_length=3,
        max_length=500
    )


# ==========================================
# 4. LOAD ML MODEL
# ==========================================

try:
    ml_artifact = load_model()
    logger.info("ML model loaded successfully.")

except Exception:
    ml_artifact = None
    logger.exception("ML model loading failed.")


# ==========================================
# 5. ROOT ENDPOINT
# ==========================================

@app.get("/")
def home():

    return {
        "message": "Welcome to Sales & Operations Intelligence Copilot",
        "status": "Backend is running"
    }


# ==========================================
# 6. HEALTH CHECK ENDPOINT
# ==========================================

@app.get("/health")
def health_check():

    model_loaded = ml_artifact is not None

    return {
        "status": "healthy" if model_loaded else "degraded",
        "application": "Sales & Operations Intelligence Copilot",
        "version": "1.0.0",
        "ml_model_loaded": model_loaded
    }


# ==========================================
# 7. ML LEAD PREDICTION API
# ==========================================

@app.post("/predict")
def predict_lead_api(lead: LeadRequest):

    if ml_artifact is None:

        logger.error(
            "Prediction requested but ML model is unavailable."
        )

        raise HTTPException(
            status_code=503,
            detail="Prediction service is temporarily unavailable."
        )

    try:

        lead_data = lead.model_dump()

        result = predict_lead(
            lead_data=lead_data,
            artifact=ml_artifact
        )

        logger.info("Lead prediction completed successfully.")

        return result

    except HTTPException:
        raise

    except Exception:

        logger.exception("Lead prediction failed.")

        raise HTTPException(
            status_code=500,
            detail="An internal error occurred during lead prediction."
        )


# ==========================================
# 8. COMPANY KNOWLEDGE ASSISTANT API
# ==========================================

@app.post("/ask")
def ask_company_api(request: QuestionRequest):

    try:

        result = ask_company_assistant(
            request.question
        )

        logger.info("RAG assistant request completed successfully.")

        return result

    except HTTPException:
        raise

    except Exception:

        logger.exception("AI assistant request failed.")

        raise HTTPException(
            status_code=503,
            detail="AI assistant is temporarily unavailable. Please try again."
        )


