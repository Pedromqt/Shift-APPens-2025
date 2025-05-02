from gtts import gTTS
import os

def falar(texto: str):
    nome = 'resposta.mp3'
    tts = gTTS(text=texto, lang='pt', tld='pt')
    tts.save(nome)
    os.system(f"mpg123 {nome} >/dev/null 2>&1")
    os.remove(nome)