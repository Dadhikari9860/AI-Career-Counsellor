# Career Guidance and Job Recommendation System

A comprehensive AI-powered career guidance system that provides personalized job recommendations, skill gap analysis, learning paths, and an intelligent chatbot using machine learning algorithms.

## 🚀 Quick Start

### Option 1: Using Startup Scripts (Easiest)

**Terminal 1 - Backend:**

```bash
./start_backend.sh
```

**Terminal 2 - Frontend:**

```bash
./start_frontend.sh
```

**Then open:** http://localhost:3001

### Option 2: Manual Start

**Terminal 1 - Backend:**

```bash
cd backend
source venv/bin/activate
python run.py
```

**Terminal 2 - Frontend:**

```bash
cd frontend
npm run dev
```

**Then open:** http://localhost:3001

📖 **For detailed setup instructions, see [HOW_TO_RUN.md](HOW_TO_RUN.md)**

## Features

### Core Features

- **Hybrid Recommendation System**: Combines content-based filtering, collaborative filtering (SVD), and supervised classification
- **Skill Gap Analysis**: Identifies missing skills and suggests learning resources
- **Intelligent Chatbot**: Intent-driven chatbot for career advice and recommendations
- **User Profile Management**: Track skills, experience, education, and career goals
- **Job Recommendations**: Personalized job postings based on user profile
- **Career Role Recommendations**: AI-powered career path suggestions

### Unique Features

- **Career Path Simulator**: Visualize progression from current role to target role with time estimates
- **Micro-Quiz Skill Verification**: Interactive quizzes to verify and update skill proficiency
- **Trust & Transparency Panel**: Explains why recommendations are made using feature importance

## Tech Stack

### Backend

- **Framework**: Flask (Python 3)
- **Database**: PostgreSQL (SQLite for development)
- **ML Libraries**:
  - scikit-learn (TF-IDF, classifiers, SVD)
  - pandas, numpy
  - sentence-transformers (optional, for BERT embeddings)
  - surprise (collaborative filtering)
- **Authentication**: JWT (Flask-JWT-Extended)

### Frontend

- **Framework**: React with TypeScript
- **Build Tool**: Vite
- **Visualization**: Recharts
- **Routing**: React Router

## Project Structure

```
FinalYearProject/
├── backend/
│   ├── app/
│   │   ├── routes/          # API endpoints
│   │   ├── services/         # Business logic & ML services
│   │   ├── models.py         # Database models
│   │   └── __init__.py       # Flask app factory
│   ├── ml/
│   │   ├── training/         # ML training scripts
│   │   └── models/          # Saved trained models
│   ├── data/
│   │   ├── raw/              # Raw datasets
│   │   └── processed/       # Processed datasets
│   ├── config.py            # Configuration
│   ├── run.py               # Application entry point
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API services
│   │   ├── contexts/         # React contexts
│   │   └── types/           # TypeScript types
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

## Datasets

This system is designed to work with real, public datasets. You need to provide at least three types of datasets:

### 1. Resume/User Profile Dataset

- **Purpose**: User features, skill extraction, role mapping
- **Required Columns**: skills, experience, education, role/job_title
- **Sources**:
  - Kaggle: "Resume Dataset" (https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset)
  - Kaggle: "IT Jobs Market Analysis" (https://www.kaggle.com/datasets/asaniczka/it-jobs-market-analysis-2023)

### 2. Job Postings Dataset

- **Purpose**: Job/role content-based recommendation, skill gap analysis
- **Required Columns**: title, description, required_skills, location, salary_range
- **Sources**:
  - Kaggle: "Data Science Jobs" (https://www.kaggle.com/datasets/andrewmvd/data-science-jobs)
  - Kaggle: "Software Engineer Jobs" (https://www.kaggle.com/datasets/arshkon/linkedin-job-postings)

### 3. User-Job Interactions Dataset

- **Purpose**: Collaborative filtering, user preferences
- **Required Columns**: user_id, item_id/job_id, rating/interaction
- **Sources**:
  - Kaggle: "Job Recommendation Dataset" (https://www.kaggle.com/datasets/arindam235/startup-investments-crunchbase)
  - Create from user feedback in the system

### Dataset Setup

**Quick Download (Recommended):**

Use the automated download script:

```bash
cd backend
python scripts/download_datasets.py
```

**Note:** Requires Kaggle API setup. See `docs/DOWNLOAD_DATASETS.md` for detailed instructions.

**Manual Download:**

1. Download datasets from the sources above or use your own
2. Place CSV files in `backend/data/raw/` directory
3. See `DATASET_LINKS.md` for direct links to all datasets

**After Downloading:**

Run preprocessing script:

```bash
cd backend
python -m ml.training.data_preprocessing
```

## Installation & Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL (optional, SQLite works for development)
- pip and npm

### Backend Setup

1. Navigate to backend directory:

   ```bash
   cd backend
   ```

2. Create virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Initialize database:

   ```bash
   python -c "from app import create_app, db; from config import Config; app = create_app(Config); app.app_context().push(); db.create_all()"
   ```

6. (Optional) Seed database with sample data:

   ```bash
   python scripts/seed_data.py
   ```

7. Train ML models:

   ```bash
   python -m ml.training.train_all
   ```

8. Run the backend server:
   ```bash
   python run.py
   ```
   Backend will run on http://localhost:5000

### Frontend Setup

1. Navigate to frontend directory:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Run development server:
   ```bash
   npm run dev
   ```
   Frontend will run on http://localhost:3000

## Usage

### Training Models

To train all ML models:

```bash
cd backend
python -m ml.training.train_all
```

To train individual models:

```bash
# Content-based recommendation
python -m ml.training.train_content_based

# Collaborative filtering
python -m ml.training.train_collaborative_filtering

# Career role classifier
python -m ml.training.train_classifier

# Chatbot intent classifier
python -m ml.training.train_chatbot_intent
```

### API Endpoints

#### Authentication

- `POST /api/register` - Register new user
- `POST /api/login` - Login user
- `GET /api/me` - Get current user (requires auth)

#### Recommendations

- `GET /api/recommendations` - Get hybrid recommendations (requires auth)
- `GET /api/skill-gap?target_role=<role>` - Get skill gap analysis (requires auth)
- `GET /api/learning-path?target_role=<role>` - Get learning path (requires auth)

#### Chatbot

- `POST /api/chat` - Chat with AI assistant (requires auth)

#### Profile

- `GET /api/profile` - Get user profile (requires auth)
- `PUT /api/profile` - Update user profile (requires auth)

#### Analytics & Unique Features

- `GET /api/career-path-simulator?target_role=<role>` - Get career path (requires auth)
- `GET /api/trust-panel?target_role=<role>` - Get trust panel (requires auth)
- `POST /api/quiz/submit` - Submit quiz results (requires auth)

#### Feedback

- `POST /api/feedback` - Submit feedback on recommendations (requires auth)

## ML Models

### 1. Content-Based Recommendation

- **Algorithm**: TF-IDF vectorization + Cosine similarity
- **Optional**: Sentence-BERT for semantic similarity
- **Input**: User skills, experience, interests
- **Output**: Similar jobs and roles

### 2. Collaborative Filtering

- **Algorithm**: SVD (Singular Value Decomposition)
- **Input**: User-item interaction matrix
- **Output**: Personalized recommendations based on similar users

### 3. Career Role Classifier

- **Algorithm**: Random Forest / Decision Tree
- **Input**: User features (skills, experience, education)
- **Output**: Predicted suitable career roles with probabilities
- **Metrics**: Accuracy, Precision, Recall, F1-Score

### 4. Chatbot Intent Classifier

- **Algorithm**: TF-IDF + Logistic Regression
- **Intents**: career_advice, job_search, skill_gap, learning_path, recommendation_explanation, general_info
- **Output**: Intent classification with confidence scores

### Hybrid Recommendation

Combines all three models with weighted scoring:

- Content-based: 40% weight
- Classifier: 60% weight
- Collaborative filtering: Used when user interactions available

## Evaluation

The system evaluates models using:

- **Accuracy**: Overall correctness
- **Precision**: Relevant recommendations
- **Recall**: Coverage of relevant items
- **F1-Score**: Harmonic mean of precision and recall

## Development

### Running Tests

```bash
cd backend
pytest tests/
```

### Code Structure

- Backend follows Flask application factory pattern
- Frontend uses React hooks and context for state management
- ML models are trained separately and loaded at runtime
- API follows RESTful conventions

## Troubleshooting

### Common Issues

1. **Models not found**: Run training scripts first
2. **Database errors**: Ensure database is initialized and migrations are run
3. **CORS errors**: Check CORS_ORIGINS in backend config
4. **Import errors**: Ensure virtual environment is activated

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is for educational purposes.

## Acknowledgments

- Datasets from Kaggle and other public sources
- ML libraries: scikit-learn, transformers, surprise
- Frontend: React, Vite, Recharts

## Contact

For questions or issues, please open an issue in the repository.
