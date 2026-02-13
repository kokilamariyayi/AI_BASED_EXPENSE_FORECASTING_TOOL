# SpendGenie Backend (Flask API)

This is the backend API for SpendGenie expense tracker application.

## Setup Instructions

### 1. Create Virtual Environment

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Server

```bash
python app.py
```

The backend will start on `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/status` - Check authentication status

### Data Management
- `POST /api/upload` - Upload CSV file
- `GET /api/analytics` - Get expense analytics
- `GET /api/summary` - Get AI summary
- `POST /api/chat` - Chat with AI assistant

### Health Check
- `GET /api/health` - Check API status

## Database

The application uses SQLite database stored in `./data/users.db`

## File Uploads

Uploaded CSV files are stored in `./data/uploads/<session_id>/`

## Environment Variables

No environment variables required for basic setup. The app uses default configurations.

## CORS

CORS is enabled for `http://localhost:3000` (React frontend)
