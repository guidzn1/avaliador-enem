import React, { useState } from 'react';
import './App.css';
import axios from 'axios';

const REDACAO_EXEMPLO = "A questão do acesso ao cinema no Brasil é uma problemática que transcende a simples compra de ingressos. De um lado, a Constituição Federal assegura a todos o direito ao lazer e à cultura. De outro, a realidade de preços elevados e a concentração de salas em grandes centros urbanos criam uma barreira significativa para grande parte da população. Nesse contexto, é fundamental analisar as causas dessa exclusão e propor caminhos para a democratização do acesso à sétima arte.";
const TEMA_EXEMPLO = "Democratização do acesso ao cinema no Brasil";

function App() {
  const [texto, setTexto] = useState('');
  const [tema, setTema] = useState('');
  const [resultado, setResultado] = useState(null);
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState('');

  const analisarRedacao = async () => {
    if (!texto.trim() || !tema.trim()) {
      setErro("Por favor, preencha o tema e a redação.");
      return;
    }
    setCarregando(true);
    setErro('');
    setResultado(null);
    try {
      const response = await axios.post('http://127.0.0.1:5000/prever', {
        tema: tema,
        texto_redacao: texto
      });
      setResultado(response.data);
    } catch (error) {
      console.error("Erro ao conectar com o backend:", error);
      setErro('Não foi possível conectar ao servidor de análise.');
    } finally {
      setCarregando(false);
    }
  };

  const limparTudo = () => {
    setTexto('');
    setTema('');
    setResultado(null);
    setErro('');
  };

  const carregarExemplo = () => {
    setTexto(REDACAO_EXEMPLO);
    setTema(TEMA_EXEMPLO);
  };

  return (
    <div className="App">
      <div className="glass-container">
        <header className="App-header">
          <h1>Análise de Coesão Textual</h1>
          <p>Uma interface moderna para o modelo de ML do seu projeto</p>
        </header>

        <main className="App-main">
          <div className="input-area">
            <input
              type="text"
              className="theme-input"
              placeholder="Digite o tema da redação aqui..."
              value={tema}
              onChange={(e) => setTema(e.target.value)}
              disabled={carregando}
            />
            <textarea
              className="essay-textarea"
              placeholder="Cole sua redação aqui..."
              value={texto}
              onChange={(e) => setTexto(e.target.value)}
              disabled={carregando}
            />
            <div className="button-group">
              <button onClick={analisarRedacao} disabled={!texto || !tema || carregando} className="glow-button primary">
                {carregando ? 'Analisando...' : 'Analisar'}
              </button>
              <button onClick={limparTudo} disabled={carregando} className="glow-button secondary">
                Limpar
              </button>
              <button onClick={carregarExemplo} disabled={carregando} className="glow-button secondary">
                Carregar Exemplo
              </button>
            </div>
          </div>
          
          {erro && <p className="error-message">{erro}</p>}

          {resultado && (
            <div className="results-area">
              <div className="score-card">
                <h3>Nota Final Prevista</h3>
                <p className="score">
                  <span>{resultado.nota_final_prevista}</span> / 1000
                </p>
              </div>
             
              <div className="details-card">
                <h3>Análise Detalhada</h3>
                <ul>
                  <li><strong>Nº de Palavras:</strong> {resultado.analise_detalhada.num_palavras.toFixed(0)}</li>
                  <li><strong>Nº de Frases:</strong> {resultado.analise_detalhada.num_frases.toFixed(0)}</li>
                  <li><strong>Média de Palavras/Frase:</strong> {resultado.analise_detalhada.media_palavras_frase.toFixed(2)}</li>
                  <li><strong>Diversidade Lexical (TTR):</strong> {resultado.analise_detalhada.diversidade_lexical_ttr.toFixed(2)}</li>
                   <li><strong>Nº de Conjunções:</strong> {resultado.analise_detalhada.num_conjuncoes.toFixed(0)}</li>
                </ul>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;