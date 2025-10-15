# Ferramentas do Flask para criar o servidor
from flask import Flask, request, jsonify
from flask_cors import CORS
# Ferramenta para carregar nosso modelo salvo
import joblib
import os

# --- 1. CONFIGURAÇÃO INICIAL ---

# Cria a aplicação Flask (nosso servidor)
app = Flask(__name__)
# Permite que nosso frontend se comunique com o backend
CORS(app)

# --- 2. CARREGANDO OS MODELOS ---

caminho_atual = os.path.dirname(os.path.abspath(__file__))
caminho_modelo = os.path.join(caminho_atual, 'modelo_coesao.pkl')
caminho_vetorizador = os.path.join(caminho_atual, 'vetorizador.pkl')

print("Carregando modelo e vetorizador...")
modelo = joblib.load(caminho_modelo)
vetorizador = joblib.load(caminho_vetorizador)
print("Modelos carregados com sucesso!")

# --- 3. DEFININDO A ROTA DA API ---
@app.route('/prever', methods=['POST'])
def prever_nota():
    dados = request.get_json()
    if 'texto_redacao' not in dados:
        return jsonify({'erro': 'Nenhum texto de redação foi fornecido!'}), 400

    texto = dados['texto_redacao']
    
    texto_para_vetorizar = [texto]
    vetor_texto = vetorizador.transform(texto_para_vetorizar)
    nota_prevista = modelo.predict(vetor_texto)

    nota_final = round(nota_prevista[0])

    # --- INÍCIO DA CORREÇÃO ---
    # Adicionamos uma "trava" para garantir que a nota fique no intervalo correto.
    if nota_final < 0:
        nota_final = 0
    elif nota_final > 200:
        nota_final = 200
    # --- FIM DA CORREÇÃO ---

    return jsonify({'nota_prevista_c4': nota_final})

# --- 4. EXECUTANDO O SERVIDOR ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)