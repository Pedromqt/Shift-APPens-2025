import json, os
from dotenv import load_dotenv
from pathlib import Path




root = Path(__file__).resolve().parent.parent
env_path = root / '.env'

load_dotenv(dotenv_path=env_path, override=True)



OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME     = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

print("🔑 OPENAI_API_KEY:", OPENAI_API_KEY)
print("🤖 MODEL_NAME:    ", MODEL_NAME)

if not OPENAI_API_KEY or not OPENAI_API_KEY.startswith("sk-"):
    raise RuntimeError("❌ OPENAI_API_KEY inválida ou não encontrada no .env")

