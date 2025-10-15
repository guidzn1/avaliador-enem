import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV # <-- A nossa nova ferramenta de otimização
import joblib
import os

print("--- INICIANDO OTIMIZAÇÃO E TREINAMENTO DO MODELO FINAL ---")

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

# 3. Definir o "grid" de hiperparâmetros para testar
# ATENÇÃO: Este é um grid pequeno para que o processo não demore horas.
# Em um projeto real, testaríamos muito mais combinações.
param_grid = {
    'n_estimators': [100, 200],      # Testar com 100 e 200 árvores
    'max_depth': [10, 20, None],     # Testar com profundidade máxima de 10, 20 ou sem limite
    'min_samples_split': [2, 5]      # Testar com o mínimo de 2 ou 5 amostras para dividir
}

# 4. Configurar o modelo e a busca pelos melhores parâmetros
rf = RandomForestRegressor(random_state=42)
grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, 
                           cv=3, n_jobs=-1, verbose=2, scoring='neg_mean_squared_error')
# cv=3: Usa uma validação cruzada de 3 folds para testar cada combinação.
# n_jobs=-1: Usa todos os processadores do seu computador.
# verbose=2: Mostra o progresso da busca.
# scoring='neg_mean_squared_error': A métrica para decidir qual combinação é a melhor.

print("Iniciando a busca pelos melhores hiperparâmetros... ISTO VAI DEMORAR BASTANTE.")
grid_search.fit(X_scaled, y)

print("\nBusca concluída!")
print("Melhores parâmetros encontrados:")
print(grid_search.best_params_)

# 5. Usar o melhor modelo encontrado pela busca
modelo_otimizado = grid_search.best_estimator_

# 6. Salvar o modelo otimizado e o normalizador
caminho_backend = 'backend/'
joblib.dump(modelo_otimizado, os.path.join(caminho_backend, 'modelo_nota_final_otimizado.pkl'))
joblib.dump(scaler, os.path.join(caminho_backend, 'scaler.pkl')) # O scaler continua o mesmo

print(f"\nModelo final OTIMIZADO e normalizador foram salvos na pasta '{caminho_backend}'.")
print("--- PROCESSO FINALIZADO ---")