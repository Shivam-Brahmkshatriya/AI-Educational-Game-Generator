import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = BASE_DIR / "output" / "games"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DB_DIR = BASE_DIR / "output" / "db"
DB_DIR.mkdir(parents=True, exist_ok=True)
SQLITE_DB_PATH = DB_DIR / "langgraph_state.db"

# Local Ollama Settings
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma4:latest")

# FastAPI Settings
PORT = 8000
HOST = "0.0.0.0"
