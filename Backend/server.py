from flask import Flask, request, jsonify
from ai import obter_resposta_da_ia
from tts import falar

app = Flask(__name__)

@app.route('/assist', methods=['POST'])
def assist():
    data = request.json or {}
    pergunta = data.get('pergunta', '')
    lat = data.get('lat')
    lon = data.get('lon')

    resposta = obter_resposta_da_ia(pergunta, lat, lon)
    falar(resposta)
    return jsonify(resposta=resposta)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)