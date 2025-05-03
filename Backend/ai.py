import openai
from config import OPENAI_API_KEY, MODEL_NAME

# Define chave da API
openai.api_key = OPENAI_API_KEY

def obter_resposta_da_ia(pergunta: str, lat: float = None, lon: float = None) -> str:
    # Constrói prompt com localização (se fornecida)
    # Eventualmente metemos as infomracoes do user no prompt inicial
    system = 'Você é um assistente de mobilidade para pessoas com deficiência visual.– Use descrições espaciais claras: “à sua frente, 2 passos”.– Nunca diga “veja isto” ou “observe aquilo”.– Inclua avisos de segurança (“cuidado”, “obstáculo”).– Tom calmo, paciente, encorajador.'
    if lat and lon:
        system += f' Ele está em lat {lat:.5f}, lon {lon:.5f}.'

    resp = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=[
            {'role': 'system', 'content': system},
            {'role': 'user', 'content': pergunta}
        ],
        max_tokens=100
    )

    return resp['choices'][0]['message']['content'].strip()
