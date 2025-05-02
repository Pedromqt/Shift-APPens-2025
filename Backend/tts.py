from gtts import gTTS
import pygame
import time
import os

def falar(texto: str):
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
