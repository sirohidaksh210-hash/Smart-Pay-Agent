import os
import httpx
from dotenv import load_dotenv
from pathlib import Path

env_file = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_file)
API_KEY = os.getenv("GEMINI_API_KEY")

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
try:
    r = httpx.get(url, timeout=10.0)
    models = [m["name"].replace("models/", "") for m in r.json().get("models", []) if "generateContent" in m.get("supportedGenerationMethods", [])]
    print("AVAILABLE_MODELS:", models)
except Exception as e:
    print("ERROR:", e)
