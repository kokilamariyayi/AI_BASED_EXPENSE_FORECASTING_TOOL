import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const COLORS = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b', '#fa709a'];

function Analytics({ username, onLogout }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filters, setFilters] = useState({
    year: '',
    month: '',
    start: '',
    end: ''
  });

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    setLoading(true);
    setError('');

    try {
      const params = new URLSearchParams();
      if (filters.year) params.append('year', filters.year);
      if (filters.month) params.append('month', filters.month);
      if (filters.start) params.append('start', filters.start);
      if (filters.end) params.append('end', filters.end);

      const response = await axios.get(`/api/analytics?${params.toString()}`);
      setData(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch analytics');
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (e) => {
    setFilters({
      ...filters,
      [e.target.name]: e.target.value
    });
  };

  const applyFilters = () => {
    fetchAnalytics();
  };

  const resetFilters = () => {
    setFilters({
      year: '',
      month: '',
      start: '',
      end: ''
    });
    setTimeout(fetchAnalytics, 100);
  };

  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading analytics...</p>
        </div>
      </div>
    );
  }

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
        <h2 style={{ color: '#667eea', marginBottom: '20px' }}>📊 Expense Analytics</h2>

        {error && (
          <div className="error-message">
            {error}
            <div style={{ marginTop: '10px' }}>
              <Link to="/upload" style={{ color: '#667eea', fontWeight: 'bold' }}>
                Upload a CSV file to get started
              </Link>
            </div>
          </div>
        )}

        {!error && data && (
          <>
            <div className="analytics-filters">
              <input
                type="number"
                name="year"
                placeholder="Year (e.g., 2024)"
                value={filters.year}
                onChange={handleFilterChange}
              />
              <input
                type="number"
                name="month"
                placeholder="Month (1-12)"
                value={filters.month}
                onChange={handleFilterChange}
                min="1"
                max="12"
              />
              <input
                type="date"
                name="start"
                placeholder="Start Date"
                value={filters.start}
                onChange={handleFilterChange}
              />
              <input
                type="date"
                name="end"
                placeholder="End Date"
                value={filters.end}
                onChange={handleFilterChange}
              />
              <button onClick={applyFilters} className="btn-secondary">Apply Filters</button>
              <button onClick={resetFilters} className="btn-secondary">Reset</button>
            </div>

            {/* Summary Cards */}
            <div className="analytics-grid">
              <div className="analytics-card">
                <h3>Total Spending</h3>
                <div className="stat-value">₹{data.summary.total.toLocaleString('en-IN', { maximumFractionDigits: 2 })}</div>
                <div className="stat-label">Across all categories</div>
              </div>

              <div className="analytics-card">
                <h3>Top Category</h3>
                <div className="stat-value">{data.summary.top_cat || 'N/A'}</div>
                <div className="stat-label">Highest spending category</div>
              </div>

              <div className="analytics-card">
                <h3>Peak Spending Day</h3>
                <div className="stat-value">₹{data.summary.peak_amount.toLocaleString('en-IN', { maximumFractionDigits: 2 })}</div>
                <div className="stat-label">{data.summary.peak_day || 'N/A'}</div>
              </div>
            </div>

            {/* Charts */}
            <div style={{ marginTop: '40px' }}>
              <h3 style={{ color: '#667eea', marginBottom: '20px' }}>Monthly Trend</h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={data.monthly}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month_year" />
                  <YAxis />
                  <Tooltip formatter={(value) => `₹${value.toLocaleString('en-IN')}`} />
                  <Legend />
                  <Line type="monotone" dataKey="amount" stroke="#667eea" strokeWidth={2} name="Expenses" />
                </LineChart>
              </ResponsiveContainer>
            </div>

            <div style={{ marginTop: '40px' }}>
              <h3 style={{ color: '#667eea', marginBottom: '20px' }}>Spending by Category</h3>
              <ResponsiveContainer width="100%" height={400}>
                <PieChart>
                  <Pie
                    data={data.category.slice(0, 6)}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={(entry) => `${entry.category}: ₹${entry.amount.toLocaleString('en-IN')}`}
                    outerRadius={120}
                    fill="#8884d8"
                    dataKey="amount"
                  >
                    {data.category.slice(0, 6).map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => `₹${value.toLocaleString('en-IN')}`} />
                </PieChart>
              </ResponsiveContainer>
            </div>

            <div style={{ marginTop: '40px' }}>
              <h3 style={{ color: '#667eea', marginBottom: '20px' }}>Top Categories</h3>
              <ul className="category-list">
                {data.category.slice(0, 10).map((cat, index) => (
                  <li key={index}>
                    <span>{cat.category}</span>
                    <span style={{ fontWeight: 'bold', color: '#667eea' }}>
                      ₹{cat.amount.toLocaleString('en-IN', { maximumFractionDigits: 2 })}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default Analytics;
