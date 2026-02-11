import os
from pathlib import Path
from dotenv import load_dotenv

# 🔥 Charger le .env depuis la RACINE du projet
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)


class Config:
    # Clé API Gemini
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # Configuration du modèle
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.1"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2048"))
    
    # Chemins
    VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "data/vector_store")
    DOCUMENTS_PATH = os.getenv("DOCUMENTS_PATH", "data/documents")
    
    # Configuration RAG
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "4"))
    
    @classmethod
    def validate(cls):
        """Valide la configuration"""
        errors = []
        if not cls.GEMINI_API_KEY:
            errors.append("GEMINI_API_KEY est requis dans le fichier .env")
        return errors

# Instance de configuration globale
config = Config()