# Shift-APPens-2025
Shift APPens Project - Hackathon 2025 - Coimbra, Portugal

# Objetivo
Desenvolver um assistente inteligente de navegação para pessoas cegas que utiliza comandos auditivos para orientar o utilizador de forma segura até ao seu destino. O sistema combina diversas tecnologias para garantir uma navegação autónoma, eficiente e segura:
Deteção de obstáculos em tempo real com uso de câmaras e modelos de visão computacional (YOLO), capazes de identificar buracos, objetos no caminho, entre outros perigos.
Planeamento de rotas.
Geolocalização contínua com atualizações frequentes via GPS ou IP, para ajustar rotas em tempo real e garantir precisão durante o percurso.
Interação por voz, permitindo que o utilizador indique o destino e receba instruções de forma auditiva, sem necessidade de interação visual ou tátil.
Informação urbana em tempo real, incluindo localização de passadeiras, semáforos, estradas e vias pedonais, com especial atenção a cidades com maior densidade de infraestrutura.

# Tecnologias usadas:
## Frontend
Django
React js
Node.js
JavaScript, CSS          

## Backend
Python
Django
YOLO
OpenCV, Flask, Geopy, SpeechRecognition, TTS, pygame, openAI, torch

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
