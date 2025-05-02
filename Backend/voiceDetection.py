import speech_recognition as sr
import requests
import json
from geopy.geocoders import Nominatim
import time
import threading
import openrouteservice
from flask import Flask, request
from flask_cors import CORS

# Configuração da API do OpenRouteService
ORS_API_KEY = '5b3ce3597851110001cf6248be4f316345c74356a821df1601dbc6cd'
client = openrouteservice.Client(key=ORS_API_KEY)

# Flask
app = Flask(__name__)
CORS(app)  # ✅ CORS ativado corretamente logo após a criação do app

localizacao_atual = {'lat': None, 'lon': None}

# Estado global
execucao_ativa = False
thread_localizacao = None

# Endpoint para receber localização do telemóvel
@app.route('/localizacao', methods=['POST'])
def receber_localizacao():
    dados = request.json
    localizacao_atual['lat'] = dados.get('latitude')
    localizacao_atual['lon'] = dados.get('longitude')
    return 'Localização recebida com sucesso.', 200

# Obter morada
def morada_detalhada_osm(lat, lon):
    geolocator = Nominatim(user_agent="guiar-assistente")
    time.sleep(1)
    localizacao = geolocator.reverse((lat, lon), language='pt')
    return localizacao.address if localizacao else "Morada não encontrada"

# Obter localização
def obter_localizacao():
    if localizacao_atual['lat'] and localizacao_atual['lon']:
        lat = localizacao_atual['lat']
        lon = localizacao_atual['lon']
        return morada_detalhada_osm(lat, lon), lat, lon
    return "Localização não recebida do telemóvel ainda.", None, None

# Obter direções
def obter_direcoes(lat_inicial, lon_inicial, lat_destino, lon_destino):
    origem = (lon_inicial, lat_inicial)
    destino = (lon_destino, lat_destino)
    try:
        rotas = client.directions(
            coordinates=[origem, destino],
            profile='driving-car',
            format='geojson'
        )
        instrucoes = []
        for step in rotas['features'][0]['properties']['segments'][0]['steps']:
            instrucoes.append(step['instruction'])
        return "\n".join(instrucoes)
    except Exception as e:
        return f"❗ Erro ao obter direções: {str(e)}"

# Comando de voz
def interpretar_comando(texto):
    global execucao_ativa, thread_localizacao
    texto = texto.lower()
    if "olá" in texto:
        print("🟢 Dispositivo ligado!")
        r2 = sr.Recognizer()
        while True:
            with sr.Microphone() as source:
                print("🎤 À espera de comandos...")
                audio = r2.listen(source)
            try:
                comando_utilizador = r2.recognize_google(audio, language='pt-PT')
                print("🗣️ Comando:", comando_utilizador)
                localizacao_texto, lat, lon = obter_localizacao()
                partes = comando_utilizador.split("o")
                comando_utilizador = partes[1]
                if comando_utilizador:
                    destino_texto = comando_utilizador
                    geolocator = Nominatim(user_agent="guiar-assistente")
                    destino_location = geolocator.geocode(destino_texto)
                    if destino_location:
                        lat_destino = destino_location.latitude
                        lon_destino = destino_location.longitude
                        direcoes = obter_direcoes(lat, lon, lat_destino, lon_destino)
                        print("\n🤖 Direções para o Polo 2, Coimbra:")
                        print(direcoes)
                execucao_ativa = True
                thread_localizacao = threading.Thread(target=atualizar_localizacao_continua, args=(comando_utilizador,))
                thread_localizacao.daemon = True
                #thread_localizacao.start()
                print("\n🛑 Para parar as direções, diga 'para guiar' no próximo prompt")
            except sr.UnknownValueError:
                print("❗ Não percebi o comando.")
            except sr.RequestError:
                print("❗ Erro ao aceder ao serviço de reconhecimento.")
    elif "para guiar" in texto or "parar guiar" in texto:
        execucao_ativa = False
        if thread_localizacao and thread_localizacao.is_alive():
            print("🛑 Parando navegação...")
            time.sleep(1.5)
            print("✅ Navegação finalizada!")
    else:
        print("Comando de ativação não reconhecido.")

# Atualização contínua
def atualizar_localizacao_continua(destino):
    global execucao_ativa
    print("🔄 Iniciando atualizações de localização...")
    contador = 1
    while execucao_ativa:
        localizacao, lat, lon = obter_localizacao()
        mensagem = f"ATUALIZAÇÃO: Minha posição atual é {localizacao}. Coordenadas: {lat}, {lon}. Continue me guiando para o destino."
        print(f"\n📍 Atualização #{contador}: {localizacao}")
        print(mensagem)
        contador += 1
        time.sleep(10)
        if contador > 10:
            print("\n🏁 Você chegou ao seu destino!")
            execucao_ativa = False
            break

# Escutar microfone
def ouvir_microfone():
    r = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            if execucao_ativa:
                print("🎤 Diz 'Para Guiar' para encerrar a navegação...")
            else:
                print("🎤 Diz 'Olá Guiar' para começar...")
            audio = r.listen(source)
        try:
            comando = r.recognize_google(audio, language='pt-PT')
            print("🗣️ Disseste:", comando)
            interpretar_comando(comando)
        except sr.UnknownValueError:
            print("❗ Não percebi.")
        except sr.RequestError:
            print("❗ Erro ao aceder ao serviço de reconhecimento.")

# Main
if __name__ == "__main__":
    print("🚀 Iniciando o assistente Guiar com OpenStreetMap...")

    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000))
    flask_thread.daemon = True
    flask_thread.start()

    print(localizacao_atual['lat'])
    print(localizacao_atual['lon'])
    print(obter_localizacao())

    try:
        ouvir_microfone()
    except KeyboardInterrupt:
        print("\n👋 Encerrando o assistente Guiar...")
        execucao_ativa = False
        if thread_localizacao and thread_localizacao.is_alive():
            thread_localizacao.join(2)
