import pandas as pd
import spacy
from collections import Counter

# Carregar o modelo de linguagem do spaCy para o português
try:
    nlp = spacy.load("pt_core_news_sm")
except OSError:
    print("Modelo 'pt_core_news_sm' do spaCy não encontrado.")
    print("Por favor, rode o comando: python -m spacy download pt_core_news_sm")
    exit()

def extrair_features(texto):
    """
    Esta função extrai um conjunto simplificado de características linguísticas de um texto.
    """
    doc = nlp(texto)
    
    num_palavras = len([token for token in doc if not token.is_punct])
    num_frases = len(list(doc.sents))
    media_palavras_frase = num_palavras / num_frases if num_frases > 0 else 0
    palavras_unicas = len(set(token.text.lower() for token in doc if not token.is_punct))
    ttr = palavras_unicas / num_palavras if num_palavras > 0 else 0
    contagem_pos = Counter(token.pos_ for token in doc if not token.is_punct)
    
    features = {
        'num_palavras': num_palavras, 'num_frases': num_frases,
        'media_palavras_frase': media_palavras_frase, 'diversidade_lexical_ttr': ttr,
        'num_verbos': contagem_pos.get('VERB', 0), 'num_substantivos': contagem_pos.get('NOUN', 0),
        'num_adjetivos': contagem_pos.get('ADJ', 0), 'num_adverbios': contagem_pos.get('ADV', 0),
        'num_conjuncoes': contagem_pos.get('CCONJ', 0) + contagem_pos.get('SCONJ', 0),
    }
    return features

def preparar_dados(caminho_redacoes, caminho_temas):
    """
    Carrega ambos os arquivos, junta-os usando os nomes de coluna corretos
    e cria um texto combinado para a extração de features.
    """
    print("Carregando dados de redações e temas...")
    df_redacoes = pd.read_csv(caminho_redacoes)
    df_temas = pd.read_csv(caminho_temas)

    print("Juntando os dataframes...")
    df_completo = pd.merge(df_redacoes, df_temas, left_on='prompt', right_on='id')

    # --- CORREÇÃO AQUI ---
    # Voltamos a usar 'c4' como a nossa coluna-alvo.
    df_modelo = df_completo[['essay', 'title_y', 'c4']].copy()
    df_modelo.dropna(inplace=True)

    print("Combinando tema e redação em um único texto...")
    df_modelo['texto_combinado'] = df_modelo['title_y'] + " " + df_modelo['essay']
    
    print("Iniciando extração de características do texto combinado... Isso pode demorar.")
    features_df = df_modelo['texto_combinado'].apply(lambda texto: pd.Series(extrair_features(texto)))
    
    features_df.reset_index(drop=True, inplace=True)
    df_modelo.reset_index(drop=True, inplace=True)
    
    # --- CORREÇÃO AQUI ---
    # Selecionamos as colunas de features e a nota de coesão 'c4'
    df_final = pd.concat([features_df, df_modelo['c4']], axis=1)
    
    print("Preparação de dados concluída.")
    return df_final

if __name__ == '__main__':
    caminho_redacoes = 'dados/extended_essay-br.csv'
    caminho_temas = 'dados/prompts.csv'
    
    dados_processados = preparar_dados(caminho_redacoes, caminho_temas)
    
    print("\nVisualização dos dados processados:")
    print(dados_processados.head())
    
    dados_processados.to_csv('dados/dados_processados.csv', index=False)
    print("\nNovos dados processados (para COESÃO) salvos com sucesso em 'dados/dados_processados.csv'")