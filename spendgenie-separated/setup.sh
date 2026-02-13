#!/bin/bash

echo "========================================"
echo "SpendGenie Setup Script (macOS/Linux)"
echo "========================================"
echo ""

echo "Step 1: Setting up Backend..."
cd backend

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "Backend setup complete!"
echo ""

cd ..

echo "Step 2: Setting up Frontend..."
cd frontend

echo "Installing Node dependencies..."
npm install

echo ""
echo "Frontend setup complete!"
echo ""

cd ..

echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To run the application:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm start"
echo ""
echo "Then open http://localhost:3000 in your browser"
echo "========================================"
