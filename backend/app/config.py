import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Load API Key from environment
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
    # Default model (Groq's fastest Llama 3.3)
    MODEL_NAME: str = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
    
    # Generation parameters
    MAX_TOKENS: int = 4096
    TEMPERATURE: float = 0.2
    
    # Allowed languages for the UI/API
    ALLOWED_LANGUAGES: list = [
        "python", "javascript", "sql", "typescript", 
        "java", "go", "rust", "csharp", "cpp"
    ]

settings = Settings()