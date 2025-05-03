import os
import platform
import tempfile
from gtts import gTTS
import time
import threading
import keyboard  # Usaremos o módulo keyboard para capturar a tecla 'p'
import pygame  # Vamos usar pygame para o controle do áudio no Windows

# Variável global para controlar se a fala deve ser interrompida
falar_interrompido = False
pygame.mixer.init()  # Inicializa o mixer do pygame para controlar o áudio

def interromper_falar():
    global falar_interrompido
    falar_interrompido = True
    pygame.mixer.music.stop()  # Interrompe imediatamente o áudio

def falar(texto: str):
    global falar_interrompido
    falar_interrompido = False  # Resetando a variável de interrupção

    # Gera mp3 temporário
    fd, ficheiro = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)
    gTTS(text=texto, lang='pt', tld='pt').save(ficheiro)

    so = platform.system()
    if so == "Windows":
        # Abre com o pygame para permitir controle total sobre o áudio
        nome = "resposta.mp3"
        tts = gTTS(text=texto, lang='pt', tld='pt')
        tts.save(nome)

        pygame.mixer.music.load(nome)
        pygame.mixer.music.play()

        # Enquanto o áudio está tocando, verifica se a tecla 'p' foi pressionada
        while pygame.mixer.music.get_busy() and not falar_interrompido:
            time.sleep(0.1)
            if keyboard.is_pressed('p'):  # Verifica se a tecla 'p' foi pressionada
                interromper_falar()  # Interrompe o áudio
                print("🛑 Fala interrompida pelo usuário.")
                break

        # Espera um pouco para garantir que o áudio foi completamente interrompido
        pygame.mixer.music.stop()  # Garante que o áudio seja completamente interrompido
        pygame.mixer.music.unload()  # Descarrega o áudio da memória

        try:
            os.remove(nome)  # Remove o arquivo de áudio
            print("✅ Arquivo de áudio removido com sucesso.")
        except PermissionError:
            print("❗ Erro ao tentar remover o arquivo. O arquivo ainda está sendo usado por outro processo.")
    
    elif so == "Darwin":
        # macOS
        os.system(f'afplay "{ficheiro}"')
    else:
        # Linux com mpg123 instalado
        os.system(f'mpg123 "{ficheiro}" >/dev/null 2>&1')

    os.remove(ficheiro)

# Função para escutar o evento de pressionamento de tecla
def escutar_teclas():
    while True:
        if keyboard.is_pressed('p'):  # Se a tecla 'p' for pressionada
            interromper_falar()
            print("🛑 Fala interrompida pelo usuário.")
            time.sleep(0.1)  # Previne que a interrupção aconteça múltiplas vezes de forma rápida

# Inicia a escuta das teclas em uma thread separada
t = threading.Thread(target=escutar_teclas)
t.daemon = True
t.start()
