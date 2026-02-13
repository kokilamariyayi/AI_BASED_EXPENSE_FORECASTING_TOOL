import React from 'react';
import { Link } from 'react-router-dom';

function Dashboard({ username, onLogout }) {
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
        <div className="welcome-section">
          <h2>Welcome to SpendGenie!</h2>
          <p>Your AI-powered personal expense tracking companion</p>

          <div className="features-grid">
            <div className="feature-card">
              <h3>📊 Analytics</h3>
              <p>Get detailed insights into your spending patterns with interactive charts and reports</p>
            </div>

            <div className="feature-card">
              <h3>🤖 AI Assistant</h3>
              <p>Chat with our AI to get personalized financial advice and spending tips</p>
            </div>

            <div className="feature-card">
              <h3>📈 Predictions</h3>
              <p>See forecasts of your future expenses based on historical data</p>
            </div>

            <div className="feature-card">
              <h3>💰 Budget Tracking</h3>
              <p>Monitor your spending by category and stay within your budget</p>
            </div>
          </div>

          <div style={{ marginTop: '40px' }}>
            <h3 style={{ marginBottom: '20px', color: '#667eea' }}>Quick Start Guide</h3>
            <ol style={{ textAlign: 'left', maxWidth: '600px', margin: '0 auto', lineHeight: '2' }}>
              <li>Upload your expense CSV file in the <Link to="/upload">Upload Data</Link> section</li>
              <li>View detailed analytics and visualizations in <Link to="/analytics">Analytics</Link></li>
              <li>Chat with our AI assistant in <Link to="/chat">AI Chat</Link> for personalized tips</li>
              <li>Get predictions and insights to improve your financial health</li>
            </ol>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
