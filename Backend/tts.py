import os
import platform
import tempfile
from gtts import gTTS
import pygame
import time

def falar(texto: str):
    # gera mp3 temporário
    fd, ficheiro = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)
    gTTS(text=texto, lang='pt', tld='pt').save(ficheiro)

    so = platform.system()
    if so == "Windows":
        # abre com o programa padrão (Windows Media Player, Groove, etc.)
        nome = "resposta.mp3"
        tts = gTTS(text=texto, lang='pt', tld='pt')
        tts.save(nome)

        pygame.mixer.init()
        pygame.mixer.music.load(nome)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.music.unload()
        os.remove(nome)
    elif so == "Darwin":
        # macOS
        os.system(f'afplay "{ficheiro}"')
    else:
        # presumimos Linux com mpg123 instalado
        os.system(f'mpg123 "{ficheiro}" >/dev/null 2>&1')

    os.remove(ficheiro)
