import time
import sys
import os
import threading
from createQueue import alertsQueue, navigationQueue

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tts2 import falar

ultimo_alerta = ""
ultimo_tempo_alerta = 0

def processar_falas():
    global ultimo_alerta, ultimo_tempo_alerta
    while True:
        try:
            # Prioridade: alertas primeiro
            if not alertsQueue.empty():
                texto = alertsQueue.get()
            elif not navigationQueue.empty():
                texto = navigationQueue.get()
            else:
                time.sleep(0.1)
                continue

            tempo_atual = time.time()
            if texto != ultimo_alerta or (tempo_atual - ultimo_tempo_alerta > 5):
                falar(texto)
                ultimo_alerta = texto
                ultimo_tempo_alerta = tempo_atual

        except Exception as e:
            print(f"[ERRO NA THREAD DE FALA] {e}")
            time.sleep(0.5)

# Iniciar a thread
thread_fala = threading.Thread(target=processar_falas, daemon=True)
thread_fala.start()
