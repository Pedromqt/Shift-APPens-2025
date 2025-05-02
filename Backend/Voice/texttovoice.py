
from ai import obter_resposta_da_ia
from Backend.Voice.tts2 import falar


import json
from pathlib import Path
from ai import client, SYSTEM_PROMPT, obter_resposta_da_ia
from tts import falar
from config import MODEL_NAME
# Se quiseres carregar/persistir histórico num ficheiro:
HISTORY_PATH = Path(__file__).resolve().parent.parent / "chat_history.json"

def load_history():
    if HISTORY_PATH.exists():
        return json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
    # inicia com o system prompt
    return [{"role": "system", "content": SYSTEM_PROMPT}]

def save_history(history):
    HISTORY_PATH.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")

def main():
    history = load_history()

    while True:
        pergunta = input("\nO que o utilizador disse? (ou 'sair'): ")
        if pergunta.lower() in ("sair", "exit", "quit"):
            break

        # adiciona mensagem do utilizador
        history.append({"role": "user", "content": pergunta})

        # chama a OpenAI com TODO o histórico
        response = client.chat.completions.create(
            model=MODEL_NAME,        # ou MODEL_NAME
            messages=history,
            max_tokens=150,
        )
        resposta = response.choices[0].message.content.strip()

        # armazena a resposta na história
        history.append({"role": "assistant", "content": resposta})

        # opcional: grava em disco
        save_history(history)

        print("IA:", resposta)
        falar(resposta)

    # no fim podes limpar histórico ou mantê-lo
    print("Sessão terminada.")

if __name__ == "__main__":
    main()
