# Career Guidance and Job Recommendation System

## Complete Project Report

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [System Architecture](#2-system-architecture)
3. [Machine Learning Algorithms](#3-machine-learning-algorithms)
4. [Datasets](#4-datasets)
5. [Training Process](#5-training-process)
6. [System Features](#6-system-features)
7. [Technical Implementation](#7-technical-implementation)
8. [Evaluation Metrics](#8-evaluation-metrics)
9. [How It Works](#9-how-it-works)
10. [Future Enhancements](#10-future-enhancements)

---

## 1. Project Overview

### 1.1 Project Description

The **Career Guidance and Job Recommendation System** is an AI-powered web application designed to provide personalized career guidance, job recommendations, skill gap analysis, and learning paths for users. The system leverages multiple machine learning algorithms to deliver intelligent, data-driven recommendations tailored to each user's profile, skills, and career goals.

### 1.2 Objectives

- **Personalized Recommendations**: Provide job and career role recommendations based on user profile
- **Skill Gap Analysis**: Identify missing skills required for target roles
- **Learning Path Generation**: Create structured week-by-week learning roadmaps
- **Intelligent Chatbot**: Natural language interface for career guidance
- **Resume Analysis**: Extract skills, experience, and location from uploaded resumes
- **Location-Based Job Matching**: Filter and recommend jobs based on user location

### 1.3 Key Features

1. **Hybrid Recommendation System**: Combines content-based, collaborative filtering, and classification
2. **Resume Parser**: Extracts skills, experience, education, and location from PDF/DOCX resumes
3. **LinkedIn Integration**: Generates LinkedIn profile and job search links
4. **Learning Roadmap Generator**: Creates structured week-by-week study plans
5. **Career Path Simulator**: Visualizes progression from current to target role
6. **Skill Verification Quiz**: Interactive quizzes to verify skill proficiency
7. **Trust & Transparency Panel**: Explains recommendation reasoning

---

## 2. System Architecture

### 2.1 Overall Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React/TypeScript)              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │Dashboard │  │ Chatbot │  │ Profile │  │ Roadmap │     │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTP/REST API
┌───────────────────────▼─────────────────────────────────────┐
│              Backend API (Flask/Python)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Routes     │  │   Services   │  │   Models     │     │
│  │  (Endpoints) │  │  (Business   │  │  (Database)  │     │
│  │              │  │   Logic)     │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│              ML Service Layer                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Content-    │  │ Collaborative│  │  Classifier │     │
│  │  Based       │  │  Filtering   │  │             │     │
│  │  (TF-IDF)    │  │  (SVD)       │  │ (Random     │     │
│  │              │  │              │  │  Forest)    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│              Database (PostgreSQL/SQLite)                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │  Users   │  │   Jobs   │  │  Roles   │  │Feedback  │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Technology Stack

#### Backend

- **Framework**: Flask (Python 3.8+)
- **Database**: PostgreSQL (production) / SQLite (development)
- **ORM**: SQLAlchemy
- **Authentication**: JWT (Flask-JWT-Extended)
- **ML Libraries**:
  - scikit-learn (TF-IDF, classifiers, SVD)
  - pandas, numpy (data processing)
  - sentence-transformers (optional, for BERT embeddings)
  - surprise (collaborative filtering)
- **File Processing**: PyPDF2, pdfplumber, python-docx

#### Frontend

- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Routing**: React Router v6
- **Visualization**: Recharts
- **State Management**: React Context API
- **HTTP Client**: Axios

---

## 3. Machine Learning Algorithms

### 3.1 Content-Based Recommendation System

#### Algorithm: TF-IDF Vectorization + Cosine Similarity

**Purpose**: Recommend jobs and roles based on user's skills, experience, and interests

**How It Works**:

1. **Feature Extraction**:

   - Combines user features (skills, experience, role, interests) into text
   - Uses TF-IDF (Term Frequency-Inverse Document Frequency) to vectorize text
   - Creates feature vectors for users, jobs, and roles

2. **Vectorization**:

   ```python
   TF-IDF Parameters:
   - max_features: 5000 (top 5000 most important terms)
   - ngram_range: (1, 2) (unigrams and bigrams)
   - stop_words: 'english' (removes common words)
   - min_df: 2 (term must appear in at least 2 documents)
   - max_df: 0.95 (term appears in max 95% of documents)
   ```

3. **Similarity Calculation**:

   - Uses Cosine Similarity to find similar users/jobs/roles
   - Formula: `cos(θ) = (A · B) / (||A|| × ||B||)`
   - Returns similarity scores between 0 and 1

4. **Recommendation Generation**:
   - Computes similarity between user vector and all job/role vectors
   - Ranks by similarity score (highest first)
   - Returns top-k recommendations

**Advantages**:

- No cold start problem (works for new users)
- Explains recommendations (shows matched skills)
- Domain-specific (understands tech skills)

**Limitations**:

- Limited to content similarity
- May miss serendipitous recommendations

---

### 3.2 Collaborative Filtering

#### Algorithm: SVD (Singular Value Decomposition)

**Purpose**: Recommend based on similar users' preferences

**How It Works**:

1. **Interaction Matrix Creation**:

   - Creates user-item interaction matrix
   - Rows: Users, Columns: Jobs/Roles
   - Values: Ratings/interactions (1-5 scale)

2. **Matrix Factorization**:

   ```python
   SVD decomposes matrix: R = U × Σ × V^T
   Where:
   - R: Original user-item matrix (m × n)
   - U: User latent factors (m × k)
   - Σ: Singular values (k × k)
   - V: Item latent factors (n × k)
   - k: Number of latent factors (typically 50)
   ```

3. **Dimensionality Reduction**:

   - Reduces high-dimensional matrix to lower-dimensional space
   - Captures latent patterns in user preferences
   - Handles sparse data efficiently

4. **Prediction**:
   - Predicts ratings for unseen user-item pairs
   - Uses dot product of user and item latent factors
   - Formula: `predicted_rating = user_factor · item_factor`

**Implementation Options**:

- **Surprise Library**: Optimized SVD for recommendation systems
- **scikit-learn TruncatedSVD**: Alternative implementation

**Advantages**:

- Discovers hidden patterns
- Works well with user feedback
- Improves over time with more data

**Limitations**:

- Cold start problem (new users/items)
- Requires sufficient interaction data
- Less interpretable

---

### 3.3 Career Role Classifier

#### Algorithm: Random Forest Classifier

**Purpose**: Predict suitable career roles based on user profile

**How It Works**:

1. **Feature Engineering**:

   - **Skills**: One-hot encoding for 30+ common skills
   - **Experience**: Years of experience (numeric)
   - **Education**: Degree level (categorical)
   - **Skill Count**: Total number of skills
   - **Skill Categories**: Frontend, Backend, Data Science, DevOps, etc.

2. **Model Architecture**:

   ```python
   RandomForestClassifier Parameters:
   - n_estimators: 500 (number of decision trees)
   - max_depth: 50 (maximum tree depth)
   - min_samples_split: 3 (minimum samples to split)
   - min_samples_leaf: 3 (minimum samples in leaf)
   - class_weight: 'balanced' (handles class imbalance)
   - max_features: 'sqrt' (features per split)
   - bootstrap: True (bootstrap sampling)
   - oob_score: True (out-of-bag validation)
   ```

3. **Training Process**:

   - Splits data: 80% training, 20% testing
   - Trains ensemble of decision trees
   - Each tree votes on class prediction
   - Final prediction: majority vote
   - Returns probabilities for each role

4. **Prediction**:
   - Input: User feature vector
   - Output: Predicted role with probability scores
   - Returns top-k roles sorted by probability

**Advantages**:

- Handles non-linear relationships
- Feature importance analysis
- Robust to overfitting
- Works with mixed data types

**Alternative**: Decision Tree (simpler, faster, but less accurate)

---

### 3.4 Chatbot Intent Classifier

#### Algorithm: TF-IDF + Logistic Regression

**Purpose**: Classify user queries into intents for appropriate responses

**How It Works**:

1. **Intent Categories**:

   - `career_advice`: Career recommendations
   - `job_search`: Job search requests
   - `skill_gap`: Skill gap analysis
   - `learning_path`: Learning resource requests
   - `recommendation_explanation`: Why recommendations were made
   - `general_info`: General questions

2. **Text Vectorization**:

   ```python
   TF-IDF Parameters:
   - max_features: 5000
   - ngram_range: (1, 2) (captures word pairs)
   - stop_words: 'english'
   - min_df: 1
   - max_df: 0.9
   ```

3. **Classification Model**:

   ```python
   LogisticRegression Parameters:
   - max_iter: 2000
   - C: 1.0 (regularization strength)
   - solver: 'lbfgs' (optimization algorithm)
   - multi_class: 'multinomial' (for multi-class)
   ```

4. **Training Data**:
   - 50+ example queries per intent
   - Includes variations and synonyms
   - Handles typos and informal language

**Advantages**:

- Fast inference
- Interpretable (can see important words)
- Works well with limited training data
- Handles multiple intents

---

### 3.5 Hybrid Recommendation System

**Purpose**: Combines all models for better recommendations

**How It Works**:

1. **Weighted Combination**:

   ```python
   Final Score = (Content-Based × 0.4) + (Classifier × 0.6)

   If collaborative filtering available:
   Final Score = (Content-Based × 0.3) +
                 (Classifier × 0.5) +
                 (Collaborative × 0.2)
   ```

2. **Score Normalization**:

   - Normalizes scores from all models to 0-1 range
   - Combines using weighted average
   - Ranks final recommendations

3. **Deduplication**:
   - Removes duplicate recommendations
   - Keeps highest-scoring instance
   - Ensures diversity

**Advantages**:

- Best of all approaches
- Handles different scenarios
- More robust and accurate
- Balances precision and recall

---

## 4. Datasets

### 4.1 Dataset Sources

#### 4.1.1 Resume/User Profile Dataset

**Primary Sources**:

1. **Kaggle - Resume Dataset**

   - **URL**: https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset
   - **Size**: ~1000+ resumes
   - **Format**: CSV
   - **Columns**: skills, experience, education, role/job_title
   - **Purpose**: User feature extraction, role mapping, skill normalization

2. **Kaggle - IT Jobs Market Analysis 2023**
   - **URL**: https://www.kaggle.com/datasets/asaniczka/it-jobs-market-analysis-2023
   - **Size**: ~5000+ entries
   - **Format**: CSV
   - **Columns**: skills, roles, experience levels, salary
   - **Purpose**: IT-specific skill-role mappings, market trends

**Usage in System**:

- Training content-based recommender
- Training career role classifier
- Skill extraction and normalization
- User profile feature engineering

---

#### 4.1.2 Job Postings Dataset

**Primary Sources**:

1. **Kaggle - Data Science Jobs**

   - **URL**: https://www.kaggle.com/datasets/andrewmvd/data-science-jobs
   - **Size**: ~2000+ jobs
   - **Format**: CSV
   - **Columns**: title, description, required_skills, location, salary_range
   - **Purpose**: Data science job recommendations, skill requirements

2. **Kaggle - LinkedIn Job Postings**
   - **URL**: https://www.kaggle.com/datasets/arshkon/linkedin-job-postings
   - **Size**: ~5000+ jobs
   - **Format**: CSV
   - **Columns**: title, company, description, skills, location
   - **Purpose**: Software engineering job recommendations

**Usage in System**:

- Content-based job recommendations
- Skill requirement extraction
- Job matching based on user profile
- Location-based filtering

---

#### 4.1.3 User-Job Interactions Dataset

**Primary Sources**:

1. **System-Generated Interactions**

   - Created from user feedback in the system
   - Stored in `Feedback` database table
   - Includes: clicks, likes, saves, applications
   - **Format**: user_id, item_id, rating/interaction_type

2. **Kaggle - Job Recommendation Datasets**
   - Search: https://www.kaggle.com/datasets/search?search=job+recommendation
   - **Format**: CSV with user_id, job_id, rating columns
   - **Purpose**: Collaborative filtering training

**Usage in System**:

- Training SVD collaborative filtering model
- Learning user preferences
- Improving recommendation accuracy
- Personalization based on similar users

---

### 4.2 Dataset Structure

#### 4.2.1 Resume Dataset Structure

```csv
id,skills,experience,education,role,location
1,"python,java,sql",5,"Bachelor","Software Engineer","New York, NY"
2,"react,javascript,node.js",2,"Master","Frontend Developer","San Francisco, CA"
```

**Required Columns**:

- `skills` or `skills_cleaned`: Comma-separated list of skills
- `experience` or `experience_years`: Years of experience (numeric)
- `education`: Degree level (Bachelor, Master, PhD)
- `role` or `job_title`: Current or target role
- `location`: Geographic location (optional)

---

#### 4.2.2 Job Postings Dataset Structure

```csv
id,title,description,required_skills,location,company
1,"Senior Python Developer","We are looking for...","python,django,sql","Remote","Tech Corp"
2,"React Developer","Join our team...","react,javascript,typescript","New York, NY","Startup Inc"
```

**Required Columns**:

- `title` or `job_title`: Job title
- `description`: Job description text
- `required_skills` or `skills`: Required skills (comma-separated)
- `location`: Job location
- `company`: Company name (optional)
- `salary_range`: Salary information (optional)

---

#### 4.2.3 Interactions Dataset Structure

```csv
user_id,item_id,rating,interaction_type,timestamp
1,5,4,"like","2024-01-15 10:30:00"
1,12,5,"apply","2024-01-16 14:20:00"
2,5,3,"click","2024-01-17 09:15:00"
```

**Required Columns**:

- `user_id`: User identifier
- `item_id` or `job_id`: Job/role identifier
- `rating`: Numeric rating (1-5) or interaction score
- `interaction_type`: Type of interaction (click, save, apply, like)

---

### 4.3 Data Preprocessing

#### 4.3.1 Preprocessing Steps

1. **Data Cleaning**:

   - Remove duplicates
   - Handle missing values (fill with defaults or remove)
   - Standardize formats (dates, numbers, text)

2. **Skill Normalization**:

   ```python
   Process:
   - Convert to lowercase
   - Remove special characters
   - Handle variations (e.g., "JS" → "javascript")
   - Remove duplicates
   - Standardize skill names
   ```

3. **Feature Extraction**:

   - Extract experience years from text (e.g., "5 years" → 5)
   - Normalize role titles (e.g., "Software Engineer" → "software engineer")
   - Extract skills from descriptions using keyword matching
   - Categorize skills (Frontend, Backend, Data Science, etc.)

4. **Text Processing**:
   - Remove HTML tags
   - Remove extra whitespace
   - Lowercase conversion
   - Remove stop words (for TF-IDF)

---

### 4.4 Current Dataset Files

Based on the project structure, the system currently uses:

- `backend/data/raw/resumes_dataset.csv` (3002 rows)
- `backend/data/raw/jobs_dataset.csv` (1502 rows)
- `backend/data/raw/interactions_dataset.csv` (2988 rows)

These datasets are processed and stored in:

- `backend/data/processed/resumes_processed.csv`
- `backend/data/processed/jobs_processed.csv`
- `backend/data/processed/interactions_processed.csv`

---

## 5. Training Process

### 5.1 Training Pipeline

The complete training process follows these steps:

```
1. Data Preprocessing
   ↓
2. Train Content-Based Model
   ↓
3. Train Collaborative Filtering Model
   ↓
4. Train Career Role Classifier
   ↓
5. Train Chatbot Intent Classifier
   ↓
6. Save All Models
```

### 5.2 Step-by-Step Training

#### Step 1: Data Preprocessing

**Script**: `backend/ml/training/data_preprocessing.py`

**Process**:

1. Load raw datasets from `backend/data/raw/`
2. Clean and normalize data
3. Extract features (skills, experience, etc.)
4. Save processed data to `backend/data/processed/`

**Output**:

- `resumes_processed.csv`
- `jobs_processed.csv`
- `interactions_processed.csv`
- `dataset_summary.json`

---

#### Step 2: Content-Based Model Training

**Script**: `backend/ml/training/train_content_based.py`

**Process**:

1. Load processed datasets
2. Create feature vectors for users, jobs, and roles
3. Apply TF-IDF vectorization
4. Compute and save vectors

**Output Files**:

- `user_vectors.npy` - User feature vectors
- `job_vectors.npy` - Job feature vectors
- `role_vectors.npy` - Role feature vectors
- `user_ids.npy`, `job_ids.npy`, `role_ids.npy` - ID mappings
- `tfidf_vectorizer.joblib` - TF-IDF vectorizer
- `content_based_metadata.json` - Model metadata

**Training Time**: ~2-5 minutes (depending on dataset size)

---

#### Step 3: Collaborative Filtering Training

**Script**: `backend/ml/training/train_collaborative_filtering.py`

**Process**:

1. Load interactions dataset
2. Create user-item interaction matrix
3. Apply SVD decomposition
4. Train model on interaction data

**Output Files**:

- `svd_model.joblib` - Trained SVD model
- `svd_user_mapping.json` - User ID mappings
- `svd_item_mapping.json` - Item ID mappings
- `interaction_matrix.npy` - Interaction matrix (if using sklearn)
- `svd_metadata.json` - Model metadata

**Parameters**:

- `n_components`: 50 (latent factors)
- `n_factors`: 50 (for Surprise library)

**Training Time**: ~1-3 minutes

---

#### Step 4: Career Role Classifier Training

**Script**: `backend/ml/training/train_classifier.py`

**Process**:

1. Load resume dataset
2. Extract features (skills, experience, education)
3. Encode labels (career roles)
4. Split data (80% train, 20% test)
5. Train Random Forest classifier
6. Evaluate model performance

**Output Files**:

- `classifier_model.joblib` - Trained classifier
- `label_encoder.joblib` - Role label encoder
- `skill_binarizer.joblib` - Skill binarizer
- `classifier_metadata.json` - Model metadata and metrics

**Evaluation Metrics**:

- Accuracy
- Precision (per class)
- Recall (per class)
- F1-Score (per class)
- Classification report

**Training Time**: ~3-10 minutes

---

#### Step 5: Chatbot Intent Classifier Training

**Script**: `backend/ml/training/train_chatbot_intent.py`

**Process**:

1. Create training data (50+ examples per intent)
2. Apply TF-IDF vectorization
3. Train Logistic Regression classifier
4. Evaluate on test set

**Output Files**:

- `intent_classifier.joblib` - Trained intent classifier
- `intent_vectorizer.joblib` - TF-IDF vectorizer
- `intent_metadata.json` - Model metadata

**Training Time**: ~1-2 minutes

---

### 5.3 Running Training

**Train All Models**:

```bash
cd backend
python -m ml.training.train_all
```

**Train Individual Models**:

```bash
# Content-based
python -m ml.training.train_content_based

# Collaborative filtering
python -m ml.training.train_collaborative_filtering

# Classifier
python -m ml.training.train_classifier

# Intent classifier
python -m ml.training.train_chatbot_intent
```

---

## 6. System Features

### 6.1 Core Features

#### 6.1.1 User Authentication & Profile Management

- **Registration**: Create account with email/password
- **Login**: JWT-based authentication
- **Profile Management**: Update skills, experience, education, location
- **Resume Upload**: Upload PDF/DOCX resumes for automatic parsing
- **Google OAuth**: Optional Google sign-in integration

#### 6.1.2 Job Recommendations

- **Personalized Recommendations**: Based on skills, experience, location
- **LinkedIn Integration**: Direct links to LinkedIn job postings
- **Location Filtering**: Jobs filtered by user's location
- **Skill-Based Matching**: Match score based on skill overlap
- **Real-Time Scraping**: Scrapes LinkedIn for latest job postings

#### 6.1.3 Career Role Recommendations

- **AI-Powered Suggestions**: ML-based role recommendations
- **Skill Gap Analysis**: Shows missing skills for target roles
- **Match Percentage**: Visual indicator of role fit
- **Role Details**: Description, required skills, salary, growth outlook

#### 6.1.4 Learning Resources

- **YouTube Integration**: Links to relevant tutorial videos
- **Skill-Specific Resources**: Resources for specific skills
- **Learning Roadmaps**: Week-by-week structured learning paths
- **Prerequisites**: Shows what to learn first

#### 6.1.5 Intelligent Chatbot

- **Natural Language Interface**: Chat-based interaction
- **Intent Recognition**: Understands user queries
- **Dynamic Responses**: Responds to specific skill requests
- **Learning Path Generation**: Creates roadmaps on demand
- **Context-Aware**: Uses user profile for personalized responses

---

### 6.2 Advanced Features

#### 6.2.1 Resume Parser

**Extracted Information**:

- Skills (30+ tech skills recognized)
- Experience years
- Education level
- Current role
- Location (city, state, country)
- Email and phone (optional)

**Supported Formats**:

- PDF (using PyPDF2 and pdfplumber)
- DOCX (using python-docx)
- TXT (plain text)

**Location Extraction**:

- Pattern matching for "Location:", "City, State" format
- Common city recognition
- Validation to avoid false positives

---

#### 6.2.2 Learning Roadmap Generator

**Features**:

- Week-by-week breakdown
- Beginner → Intermediate → Advanced progression
- Topic lists for each week
- Estimated hours per week
- Prerequisites identification
- Skill-specific roadmaps

**Supported Skills**:

- Database, SQL, Python, JavaScript, React
- Machine Learning, Data Science
- Node.js, Docker, AWS
- And 20+ more skills

---

#### 6.2.3 Career Path Simulator

**Features**:

- Visual progression path
- Time estimates for each level
- Required skills per level
- Current position tracking
- Skill match percentage

---

#### 6.2.4 Trust & Transparency Panel

**Features**:

- Feature importance analysis
- Explanation of recommendations
- Skill gap visualization
- Recommendation score breakdown

---

#### 6.2.5 Skill Verification Quiz

**Features**:

- Interactive quizzes for skills
- Multiple choice questions
- Score calculation
- Updates user profile based on results

---

## 7. Technical Implementation

### 7.1 Backend Architecture

#### 7.1.1 Flask Application Structure

```
backend/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models (SQLAlchemy)
│   ├── routes/              # API endpoints
│   │   ├── auth.py          # Authentication
│   │   ├── recommendations.py  # Recommendations API
│   │   ├── chatbot.py       # Chatbot API
│   │   ├── profile.py        # Profile management
│   │   ├── resume.py         # Resume upload/parsing
│   │   ├── analytics.py      # Analytics & roadmaps
│   │   └── roles.py          # Career roles
│   ├── services/            # Business logic
│   │   ├── ml_service.py    # ML inference
│   │   ├── job_scraper.py   # LinkedIn scraping
│   │   ├── resume_parser.py # Resume parsing
│   │   ├── youtube_learning_service.py  # YouTube resources
│   │   └── learning_roadmap_service.py  # Roadmap generation
│   └── utils/               # Utilities
│       ├── auth_helpers.py  # JWT helpers
│       └── role_helpers.py  # Role utilities
├── ml/
│   ├── training/            # Training scripts
│   └── models/             # Saved models
├── data/
│   ├── raw/                 # Raw datasets
│   └── processed/          # Processed datasets
└── config.py               # Configuration
```

---

#### 7.1.2 Database Models

**User Model**:

```python
- id: Integer (Primary Key)
- username: String (Unique)
- email: String (Unique)
- password_hash: String
- full_name: String
- location: String
- skills: JSON (List of skills)
- experience_years: Integer
- education: JSON
- interests: JSON
- current_role: String
- target_role: String
```

**Job Model**:

```python
- id: Integer (Primary Key)
- title: String
- company: String
- description: Text
- required_skills: JSON
- location: String
- salary_range: String
- job_type: String
```

**CareerRole Model**:

```python
- id: Integer (Primary Key)
- title: String (Unique)
- description: Text
- required_skills: JSON
- category: String
- average_salary: String
- growth_outlook: String
- typical_path: JSON
```

---

### 7.2 Frontend Architecture

#### 7.2.1 Component Structure

```
frontend/src/
├── components/
│   └── Navbar.tsx           # Navigation component
├── pages/
│   ├── Dashboard.tsx         # Main dashboard
│   ├── Chatbot.tsx           # Chatbot interface
│   ├── Profile.tsx           # Profile management
│   ├── CareerPathSimulator.tsx  # Career path
│   ├── Roadmap.tsx           # Learning roadmap
│   ├── TrustPanel.tsx        # Trust panel
│   └── Quiz.tsx              # Skill quiz
├── contexts/
│   └── AuthContext.tsx       # Authentication context
├── services/
│   └── api.ts               # API client
└── types/
    └── index.ts             # TypeScript types
```

---

### 7.3 API Endpoints

#### Authentication

- `POST /api/register` - User registration
- `POST /api/login` - User login
- `GET /api/me` - Get current user

#### Recommendations

- `GET /api/recommendations` - Hybrid recommendations
- `GET /api/skill-gap?target_role=<role>` - Skill gap analysis
- `GET /api/learning-path?target_role=<role>` - Learning path

#### Chatbot

- `POST /api/chat` - Chat with AI assistant

#### Profile

- `GET /api/profile` - Get user profile
- `PUT /api/profile` - Update profile

#### Resume

- `POST /api/resume/upload` - Upload and parse resume
- `POST /api/resume/analyze` - Analyze resume text

#### Analytics

- `GET /api/career-path-simulator?target_role=<role>` - Career path
- `GET /api/trust-panel?target_role=<role>` - Trust panel
- `GET /api/roadmap?skill=<skill>` - Learning roadmap
- `POST /api/quiz/submit` - Submit quiz results

---

## 8. Evaluation Metrics

### 8.1 Model Evaluation

#### 8.1.1 Career Role Classifier

**Metrics Used**:

- **Accuracy**: Overall correctness
  - Formula: `(TP + TN) / (TP + TN + FP + FN)`
- **Precision**: Relevant recommendations
  - Formula: `TP / (TP + FP)`
- **Recall**: Coverage of relevant items
  - Formula: `TP / (TP + FN)`
- **F1-Score**: Harmonic mean of precision and recall
  - Formula: `2 × (Precision × Recall) / (Precision + Recall)`

**Expected Performance**:

- Accuracy: 75-85%
- Precision: 70-80% (varies by class)
- Recall: 65-75% (varies by class)
- F1-Score: 70-80%

---

#### 8.1.2 Content-Based Recommendation

**Metrics**:

- **Cosine Similarity Score**: 0-1 range
- **Top-K Accuracy**: % of relevant items in top-k
- **Diversity**: Variety of recommendations

**Evaluation**:

- Similarity scores typically range from 0.3-0.9
- Higher scores indicate better matches
- Diversity ensures users see varied options

---

#### 8.1.3 Collaborative Filtering

**Metrics**:

- **RMSE** (Root Mean Squared Error): Prediction accuracy
  - Formula: `√(Σ(predicted - actual)² / n)`
- **MAE** (Mean Absolute Error): Average prediction error
- **Coverage**: % of items that can be recommended

**Expected Performance**:

- RMSE: 0.8-1.2 (on 1-5 rating scale)
- MAE: 0.6-1.0
- Coverage: 60-80%

---

#### 8.1.4 Chatbot Intent Classifier

**Metrics**:

- **Accuracy**: Overall intent classification accuracy
- **Per-Intent Precision/Recall**: Performance per intent
- **Confidence Scores**: Model certainty

**Expected Performance**:

- Accuracy: 85-95%
- High confidence (>0.8) for most queries
- Handles variations and typos well

---

## 9. How It Works

### 9.1 Complete User Flow

#### Scenario: User Uploads Resume and Gets Recommendations

1. **User Registration/Login**:

   - User creates account or logs in
   - JWT token stored in browser

2. **Resume Upload**:

   - User uploads PDF resume
   - Resume parser extracts:
     - Skills: ["python", "react", "javascript", "sql"]
     - Experience: 2 years
     - Education: "Master, Bachelor"
     - Current Role: "Software Engineer"
     - Location: "Kathmandu, Nepal"

3. **Profile Update**:

   - Extracted data saved to user profile
   - Location used for job filtering

4. **Job Recommendations**:

   - System generates user vector from skills
   - Searches LinkedIn with: "Software Engineer python react javascript" + "Kathmandu"
   - Scores jobs based on skill matches
   - Filters by location
   - Returns top 10 personalized jobs

5. **Career Role Recommendations**:

   - Classifier predicts suitable roles
   - Content-based finds similar roles
   - Hybrid system combines scores
   - Returns top roles with match percentages

6. **Learning Resources**:
   - Analyzes skill gap for target role
   - Generates week-by-week roadmap
   - Provides YouTube tutorial links
   - Shows prerequisites if needed

---

### 9.2 Recommendation Generation Process

```
User Profile
    ↓
Feature Extraction (Skills, Experience, Role)
    ↓
┌─────────────────────────────────────┐
│  Content-Based Model                │
│  - TF-IDF vectorization              │
│  - Cosine similarity with jobs/roles │
│  - Returns similarity scores         │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Classifier Model                    │
│  - Random Forest prediction          │
│  - Returns role probabilities       │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Collaborative Filtering (if data)  │
│  - SVD prediction                    │
│  - Returns user-based scores        │
└─────────────────────────────────────┘
    ↓
Hybrid Combination (Weighted Scores)
    ↓
Ranking & Deduplication
    ↓
Final Recommendations
```

---

### 9.3 Chatbot Query Processing

**Example: "show me learning resources for database"**

1. **Intent Classification**:

   - Query: "show me learning resources for database"
   - Intent: `learning_path` (confidence: 0.92)

2. **Skill Extraction**:

   - Extracted skill: "database"
   - Normalized: "database"

3. **Roadmap Generation**:

   - Generates 3-week roadmap for database
   - Week 1: Introduction, SQL basics
   - Week 2: JOINs, aggregate functions
   - Week 3: Database design, normalization

4. **Response**:
   - Returns structured roadmap
   - Includes prerequisites if needed
   - Provides YouTube resource links

---

### 9.4 Job Matching Algorithm

**Process**:

1. **User Skills Normalization**:

   ```python
   User Skills: ["React", "JavaScript", "Node.js"]
   Normalized: ["react", "javascript", "node.js"]
   ```

2. **Job Skill Extraction**:

   - From job title, description, required_skills
   - Normalized to lowercase

3. **Match Score Calculation**:

   ```python
   Exact Matches: 2 (react, javascript)
   Partial Matches: 1 (node.js appears as "node" in text)

   Job Match Ratio = (2 × 2.0 + 1 × 0.5) / (job_skills × 2.0)
   User Coverage = (2 + 1) / user_total_skills

   Final Score = (Job Match × 0.7) + (User Coverage × 0.3)
   ```

4. **Location Filtering**:

   - Filters jobs by user location
   - Partial matching (e.g., "Kathmandu" matches "Kathmandu, Nepal")

5. **Ranking**:
   - Sorted by match score (highest first)
   - LinkedIn jobs prioritized
   - Deduplication by title+company

---

## 10. Future Enhancements

### 10.1 Planned Improvements

1. **Advanced ML Models**:

   - Deep Learning for better recommendations
   - Transformer models (BERT) for semantic understanding
   - Reinforcement Learning for adaptive recommendations

2. **Enhanced Features**:

   - Salary prediction
   - Career progression timeline
   - Skill demand trends
   - Company culture matching

3. **Better Data Sources**:

   - Real-time job APIs
   - More diverse datasets
   - Industry-specific data

4. **Performance Optimization**:
   - Model caching
   - Faster inference
   - Batch processing

---

## Conclusion

This Career Guidance and Job Recommendation System is a comprehensive AI-powered platform that combines multiple machine learning algorithms to provide personalized career guidance. The system uses:

- **Content-Based Filtering** (TF-IDF) for skill-based matching
- **Collaborative Filtering** (SVD) for user preference learning
- **Supervised Classification** (Random Forest) for role prediction
- **Intent Classification** (Logistic Regression) for chatbot

All models are trained on real datasets from Kaggle and other public sources, ensuring realistic and relevant recommendations. The system is production-ready with proper error handling, authentication, and a modern user interface.

---

## References

### Dataset Sources

1. Kaggle Resume Dataset: https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset
2. Kaggle IT Jobs Market Analysis: https://www.kaggle.com/datasets/asaniczka/it-jobs-market-analysis-2023
3. Kaggle Data Science Jobs: https://www.kaggle.com/datasets/andrewmvd/data-science-jobs
4. Kaggle LinkedIn Job Postings: https://www.kaggle.com/datasets/arshkon/linkedin-job-postings

### ML Libraries

- scikit-learn: https://scikit-learn.org/
- Surprise: http://surpriselib.com/
- Sentence Transformers: https://www.sbert.net/

### Documentation

- Flask: https://flask.palletsprojects.com/
- React: https://react.dev/
- SQLAlchemy: https://www.sqlalchemy.org/

---

**Report Generated**: 2024
**Project Version**: 1.0
**Last Updated**: November 2024
