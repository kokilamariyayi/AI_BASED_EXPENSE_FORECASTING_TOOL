# SpendGenie Frontend (React)

This is the frontend application for SpendGenie expense tracker.

## Setup Instructions

### 1. Install Node.js

Make sure you have Node.js installed (v14 or higher recommended)
Download from: https://nodejs.org/

### 2. Install Dependencies

```bash
# Navigate to frontend folder
cd frontend

# Install all dependencies
npm install
```

### 3. Run the Development Server

```bash
npm start
```

The frontend will start on `http://localhost:3000`

**Note:** Make sure the backend server is running on `http://localhost:5000` before starting the frontend.

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm build` - Builds the app for production
- `npm test` - Runs the test suite

## Features

- **Authentication** - Login and register functionality
- **Dashboard** - Overview of all features
- **Upload** - Upload CSV files with expense data
- **Analytics** - View detailed charts and statistics
- **AI Chat** - Chat with AI assistant for insights and tips

## Technology Stack

- React 18
- React Router v6
- Axios for API calls
- Recharts for data visualization
- CSS3 for styling

## Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Login.js
│   │   ├── Register.js
│   │   ├── Dashboard.js
│   │   ├── Upload.js
│   │   ├── Analytics.js
│   │   └── Chat.js
│   ├── App.js
│   ├── App.css
│   ├── index.js
│   └── index.css
└── package.json
```

## API Integration

The app connects to the Flask backend running on `http://localhost:5000`

All API endpoints are prefixed with `/api/`

## Environment

The app uses a proxy configuration to connect to the backend server.
This is configured in `package.json`:

```json
"proxy": "http://localhost:5000"
```
