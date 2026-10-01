# config.py
import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # Ricerca web
    MAX_RESULTS = 5

    # Completamento: OpenAI (default), richiede OPENAI_API_KEY nel file .env
    LLM_MODEL = "gpt-4o-mini"
    AI_API_URL = "https://api.openai.com/v1/"
    AI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

    # Per usare Ollama locale al posto di OpenAI (nessuna chiave richiesta): commenta il
    # blocco sopra, scommenta questo.
    # LLM_MODEL = "llama3.2"
    # AI_API_URL = "http://localhost:11434/v1"
    # AI_API_KEY = "ollama"  # valore fittizio richiesto dal client OpenAI, ignorato da Ollama
