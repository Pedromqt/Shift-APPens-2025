# backend/ai.py

import os
import json
from pathlib import Path
from openai import OpenAI
from config import OPENAI_API_KEY, MODEL_NAME

# 1) Define o root do teu projeto (duas pastas acima deste ficheiro)
root = Path(__file__).resolve().parent.parent

# 2) Carrega o perfil do utilizador (se existir)
profile_path = root / 'perfilteste.json'
if profile_path.exists():
    with open(profile_path, 'r', encoding='utf-8') as f:
        profile = json.load(f)
else:
    # perfil por defeito, caso não tenhas criado o ficheiro
    profile = {
    "nome": "António",
    "idade": 35,
    "genero": "masculino",
    "morada": "Coimbra, Portugal, Rua Pêro Vaz de Caminha, 100",
    "velocidade_passa": "média",
    "idioma": "pt-pt",
    "unidades": "metros",
    "tem_horario_visita": "nao",
    "observacoes": "Gosta que o tratem pelo nome, Senhor António."
}


# 3) Inicializa o cliente OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# 4) Define o system prompt specialised
SYSTEM_PROMPT = f"""
Você é um assistente de mobilidade para pessoas com deficiência visual.
– Use descrições espaciais claras: “à sua frente, 2 metros, um degrau”.
– Não diga “veja isto” ou “observe aquilo”.
– Inclua avisos de segurança (“cuidado”, “obstáculo”).
– Adote tom calmo, paciente, encorajador.
– Pergunte sempre se precisa de repetição ou mais detalhes.
-Quando abordado sobre a localização atual do utilizador nao diga lugares vaguos mas sim mais detalhadamente pois o utilizador tem problemas de visão-

Usuário: {profile['nome']}. 
Tem {profile['idade']} anos.
O usuário mora exatamente em {profile['morada']}.
Prefere unidades em {profile['unidades']}.  
Velocidade de caminhada: {profile['velocidade_passa']}.
Tem em conta as seguintes observações: {profile['observacoes']}.
""".strip()

def obter_resposta_da_ia(pergunta: str, lat: float = None, lon: float = None) -> str:
    # Injeta localização se fornecida
    full_prompt = pergunta
    if lat is not None and lon is not None:
        full_prompt += f"\nUsuário está em latitude {lat:.5f}, longitude {lon:.5f}."

    resp = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": full_prompt}
        ],
        max_tokens=150
    )

    return resp.choices[0].message.content.strip()
