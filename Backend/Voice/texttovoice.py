
from ai import obter_resposta_da_ia
from Backend.Voice.tts2 import falar

if __name__ == '__main__':
    pergunta = input('O que o utilizador disse? ')
    resposta = obter_resposta_da_ia(pergunta)
    print('Resposta da IA:', resposta)
    print("flanfa")
    falar(resposta)
    print("flanfsa")