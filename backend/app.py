from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import pandas as pd

# Para evitar duplicar código, vamos importar a função do nosso script de pré-processamento
import sys
caminho_atual = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(caminho_atual, '..', 'src'))
from preprocessamento import extrair_features #

# --- 1. CONFIGURAÇÃO INICIAL ---
app = Flask(__name__)
CORS(app) # Permite a comunicação com o nosso frontend

# --- 2. CARREGANDO OS MODELOS DE ML ---
# Carrega o modelo otimizado (0-1000) e o scaler
modelo = joblib.load(os.path.join(caminho_atual, 'modelo_nota_final_otimizado.pkl'))
scaler = joblib.load(os.path.join(caminho_atual, 'scaler.pkl'))
print("Modelo OTIMIZADO (Nota Final) e scaler carregados com sucesso!")

# --- 3. ROTA DA API DE ANÁLISE ---
@app.route('/prever', methods=['POST'])
def prever_nota():
    dados = request.get_json()
    
    # Validação dos dados de entrada
    if 'texto_redacao' not in dados or not dados['texto_redacao'].strip():
        return jsonify({'erro': 'O texto da redação não pode estar vazio!'}), 400
    if 'tema' not in dados or not dados['tema'].strip():
        return jsonify({'erro': 'O tema da redação não pode estar vazio!'}), 400

    texto_redacao = dados['texto_redacao']
    tema = dados['tema']
    
    # Combina o tema e a redação, assim como fizemos no treinamento
    texto_combinado = tema + " " + texto_redacao
    
    # 1. Extrair as features do texto combinado
    features = extrair_features(texto_combinado)
    
    # 2. Converter as features para o formato que o scaler espera (um DataFrame)
    features_df = pd.DataFrame([features])
    
    # 3. Usar o scaler para normalizar as features
    features_scaled = scaler.transform(features_df)
    
    # 4. Fazer a predição com os dados normalizados
    nota_prevista = modelo.predict(features_scaled)

    nota_final = round(nota_prevista[0])
    
    # Trava de segurança para a nota de 0 a 1000
    if nota_final < 0:
        nota_final = 0
    elif nota_final > 1000:
        nota_final = 1000

    # Retornar a nota final prevista e a análise detalhada
    return jsonify({
        'nota_final_prevista': nota_final,
        'analise_detalhada': features
    })

# --- 4. EXECUÇÃO ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)