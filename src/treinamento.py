import pandas as pd
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import cohen_kappa_score, mean_squared_error
from scipy.stats import pearsonr

# --- Importando os modelos mencionados no artigo ---
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb

def converter_para_notas(preds):
    """
    Converte as predições de regressão contínuas para as faixas de nota do ENEM.
    Esta lógica precisa ser ajustada para corresponder exatamente à do artigo.
    (Suposição: valores < 20 -> 0, 20-60 -> 40, etc.)
    Vamos usar uma versão simplificada de arredondamento para o múltiplo de 40 mais próximo.
    """
    return (preds / 40).round() * 40

def avaliar_modelos(caminho_dados_processados):
    """
    Função principal para treinar e avaliar os modelos usando cross-validation.
    """
    df = pd.read_csv(caminho_dados_processados)
    
    X = df.drop('c4', axis=1)
    y = df['c4']
    
    # --- Replicação das Condições Experimentais ---
    # O artigo usa 10-fold Stratified Cross Validation. Como é regressão, usaremos KFold.
    # Suposição: KFold é um análogo razoável para a validação cruzada neste contexto.
    kf = KFold(n_splits=10, shuffle=True, random_state=42)
    
    # Dicionário para guardar os modelos a serem avaliados
    modelos = {
        'Linear Regression': LinearRegression(),
        'SVR': SVR(),
        'Random Forest': RandomForestRegressor(random_state=42),
        'XGBoost': xgb.XGBRegressor(random_state=42)
    }
    
    # Dicionário para salvar os resultados
    resultados = {}

    for nome, modelo in modelos.items():
        print(f"--- Treinando e avaliando: {nome} ---")
        
        # Listas para guardar as métricas de cada fold
        kappas = []
        pearsons = []
        
        for i, (train_index, test_index) in enumerate(kf.split(X)):
            X_train, X_test = X.iloc[train_index], X.iloc[test_index]
            y_train, y_test = y.iloc[train_index], y.iloc[test_index]
            
            # Normalização dos dados (importante para SVR e Regressão Linear)
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Treinamento
            modelo.fit(X_train_scaled, y_train)
            
            # Predição
            y_pred = modelo.predict(X_test_scaled)
            
            # Conversão para as notas do ENEM para calcular o Kappa
            y_pred_notas = converter_para_notas(y_pred)
            
            # Cálculo das Métricas
            kappa = cohen_kappa_score(y_test, y_pred_notas, weights='linear')
            p_corr, _ = pearsonr(y_test, y_pred)
            
            kappas.append(kappa)
            pearsons.append(p_corr)
            print(f"  Fold {i+1}/10 - Kappa: {kappa:.3f}, Pearson: {p_corr:.3f}")

        # Média dos resultados dos 10 folds
        resultados[nome] = {
            'Kappa Médio': pd.Series(kappas).mean(),
            'Pearson Médio': pd.Series(pearsons).mean()
        }

    return resultados

if __name__ == '__main__':
    caminho_dados = 'dados/dados_processados.csv'
    resultados_finais = avaliar_modelos(caminho_dados)
    
    print("\n--- Resultados Finais (Média dos 10 folds) ---")
    resultados_df = pd.DataFrame(resultados_finais).T
    print(resultados_df)
    
    # Salva os resultados em um CSV para análise posterior
    resultados_df.to_csv('resultados/resultados_experimento.csv')
    print("\nResultados salvos em 'resultados/resultados_experimento.csv'")