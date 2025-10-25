# 🤖 Avaliador de Coesão Textual (CoesIA)

Este projeto é uma aplicação web *full-stack* que utiliza Machine Learning para prever a nota de **Coesão Textual (Competência IV do ENEM)** de redações escritas em português. A plataforma permite que o utilizador insira o tema e o texto da redação, recebendo em troca uma análise detalhada e uma pontuação predita de 0 a 200.

O sistema foi desenvolvido como parte de um trabalho acadêmico inspirado pela metodologia do artigo: *"Combinação de Modelos de Aprendizado de Máquina utilizando Teoria de Resposta ao Item para Avaliação de Coesão Textual em Redações no contexto do ENEM"*.

![Interface do CoesIA](<placeholder_para_sua_imagem.png>)
*(Substitua este texto por um print da sua aplicação a funcionar!)*

---

## ✨ Funcionalidades

* **Interface Moderna:** Design responsivo em *dark mode* com efeitos *glassmorphism* e foco na experiência do utilizador.
* **Análise Preditiva:** Utiliza um modelo `RandomForestRegressor` otimizado para prever a nota de coesão (0-200).
* **Análise Detalhada:** Fornece métricas linguísticas extraídas do texto, como número de palavras, frases, diversidade lexical e contagem de conjunções.
* **Contexto do Tema:** O modelo leva em consideração o **tema** da redação, combinando-o com o texto para uma análise mais precisa.
* **API RESTful:** O backend em Flask expõe um endpoint `/prever` para consumir o modelo de ML.

---

## 🛠️ Stack Tecnológica

O projeto é dividido em três componentes principais:

* **Frontend (Interface do Utilizador)**
    * **React** (v18+)
    * **Axios** (para comunicação com a API)
    * **CSS Puro** (para estilização)

* **Backend (Servidor & API)**
    * **Python** (v3.10+)
    * **Flask** (para criar a API RESTful)
    * **Flask-CORS** (para permitir a comunicação entre domínios)

* **Machine Learning (Pipeline de Treino)**
    * **Scikit-learn** (para `RandomForestRegressor`, `GridSearchCV`, `StandardScaler`)
    * **Pandas** (para manipulação de dados)
    * **Spacy** (para extração de características linguísticas, como contagem de classes gramaticais)
    * **Joblib** (para salvar e carregar os modelos treinados)

---

## 🚀 Como Executar o Projeto

Siga os passos abaixo para configurar e executar o projeto localmente.

### Pré-requisitos

* [Python 3.10+](https://www.python.org/downloads/)
* [Node.js (LTS)](https://nodejs.org/en/)
* Os dados do `extended_essay-br.csv` e `prompts.csv` devem estar na pasta `/dados`.

### 1. Configuração do Ambiente Virtual (Backend)

Todos os comandos do backend devem ser executados a partir da pasta raiz do projeto (`/avaliador-enem`).

```bash
# 1. Crie o ambiente virtual
python -m venv venv

# 2. Ative o ambiente virtual
# Windows
.\venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 3. Crie um arquivo requirements.txt na raiz do projeto
# (Copie e cole o conteúdo abaixo nele)
requirements.txt:

Plaintext

flask
flask_cors
pandas
scikit-learn
spacy
xgboost
notebook
joblib
Bash

# 4. Instale todas as dependências do Python
pip install -r requirements.txt

# 5. Baixe o modelo de linguagem do Spacy
python -m spacy download pt_core_news_sm
2. Treino do Modelo de ML
Antes de iniciar o servidor, precisa de treinar o modelo. O script treinar_modelo_otimizado.py fará todo o processo: pré-processamento, otimização com GridSearchCV e salvamento do modelo final.

Bash

# 1. Execute o script de pré-processamento
python src/preprocessamento.py

# 2. Execute o script de treino otimizado
# ATENÇÃO: Este processo pode levar vários minutos (ou horas)!
python src/treinar_modelo_otimizado.py
No final, os ficheiros modelo_coesao_otimizado.pkl e scaler.pkl estarão na pasta /backend.

3. Iniciar os Servidores
Precisará de dois terminais abertos.

Terminal 1: Iniciar o Backend (Python/Flask)

Bash

# (Certifique-se de que o venv está ativo)
python backend/app.py
O servidor estará a ser executado em http://127.0.0.1:5000.

Terminal 2: Iniciar o Frontend (React)

Bash

# 1. Navegue até à pasta do frontend
cd frontend

# 2. Instale as dependências do Node.js (só na primeira vez)
npm install

# 3. Inicie a aplicação React
npm start
O seu navegador abrirá automaticamente em http://localhost:3000.

📂 Estrutura do Projeto
/avaliador-enem/
|
|-- 📂 backend/
|   |-- 📄 app.py                     # Servidor Flask (API)
|   |-- 📄 modelo_coesao_otimizado.pkl # Modelo de ML treinado
|   '-- 📄 scaler.pkl                # Normalizador dos dados
|
|-- 📂 dados/
|   |-- 📄 extended_essay-br.csv     # Dataset de redações
|   |-- 📄 prompts.csv               # Dataset de temas
|   '-- 📄 dados_processados.csv     # CSV gerado pelo pré-processamento
|
|-- 📂 frontend/
|   |-- 📂 src/
|   |   |-- 📄 App.js                 # Componente principal do React
|   |   '-- 📄 App.css                # Estilização da interface
|   '-- 📄 package.json              # Dependências do frontend
|
|-- 📂 notebooks/
|   '-- ... (Notebooks de exploração inicial)
|
|-- 📂 resultados/
|   '-- ... (Resultados de experimentos)
|
|-- 📂 src/
|   |-- 📄 preprocessamento.py       # Script de extração de features (SpaCy)
|   '-- 📄 treinar_modelo_otimizado.py # Script de treino final (GridSearchCV)
|
|-- 📄 requirements.txt              # Dependências do Python
'-- 📄 README.md                     # Este ficheiro
📈 Resultados e Aprendizagens
O modelo RandomForestRegressor otimizado demonstrou ser robusto para a tarefa, prevendo redações de nota máxima (1000) com alta precisão para a coesão (ex: 170-187 / 200).

O modelo também se mostrou capaz de diferenciar textos de baixa qualidade (ex: 96 / 200), validando a sua capacidade de generalização.

A inclusão do tema da redação como feature (combinado ao texto) foi uma etapa crucial para aumentar a consistência e a precisão das previsões.
