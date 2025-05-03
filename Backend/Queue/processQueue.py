import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Voice.tts2 import falar

def processar_falas(stop_event, alertsQueue, navigationQueue):
    ultimo_alerta = ""
    ultimo_tempo_alerta = 0

    while not stop_event.is_set():
        texto = None

        if not alertsQueue.empty():
            texto = alertsQueue.get()
        elif not navigationQueue.empty():
            texto = navigationQueue.get()

        if texto:
            tempo_atual = time.time()
            if texto != ultimo_alerta or (tempo_atual - ultimo_tempo_alerta > 5):
                falar(texto)
                ultimo_alerta = texto
                ultimo_tempo_alerta = tempo_atual
        else:
            time.sleep(0.5)
