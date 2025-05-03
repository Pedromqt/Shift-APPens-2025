# Shift-APPens-2025
Shift APPens Project - Hackathon 2025 - Coimbra, Portugal

Sistema que guia o cego para locais especificos. Usa algoritmos para detetar os melhores caminhos com base na distância, evitando escadas, obstáculos perigosos, escadas rolantes e etc.
Podemos usar camara para detetar buracos em tempo real ao longo do caminho.
Podemos usar um bd para marcar locais especificos como casa, casa da sogra, tasca do joao pinheiro e piscina municipal.
OpenStreetMap tem acesso em tempo real a tudo, multibancos, estradas, semáforos, vias pedonais para pessoas, etc. Em localidades maiores tem acesso a passadeiras.

# Como executar o software:
Ter câmara, microfone e áudio ligados.
Entrar no .env e colocar uma chave de openai.
cd .\Backend\
pip install -r ./requirements.txt
python main.py

### Câmara
A câmara deteta praticamente tudo especialmente veículos, buracos, passadeiras, semáforos (deteta se a luz está verde ou vermelha para a pessoa poder passar) e avisa através de áudio se a luz está verde ou vermelha.

### Microfone
Podemos pedir para ir para localizações e através de gps e áudio é dito como ir para essa localização.
