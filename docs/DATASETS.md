# Dataset Information

This document describes the datasets used in the Career Guidance and Job Recommendation System.

## Required Datasets

The system requires three types of datasets to function properly:

### 1. Resume/User Profile Dataset

**Purpose**: Extract user features, skills, and map to career roles

**Required Columns**:

- `skills` or `skills_cleaned`: List of skills
- `experience` or `experience_years`: Years of experience
- `education`: Education background
- `role` or `job_title`: Current or target role

**Recommended Sources**:

1. **Kaggle - Resume Dataset**

   - URL: https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset
   - Description: Contains resume data with skills, experience, and job titles
   - Size: ~1000+ resumes
   - Format: CSV

2. **Kaggle - IT Jobs Market Analysis**
   - URL: https://www.kaggle.com/datasets/asaniczka/it-jobs-market-analysis-2023
   - Description: IT job market data with skills and roles
   - Size: ~5000+ entries
   - Format: CSV

**Usage in System**:

- User feature extraction for content-based recommendations
- Training the career role classifier
- Skill extraction and normalization

### 2. Job Postings Dataset

**Purpose**: Job/role content-based recommendation and skill gap analysis

**Required Columns**:

- `title` or `job_title`: Job title
- `description`: Job description
- `required_skills` or `skills`: Required skills
- `location`: Job location (optional)
- `salary_range`: Salary information (optional)

**Recommended Sources**:

1. **Kaggle - Data Science Jobs**

   - URL: https://www.kaggle.com/datasets/andrewmvd/data-science-jobs
   - Description: Data science job postings with descriptions and requirements
   - Size: ~2000+ jobs
   - Format: CSV

2. **Kaggle - LinkedIn Job Postings**
   - URL: https://www.kaggle.com/datasets/arshkon/linkedin-job-postings
   - Description: Software engineering and tech job postings
   - Size: ~5000+ jobs
   - Format: CSV

**Usage in System**:

- Content-based job recommendations
- Skill requirement extraction for gap analysis
- Job matching based on user profile

### 3. User-Job Interactions Dataset

**Purpose**: Collaborative filtering and learning user preferences

**Required Columns**:

- `user_id`: User identifier
- `item_id` or `job_id`: Job/role identifier
- `rating` or `interaction`: Rating (1-5) or interaction type (click, save, apply)

**Recommended Sources**:

1. **Create from System Feedback**

   - The system collects user feedback on recommendations
   - Feedback is stored in the `Feedback` table
   - Can be exported and used for retraining

2. **Kaggle - Job Recommendation Dataset**
   - Search for job recommendation datasets with user interactions
   - Format: CSV with user_id, job_id, rating columns

**Usage in System**:

- Training SVD collaborative filtering model
- Personalizing recommendations based on similar users
- Improving recommendation accuracy over time

## Dataset Preprocessing

All datasets go through preprocessing before use:

1. **Data Cleaning**:

   - Remove duplicates
   - Handle missing values
   - Standardize formats

2. **Skill Normalization**:

   - Extract skills from text
   - Normalize skill names (e.g., "Python" → "python")
   - Remove duplicates

3. **Feature Engineering**:
   - Extract experience years from text
   - Normalize role titles
   - Create interaction matrices

## Data Storage

- **Raw Data**: Stored in `backend/data/raw/`
- **Processed Data**: Stored in `backend/data/processed/`
- **Database**: User data, jobs, roles stored in PostgreSQL/SQLite

## Privacy and Ethics

- All datasets should be publicly available or properly licensed
- User data in the system is stored securely
- No personal information is shared without consent
- Datasets used for training should not contain personally identifiable information

## Adding New Datasets

To add a new dataset:

1. Download the dataset
2. Place CSV file in `backend/data/raw/`
3. Update `data_preprocessing.py` if needed for new format
4. Run preprocessing: `python -m ml.training.data_preprocessing`
5. Retrain models: `python -m ml.training.train_all`

## Dataset Quality Guidelines

- **Minimum Size**: At least 100 samples per dataset type
- **Data Quality**: Clean, consistent formatting
- **Relevance**: Data should be relevant to career guidance domain
- **Diversity**: Include various roles, skills, and experience levels
- **Currency**: Prefer recent datasets (within 2-3 years)

## Notes

- The system can work with sample data if real datasets are not available
- Training scripts will generate sample data if datasets are missing
- For production use, always use real, validated datasets
- Regularly update datasets to maintain recommendation quality
