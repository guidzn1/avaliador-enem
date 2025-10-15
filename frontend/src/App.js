import React, { useState } from 'react';
import './App.css'; // Nosso arquivo de estilos
import axios from 'axios'; // Ferramenta para conectar com o backend

function App() {
  // --- ESTADOS DO COMPONENTE ---
  // Guarda o texto da redação que o usuário digita
  const [texto, setTexto] = useState('');
  // Guarda a nota recebida do backend
  const [nota, setNota] = useState(null);
  // Controla o estado de "carregando" durante a análise
  const [carregando, setCarregando] = useState(false);
  // Guarda mensagens de erro
  const [erro, setErro] = useState('');

  // --- FUNÇÃO DE SUBMISSÃO ---
  const analisarRedacao = async () => {
    // Nielsen: Visibilidade do status do sistema.
    setCarregando(true);
    setErro('');
    setNota(null);

    try {
      // Faz a requisição POST para o nosso backend Flask
      const response = await axios.post('http://127.0.0.1:5000/prever', {
        texto_redacao: texto
      });

      // Apple HIG: Clareza. Mostra o resultado de forma direta.
      setNota(response.data.nota_prevista_c4);

    } catch (error) {
      // Nielsen: Ajuda e diagnóstico de erros.
      console.error("Erro ao conectar com o backend:", error);
      setErro('Não foi possível conectar ao servidor de análise. Verifique se o backend está rodando.');
    } finally {
      // Nielsen: Visibilidade do status do sistema.
      setCarregando(false);
    }
  };

  // --- RENDERIZAÇÃO DO HTML (JSX) ---
  return (
    <div className="App">
      <header className="App-header">
        <h1>Avaliador de Coesão Textual</h1>
        <p>Inspirado no artigo "Combinação de Modelos de Aprendizado de Máquina"</p>
      </header>

      <main className="App-main">
        <textarea
          className="essay-textarea"
          placeholder="Digite ou cole a sua redação aqui..."
          value={texto}
          onChange={(e) => setTexto(e.target.value)}
          disabled={carregando} // Nielsen: Prevenção de erros. Desabilita enquanto carrega.
        />
        <button 
          className="analyze-button" 
          onClick={analisarRedacao}
          disabled={!texto || carregando} // Desabilita se não houver texto ou se estiver carregando
        >
          {carregando ? 'Analisando...' : 'Analisar Coesão'}
        </button>

        {/* --- ÁREA DE RESULTADO --- */}
        {/* Apple HIG & Nielsen: Feedback imediato e claro. */}
        {nota !== null && (
          <div className="result-container">
            <h2>Nota Prevista (Competência IV):</h2>
            <p className="score">{nota} / 200</p>
          </div>
        )}

        {erro && (
          <div className="error-container">
            <p>{erro}</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;