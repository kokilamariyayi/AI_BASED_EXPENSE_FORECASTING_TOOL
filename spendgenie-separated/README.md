# 🧞 SpendGenie - AI-Powered Expense Tracker

SpendGenie is a complete full-stack application for tracking and analyzing personal expenses with AI-powered insights.

## 🏗️ Architecture

- **Backend**: Flask (Python) REST API
- **Frontend**: React (JavaScript) SPA
- **Database**: SQLite
- **AI Features**: Linear regression for predictions, rule-based chatbot

## ✨ Features

- 👤 User Authentication (Register/Login)
- 📊 Interactive Analytics Dashboard
- 📈 Expense Trend Visualization
- 🤖 AI Chat Assistant
- 💡 Predictive Expense Forecasting
- 📁 CSV File Upload and Processing
- 🎯 Category-wise Expense Analysis

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn

### Installation Steps

#### 1. Clone/Extract the Project

```bash
cd spendgenie-separated
```

#### 2. Setup Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the backend server
python app.py
```

The backend will start on `http://localhost:5000`

#### 3. Setup Frontend (New Terminal)

```bash
# Navigate to frontend (from project root)
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

The frontend will automatically open at `http://localhost:3000`

## 📝 Usage Guide

### Step 1: Register an Account
1. Open `http://localhost:3000`
2. Click "Register here"
3. Fill in your details and create an account

### Step 2: Upload Your Data
1. Go to "Upload Data" section
2. Upload a CSV file with your expense data
3. Required columns: date, amount
4. Optional columns: category, description

### Step 3: View Analytics
1. Navigate to "Analytics"
2. View charts and statistics
3. Apply filters by year, month, or date range

### Step 4: Chat with AI
1. Go to "AI Chat"
2. Ask questions like:
   - "What are my top categories?"
   - "Show me monthly trend"
   - "How can I save money?"
   - "Predict next month's expenses"

## 📂 Project Structure

```
spendgenie-separated/
├── backend/
│   ├── app.py              # Flask application
│   ├── requirements.txt    # Python dependencies
│   ├── data/              # SQLite database & uploads
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── App.js         # Main app component
│   │   └── App.css        # Styles
│   ├── public/
│   ├── package.json       # Node dependencies
│   └── README.md
└── README.md              # This file
```

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/status` - Check auth status

### Data Management
- `POST /api/upload` - Upload CSV file
- `GET /api/analytics` - Get expense analytics
- `GET /api/summary` - Get AI summary
- `POST /api/chat` - Chat with AI

## 📊 CSV Format

Your CSV file should have these columns:

**Required:**
- `date` (or transaction_date, txn_date, posted_date, timestamp)
- `amount` (or amt, value, transaction_amount)

**Optional:**
- `category` (or cat, expense_category, type)
- `description` (or memo, narration, details)

**Example:**
```csv
date,amount,category,description
2024-01-15,500,Food,Grocery shopping
2024-01-16,1200,Transport,Fuel
2024-01-17,300,Entertainment,Movie tickets
```

## 🛠️ Technology Stack

### Backend
- Flask - Web framework
- SQLAlchemy - ORM
- Bcrypt - Password hashing
- Pandas - Data processing
- Scikit-learn - ML predictions
- Flask-CORS - Cross-origin requests

### Frontend
- React - UI library
- React Router - Navigation
- Axios - HTTP client
- Recharts - Data visualization

## 🔒 Security Features

- Password hashing with bcrypt
- Session-based authentication
- CORS protection
- Input validation
- Secure file upload handling

## 🐛 Troubleshooting

### Backend Issues

**Error: Module not found**
```bash
# Make sure virtual environment is activated
pip install -r requirements.txt
```

**Error: Port 5000 already in use**
```python
# Change port in app.py
app.run(host='0.0.0.0', port=5001, debug=True)
```

### Frontend Issues

**Error: Cannot connect to backend**
- Ensure backend is running on port 5000
- Check proxy setting in package.json

**Error: npm install fails**
```bash
# Clear npm cache
npm cache clean --force
# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json
# Reinstall
npm install
```

## 📈 Future Enhancements

- [ ] Budget setting and alerts
- [ ] Recurring expense detection
- [ ] Multi-currency support
- [ ] Export reports as PDF
- [ ] Mobile responsive design
- [ ] Advanced ML models
- [ ] Social sharing features
- [ ] Integration with bank APIs

## 👥 Contributors

SpendGenie Project Team

## 📄 License

This project is for educational purposes.

## 🙏 Acknowledgments

- Flask documentation
- React documentation
- Recharts library
- OpenAI for inspiration

---

**Happy Tracking! 🧞✨**

For issues or questions, please refer to the individual README files in backend/ and frontend/ directories.
