
import os
import logging
import ollama

# ==========================================
# 1. CONFIGURATION
# ==========================================

MODEL_NAME = "llama3.2:3b"

OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://localhost:11434"
)

# Create Ollama client
client = ollama.Client(host=OLLAMA_HOST)


# ==========================================
# 2. LOGGING CONFIGURATION
# ==========================================

logger = logging.getLogger(__name__)


# ==========================================
# 3. CHECK OLLAMA CONNECTION
# ==========================================

def check_ollama_connection():
    """Check Ollama connection and model availability."""

    try:
        response = client.list()

        available_models = [
            model.model for model in response.models
        ]

        if MODEL_NAME not in available_models:
            logger.error("Model not found: %s", MODEL_NAME)
            return False

        logger.info("Ollama connection successful.")
        logger.info("Model available: %s", MODEL_NAME)

        return True

    except Exception:
        logger.exception("Ollama connection failed.")
        return False


# ==========================================
# 4. GENERATE LLM RESPONSE
# ==========================================

def generate_response(prompt):
    """Generate an LLM response with error handling."""

    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    try:
        response = client.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        answer = response.message.content

        if not answer or not answer.strip():
            raise RuntimeError("Ollama returned an empty response.")

        logger.info("LLM response generated successfully.")

        return answer.strip()

    except ollama.ResponseError as error:
        logger.exception("Ollama response error.")

        raise RuntimeError(
            "Ollama could not process the request. "
            "Check the model and prompt."
        ) from error

    except Exception as error:
        logger.exception("LLM generation failed.")

        raise RuntimeError(
            "Unable to generate an AI response. "
            "Check whether Ollama is running."
        ) from error


# ==========================================
# 5. MANUAL CONNECTION TEST
# ==========================================

if __name__ == "__main__":

    print("Ollama Host:", OLLAMA_HOST)
    print("Checking Ollama connection...")

    if check_ollama_connection():

        try:
            answer = generate_response(
                "What is a sales lead?"
            )

            print("\nLLM Response:")
            print(answer)

        except RuntimeError as error:
            print("ERROR:", error)

    else:
        print("Ollama is unavailable or the model is missing.")
