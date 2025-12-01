#!/bin/bash

# Frontend Startup Script
echo "🎨 Starting Career Guidance Frontend..."
echo ""

# Navigate to frontend directory
cd "$(dirname "$0")/frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📥 Installing Node.js dependencies..."
    npm install
fi

# Start the development server
echo ""
echo "✅ Starting Vite dev server..."
echo "   Frontend will be available at http://localhost:3001"
echo "   Press Ctrl+C to stop"
echo ""
npm run dev

