from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import pandas as pd

# Importar a função de extração de features
import sys
caminho_atual = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(caminho_atual, '..', 'src'))
from preprocessamento import extrair_features

app = Flask(__name__)
CORS(app)

# --- CORREÇÃO AQUI ---
# Carregar o modelo otimizado (0-200) e o scaler
modelo = joblib.load(os.path.join(caminho_atual, 'modelo_coesao_otimizado.pkl'))
scaler = joblib.load(os.path.join(caminho_atual, 'scaler.pkl'))
print("Modelo OTIMIZADO (Coesão) e scaler carregados com sucesso!")

@app.route('/prever', methods=['POST'])
def prever_nota():
    dados = request.get_json()
    
    if 'texto_redacao' not in dados or not dados['texto_redacao'].strip():
        return jsonify({'erro': 'O texto da redação não pode estar vazio!'}), 400
    if 'tema' not in dados or not dados['tema'].strip():
        return jsonify({'erro': 'O tema da redação não pode estar vazio!'}), 400

    texto_redacao = dados['texto_redacao']
    tema = dados['tema']
    
    texto_combinado = tema + " " + texto_redacao
    
    features = extrair_features(texto_combinado)
    features_df = pd.DataFrame([features])
    features_scaled = scaler.transform(features_df)
    nota_prevista = modelo.predict(features_scaled)

    nota_final = round(nota_prevista[0])
    
    # --- CORREÇÃO AQUI ---
    # Trava de segurança para a nota de 0 a 200
    if nota_final < 0:
        nota_final = 0
    elif nota_final > 200:
        nota_final = 200

    # --- CORREÇÃO AQUI ---
    # Retornar a nota de coesão prevista
    return jsonify({
        'nota_prevista_c4': nota_final,
        'analise_detalhada': features
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)