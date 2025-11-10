import { useState, useRef, useEffect } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([
    { role: 'agent', content: 'Hello! I am your Astiva AI Competitive Intelligence Agent. How can I help you analyze brand visibility today?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;
    
    const userMessage = input.trim();
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setInput('');
    setIsLoading(true);

    try {
      // In a real env, this points to your FastAPI backend
      const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage })
      });
      
      const data = await response.json();
      setMessages(prev => [...prev, { role: 'agent', content: data.response || "Sorry, I couldn't process that." }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'agent', content: "Error connecting to the backend. Is FastAPI running?" }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    alert(`File "${file.name}" selected! In a production app, this would be uploaded to /api/v1/documents for background RAG indexing via Celery.`);
  };

  return (
    <div className="app-container">
      <header className="header">
        <div className="logo-section">
          <h1>Astiva AI</h1>
          <p>Competitive Intelligence Platform</p>
        </div>
        <div className="status-badge glass-panel" style={{padding: '8px 16px', borderRadius: '20px', fontSize: '14px'}}>
          <span style={{color: 'var(--success)', marginRight: '8px'}}>●</span> All Systems Operational
        </div>
      </header>

      <main className="dashboard-grid">
        
        {/* RAG & Analytics Panel */}
        <section className="rag-panel glass-panel">
          <h2>Knowledge Base (RAG)</h2>
          <p style={{color: 'var(--text-secondary)', fontSize: '14px', marginBottom: '16px'}}>Upload documents to enhance agent context.</p>
          
          <label className="upload-area">
            <span className="upload-icon">📄</span>
            <p>Click to upload or drag and drop</p>
            <p style={{fontSize: '12px', color: 'var(--text-secondary)', marginTop: '8px'}}>PDF, TXT, DOCX (Max 10MB)</p>
            <input type="file" style={{display: 'none'}} onChange={handleFileUpload} />
          </label>

          <div style={{marginTop: '32px'}}>
            <h3 style={{marginBottom: '16px'}}>Platform Metrics</h3>
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-value">14,203</div>
                <div className="stat-label">Vectors Indexed</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">2.4s</div>
                <div className="stat-label">Avg Agent Latency</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">98%</div>
                <div className="stat-label">Retrieval Accuracy</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">4</div>
                <div className="stat-label">Active Background Jobs</div>
              </div>
            </div>
          </div>
        </section>

        {/* Agent Interaction Panel */}
        <section className="chat-panel glass-panel">
          <div className="chat-messages">
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.role}`}>
                {msg.content}
              </div>
            ))}
            {isLoading && (
              <div className="message agent">
                <div className="typing-indicator">Agent is thinking...</div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          
          <div className="chat-input-area">
            <input 
              type="text" 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Ask about brand visibility (e.g. 'How does Acme Corp appear on ChatGPT?')"
            />
            <button 
              className="send-btn" 
              onClick={handleSend}
              disabled={isLoading || !input.trim()}
            >
              Send
            </button>
          </div>
        </section>

      </main>
    </div>
  );
}

export default App;
