import threading
import time
from CamDetection.camDetection import capture
import Queue.createQueue as createQueue
# from Queue.processQueue import alertar
from Voice.voiceDetection import iniciar_assistente

stop_event = threading.Event()

if __name__ == '__main__':
    try:
        # Cria as queues
        queueAlerts, queueNavigation = createQueue.createQueues()

        # Inicia a thread de captura
        capture_thread = threading.Thread(
            target=capture,
            args=(stop_event, queueAlerts),
            
            daemon=True
        )
        capture_thread.start()

        # Inicia a thread de processamento
        #process_thread = threading.Thread(
        #    target=ok,
        #    args=(stop_event, queueAlerts, queueNavigation)
        #)
        #process_thread.start()
        
        voice_assistant = threading.Thread(
            target=iniciar_assistente,
            args=(stop_event, queueNavigation)
        )
        voice_assistant.start()

        # Espera ambas as threads terminarem
        capture_thread.join()
        voice_assistant.join()
        #process_thread.join()

    except KeyboardInterrupt:
        print("\n[INFO] CTRL+C detectado. A encerrar...")
        capture_thread.join()
        voice_assistant.join()
        print("[INFO] Programa terminado com sucesso.")