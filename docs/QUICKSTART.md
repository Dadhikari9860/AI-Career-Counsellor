# Quick Start Guide

Get the Career Guidance System up and running in 5 minutes!

## Prerequisites Check

- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed
- [ ] pip and npm available

## Quick Setup

### 1. Backend Setup (2 minutes)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -c "from app import create_app, db; from config import Config; app = create_app(Config); app.app_context().push(); db.create_all()"
python scripts/seed_data.py
python -m ml.training.train_all
python run.py
```

Backend should now be running on http://localhost:5000

### 2. Frontend Setup (1 minute)

In a new terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend should now be running on http://localhost:3000

### 3. Access the Application

1. Open http://localhost:3000 in your browser
2. Click "Register" to create an account
3. Fill in your profile (skills, experience, target role)
4. Explore the dashboard, chatbot, and unique features!

## Using Real Datasets (Optional)

If you want to use real datasets instead of sample data:

1. Download datasets (see DATASETS.md for sources)
2. Place CSV files in `backend/data/raw/`
3. Run preprocessing: `python -m ml.training.data_preprocessing`
4. Retrain models: `python -m ml.training.train_all`

## Troubleshooting

**Backend won't start?**

- Check if port 5000 is available
- Ensure virtual environment is activated
- Check database connection in .env

**Frontend won't start?**

- Check if port 3000 is available
- Run `npm install` again
- Clear node_modules and reinstall

**Models not found?**

- Run `python -m ml.training.train_all` to train models
- Check that `backend/ml/models/` directory exists

**API errors?**

- Ensure backend is running on port 5000
- Check CORS settings in backend/config.py
- Verify JWT token in browser localStorage

## Next Steps

- Read the full README.md for detailed documentation
- Check DATASETS.md for dataset information
- Explore the API endpoints in the code
- Customize the models and features for your needs

Happy coding! 🚀
