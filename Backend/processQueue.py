#import as queues que ja foram criadas e criar uma thread para tratar da queue. A queue dos alerts tem prioridade, a da navegação tem que ir dizendo consoante a loc
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tts import falar

def alertar(texto):
    global ultimo_alerta, ultimo_tempo_alerta
    tempo_atual = time.time()
    if texto != ultimo_alerta or (tempo_atual - ultimo_tempo_alerta > 5):
        falar(texto)
        ultimo_alerta = texto
        ultimo_tempo_alerta = tempo_atual