import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

function Upload({ username, onLogout }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [fileInfo, setFileInfo] = useState(null);
  const navigate = useNavigate();

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (!file.name.endsWith('.csv')) {
        setError('Please select a CSV file');
        setSelectedFile(null);
        return;
      }
      setSelectedFile(file);
      setError('');
      setMessage('');
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a file first');
      return;
    }

    setUploading(true);
    setError('');
    setMessage('');

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      setMessage(response.data.message);
      setFileInfo({
        rows: response.data.rows,
        columns: response.data.columns
      });

      // Redirect to analytics after 2 seconds
      setTimeout(() => {
        navigate('/analytics');
      }, 2000);
    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed. Please try again.');
    } finally {
      setUploading(false);
    }
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
        <div className="upload-section">
          <h2>Upload Your Expense Data</h2>
          <p style={{ textAlign: 'center', color: '#666', marginBottom: '30px' }}>
            Upload a CSV file containing your transaction data
          </p>

          {error && <div className="error-message">{error}</div>}
          {message && <div className="success-message">{message}</div>}

          <div className="upload-box" onClick={() => document.getElementById('fileInput').click()}>
            <input
              id="fileInput"
              type="file"
              accept=".csv"
              onChange={handleFileSelect}
            />
            <div>
              <p style={{ fontSize: '48px', marginBottom: '20px' }}>📄</p>
              <p style={{ fontSize: '18px', fontWeight: '600', marginBottom: '10px' }}>
                {selectedFile ? selectedFile.name : 'Click to select CSV file'}
              </p>
              <p style={{ fontSize: '14px', color: '#666' }}>
                {selectedFile ? `Size: ${(selectedFile.size / 1024).toFixed(2)} KB` : 'or drag and drop'}
              </p>
            </div>
          </div>

          {selectedFile && (
            <div style={{ marginTop: '20px', textAlign: 'center' }}>
              <button 
                onClick={handleUpload} 
                className="btn-primary" 
                disabled={uploading}
                style={{ maxWidth: '300px' }}
              >
                {uploading ? 'Uploading...' : 'Upload and Analyze'}
              </button>
            </div>
          )}

          {fileInfo && (
            <div className="file-info">
              <h3 style={{ marginBottom: '10px' }}>File Details:</h3>
              <p>✅ Rows: {fileInfo.rows}</p>
              <p>✅ Columns: {fileInfo.columns.join(', ')}</p>
              <p style={{ marginTop: '10px', color: '#667eea', fontWeight: '600' }}>
                Redirecting to analytics...
              </p>
            </div>
          )}

          <div style={{ marginTop: '40px', textAlign: 'left', maxWidth: '500px', margin: '40px auto 0' }}>
            <h3 style={{ color: '#667eea', marginBottom: '15px' }}>CSV Format Requirements:</h3>
            <ul style={{ lineHeight: '2', color: '#666' }}>
              <li>Must include a <strong>date</strong> column (date, transaction_date, etc.)</li>
              <li>Must include an <strong>amount</strong> column (amount, value, etc.)</li>
              <li>Optional: <strong>category</strong> column for expense categorization</li>
              <li>Optional: <strong>description</strong> column for transaction details</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Upload;
