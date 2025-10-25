import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import joblib
import os

print("--- INICIANDO OTIMIZAÇÃO E TREINAMENTO (FOCO: COESÃO) ---")

# 1. Carregar os dados processados
print("Carregando dados processados...")
caminho_dados = 'dados/dados_processados.csv'
df = pd.read_csv(caminho_dados)

# --- Foco em 'c4' ---
X = df.drop('c4', axis=1)
y = df['c4']

# 2. Preparar os dados (Normalização)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("Dados normalizados.")

# 3. Definir o "grid" de hiperparâmetros para testar
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5]
}

# 4. Configurar o modelo e a busca
rf = RandomForestRegressor(random_state=42)
grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, 
                           cv=3, n_jobs=-1, verbose=2, scoring='neg_mean_squared_error')

print("Iniciando a busca pelos melhores hiperparâmetros (Foco: Coesão)... ISTO VAI DEMORAR BASTANTE.")
grid_search.fit(X_scaled, y)

print("\nBusca concluída!")
print("Melhores parâmetros encontrados:")
print(grid_search.best_params_)

# 5. Usar o melhor modelo encontrado
modelo_otimizado = grid_search.best_estimator_

# 6. Salvar o modelo otimizado e o normalizador
caminho_backend = 'backend/'
# Salvamos o modelo de coesão
joblib.dump(modelo_otimizado, os.path.join(caminho_backend, 'modelo_coesao_otimizado.pkl'))
joblib.dump(scaler, os.path.join(caminho_backend, 'scaler.pkl'))

print(f"\nModelo final OTIMIZADO (Coesão) e normalizador foram salvos na pasta '{caminho_backend}'.")
print("--- PROCESSO FINALIZADO ---")