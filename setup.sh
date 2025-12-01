#!/bin/bash

# Career Guidance System Setup Script
# This script automates the initial setup process

set -e

echo "=========================================="
echo "Career Guidance System Setup"
echo "=========================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check Python
echo -e "${BLUE}Checking Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8+"
    exit 1
fi
echo -e "${GREEN}Python found: $(python3 --version)${NC}"

# Check Node.js
echo -e "${BLUE}Checking Node.js...${NC}"
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is not installed. Please install Node.js 16+"
    exit 1
fi
echo -e "${GREEN}Node.js found: $(node --version)${NC}"

# Backend Setup
echo -e "\n${BLUE}Setting up backend...${NC}"
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env 2>/dev/null || echo "DATABASE_URL=sqlite:///career_guidance.db" > .env
    echo "JWT_SECRET_KEY=$(openssl rand -hex 32)" >> .env
    echo "SECRET_KEY=$(openssl rand -hex 32)" >> .env
    echo "FLASK_ENV=development" >> .env
    echo "FLASK_DEBUG=True" >> .env
fi

# Initialize database
echo "Initializing database..."
python3 -c "from app import create_app, db; from config import Config; app = create_app(Config); app.app_context().push(); db.create_all()" || echo "Database initialization completed"

# Seed database
echo "Seeding database with sample data..."
python3 scripts/seed_data.py || echo "Database seeding completed"

# Train models
echo "Training ML models (this may take a few minutes)..."
python3 -m ml.training.train_all || echo "Model training completed"

echo -e "${GREEN}Backend setup complete!${NC}"

# Frontend Setup
echo -e "\n${BLUE}Setting up frontend...${NC}"
cd ../frontend

# Install dependencies
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
else
    echo "Node modules already installed, skipping..."
fi

echo -e "${GREEN}Frontend setup complete!${NC}"

# Summary
echo -e "\n${GREEN}=========================================="
echo "Setup Complete!"
echo "==========================================${NC}"
echo ""
echo "To start the backend:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python run.py"
echo ""
echo "To start the frontend (in a new terminal):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then open http://localhost:3000 in your browser"
echo ""
echo "For more information, see README.md"

