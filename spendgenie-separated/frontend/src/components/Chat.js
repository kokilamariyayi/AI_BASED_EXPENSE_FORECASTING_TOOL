import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

function Chat({ username, onLogout }) {
  const [messages, setMessages] = useState([
    { type: 'bot', text: 'Hi! I\'m SpendGenie AI. Ask me about your spending patterns, budgeting tips, or predictions!' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = input.trim();
    setInput('');
    setMessages(prev => [...prev, { type: 'user', text: userMessage }]);
    setLoading(true);

    try {
      const response = await axios.post('/api/chat', {
        message: userMessage
      });

      setMessages(prev => [...prev, { type: 'bot', text: response.data.reply }]);
    } catch (err) {
      setMessages(prev => [...prev, { 
        type: 'bot', 
        text: 'Sorry, I encountered an error. Please try again.' 
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const quickQuestions = [
    'What are my top categories?',
    'Show me monthly trend',
    'How can I save money?',
    'Predict next month'
  ];

  const handleQuickQuestion = (question) => {
    setInput(question);
  };

  return (
    <div className="dashboard-container">
      <div className="navbar">
        <h1>🧞 SpendGenie</h1>
        <div className="navbar-right">
          <span>Welcome, {username}!</span>
          <button onClick={onLogout} className="btn-secondary">Logout</button>
        </div>
      </div>

      <div className="nav-links">
        <Link to="/dashboard" className="nav-link">Dashboard</Link>
        <Link to="/upload" className="nav-link">Upload Data</Link>
        <Link to="/analytics" className="nav-link">Analytics</Link>
        <Link to="/chat" className="nav-link">AI Chat</Link>
      </div>

      <div className="dashboard-content">
        <h2 style={{ color: '#667eea', marginBottom: '20px' }}>🤖 AI Chat Assistant</h2>

        <div style={{ marginBottom: '20px' }}>
          <p style={{ color: '#666', marginBottom: '10px' }}>Quick questions:</p>
          <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
            {quickQuestions.map((question, index) => (
              <button
                key={index}
                onClick={() => handleQuickQuestion(question)}
                style={{
                  padding: '8px 16px',
                  background: '#f0f2ff',
                  color: '#667eea',
                  border: '1px solid #667eea',
                  borderRadius: '20px',
                  cursor: 'pointer',
                  fontSize: '14px'
                }}
              >
                {question}
              </button>
            ))}
          </div>
        </div>

        <div className="chat-container">
          <div className="chat-messages">
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.type}`}>
                {msg.text}
              </div>
            ))}
            {loading && (
              <div className="message bot">
                <div className="spinner" style={{ width: '20px', height: '20px', borderWidth: '2px' }}></div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="chat-input-container">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me anything about your expenses..."
              disabled={loading}
            />
            <button onClick={handleSend} disabled={loading || !input.trim()}>
              Send
            </button>
          </div>
        </div>

        <div style={{ marginTop: '20px', padding: '15px', background: '#f8f9ff', borderRadius: '8px' }}>
          <h4 style={{ color: '#667eea', marginBottom: '10px' }}>💡 Try asking:</h4>
          <ul style={{ color: '#666', lineHeight: '1.8', marginLeft: '20px' }}>
            <li>"What are my top spending categories?"</li>
            <li>"Show me my monthly spending trend"</li>
            <li>"How can I reduce my dining expenses?"</li>
            <li>"Give me some saving tips"</li>
            <li>"Predict my next month's expenses"</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default Chat;
