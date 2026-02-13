# 🚀 QUICK START GUIDE

## Prerequisites
- Python 3.8+ installed
- Node.js 14+ installed
- npm installed

## Option 1: Automated Setup

### Windows
```bash
# Double-click setup.bat
# OR run in command prompt:
setup.bat
```

### macOS/Linux
```bash
chmod +x setup.sh
./setup.sh
```

## Option 2: Manual Setup

### Backend Setup (Terminal 1)
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python app.py
```

Backend runs on: http://localhost:5000

### Frontend Setup (Terminal 2)
```bash
cd frontend
npm install
npm start
```

Frontend opens automatically at: http://localhost:3000

## First Time Usage

1. **Register Account**
   - Open http://localhost:3000
   - Click "Register here"
   - Create your account

2. **Upload CSV**
   - Navigate to "Upload Data"
   - Upload expense CSV file
   - Required: date and amount columns

3. **View Analytics**
   - Go to "Analytics" tab
   - See charts and insights

4. **Chat with AI**
   - Go to "AI Chat" tab
   - Ask questions about expenses

## Sample CSV Format

Create a file named `expenses.csv`:

```csv
date,amount,category,description
2024-01-15,500,Food,Grocery shopping
2024-01-16,1200,Transport,Fuel
2024-01-17,300,Entertainment,Movie tickets
2024-01-18,2000,Shopping,Clothes
2024-01-19,150,Food,Restaurant
```

## Troubleshooting

**Backend won't start:**
- Check if port 5000 is available
- Ensure virtual environment is activated
- Verify all dependencies installed

**Frontend won't start:**
- Check if port 3000 is available
- Delete node_modules and run `npm install` again
- Ensure backend is running first

**Can't upload CSV:**
- Check CSV has date and amount columns
- Ensure file is .csv format
- Check file isn't corrupted

## Support

For detailed documentation, see:
- Main README.md
- backend/README.md
- frontend/README.md

## Next Steps

After setup:
1. Explore the dashboard
2. Try uploading your own expense data
3. Ask the AI assistant questions
4. Check analytics with different filters

Happy tracking! 🧞✨
