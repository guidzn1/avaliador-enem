import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

print("--- INICIANDO TREINAMENTO DO MODELO FINAL ---")

# 1. Carregar os dados processados
print("Carregando dados processados...")
caminho_dados = 'dados/dados_processados.csv'
df = pd.read_csv(caminho_dados)

X = df.drop('score', axis=1)
y = df['score']

# 2. Preparar os dados (Normalização)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("Dados normalizados.")

# 3. Escolher e configurar o modelo final
modelo_final = RandomForestRegressor(random_state=42)
print(f"Modelo escolhido: {type(modelo_final).__name__}")

# 4. Treinar o modelo com TODOS os dados
print("Treinando o modelo com todos os dados... Isso pode levar alguns minutos.")
modelo_final.fit(X_scaled, y)
print("Treinamento concluído com sucesso!")

# 5. Salvar o modelo e o normalizador no backend para produção
caminho_backend = 'backend/'
joblib.dump(modelo_final, os.path.join(caminho_backend, 'modelo_nota_final.pkl'))
joblib.dump(scaler, os.path.join(caminho_backend, 'scaler.pkl'))

print(f"Modelo final e normalizador foram salvos na pasta '{caminho_backend}'.")
print("--- PROCESSO FINALIZADO ---")