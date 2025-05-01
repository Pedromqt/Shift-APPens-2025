import speech_recognition as sr
import requests
import json
from geopy.geocoders import Nominatim
import time
import threading
import openrouteservice  # Biblioteca para interação com OpenRouteService

# Configuração da API do OpenRouteService
ORS_API_KEY = '5b3ce3597851110001cf6248be4f316345c74356a821df1601dbc6cd'  # Substitua com sua chave da API do OpenRouteService
client = openrouteservice.Client(key=ORS_API_KEY)  # Cliente para interagir com OpenRouteService

# Controles para threads e fluxo do programa
execucao_ativa = False
thread_localizacao = None

# NOVA FUNÇÃO: Obter coordenadas por IP
def coordenadas_por_ip():
    try:
        response = requests.get("http://ip-api.com/json/")
        if response.status_code == 200:
            dados = response.json()
            lat = dados.get("lat")
            lon = dados.get("lon")
            print(f"📍 Coordenadas por IP: Latitude: {lat}, Longitude: {lon}")  # Verifique se as coordenadas estão corretas
            return lat, lon
        else:
            print("❗ Erro ao obter localização por IP:", response.status_code)
            return None, None
    except Exception as e:
        print("❗ Erro ao obter localização por IP:", str(e))
        return None, None

# Morada com OSM
def morada_detalhada_osm(lat, lon):
    geolocator = Nominatim(user_agent="guiar-assistente")
    time.sleep(1)
    localizacao = geolocator.reverse((lat, lon), language='pt')
    return localizacao.address if localizacao else "Morada não encontrada"

# Junta tudo
def obter_localizacao():
    lat, lon = coordenadas_por_ip()  # ← AGORA usa IP em vez de Selenium
    if lat and lon:
        return morada_detalhada_osm(lat, lon), lat, lon
    return "Localização não encontrada", None, None

# Obter direções de OpenRouteService
def obter_direcoes(lat_inicial, lon_inicial, lat_destino, lon_destino):
    # Coleta das coordenadas para criar um caminho
    origem = (lon_inicial, lat_inicial)  # Formato do OpenRouteService: (longitude, latitude)
    destino = (lon_destino, lat_destino)
    
    # Consulta de direções
    try:
        rotas = client.directions(
            coordinates=[origem, destino],
            profile='driving-car',  # Ou 'foot-walking' para a pé
            format='geojson'
        )
        
        # Extrair a sequência de instruções
        instrucoes = []
        for step in rotas['features'][0]['properties']['segments'][0]['steps']:
            instrucoes.append(step['instruction'])
        
        return "\n".join(instrucoes)  # Retorna as instruções como uma string
    except Exception as e:
        return f"❗ Erro ao obter direções: {str(e)}"

# Comando de voz
def interpretar_comando(texto):
    global execucao_ativa, thread_localizacao

    texto = texto.lower()
    if "olá guiar" in texto:
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
                print(f"📍 Localização atual: {localizacao_texto}")

                if "polo 2" in comando_utilizador:  # Caso o destino seja Polo 2, Coimbra
                    destino_texto = "Polo 2, Coimbra"
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
                thread_localizacao.start()

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

# Atualização contínua da localização
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

# Escuta de voz
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

# Início
if __name__ == "__main__":
    print("🚀 Iniciando o assistente Guiar com OpenStreetMap...")
    try:
        ouvir_microfone()
    except KeyboardInterrupt:
        print("\n👋 Encerrando o assistente Guiar...")
        execucao_ativa = False
        if thread_localizacao and thread_localizacao.is_alive():
            thread_localizacao.join(2)
