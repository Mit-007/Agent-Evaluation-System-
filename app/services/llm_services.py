from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import GOOGLE_API_KEY, LLM_MODEL_NAME,TEMPERATURE
from app.core.logger import logger

def get_llm():
    try:
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is missing. Please set it in your .env file.")

        llm = ChatGoogleGenerativeAI(
            model=LLM_MODEL_NAME,
            temperature=float(TEMPERATURE)
        )

        return llm
    
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {e}")
        return  None