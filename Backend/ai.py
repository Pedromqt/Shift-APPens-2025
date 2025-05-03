import openai
from config import OPENAI_API_KEY, MODEL_NAME

# Define chave da API
openai.api_key = OPENAI_API_KEY

def obter_resposta_da_ia(pergunta: str, lat: float = None, lon: float = None) -> str:
    # Injeta localização se fornecida
    full_prompt = pergunta
    if lat is not None and lon is not None:
        full_prompt += f"\nUsuário está em latitude {lat:.5f}, longitude {lon:.5f}."

    resp = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": full_prompt}
        ],
        max_tokens=150
    )

    return resp['choices'][0]['message']['content'].strip()
