import os
from dotenv import load_dotenv

# Carrega variáveis de .env
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MODEL_NAME = os.getenv('MODEL_NAME', 'gpt-4o')