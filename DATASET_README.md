# Training Datasets for Career Guidance System

This document describes the training datasets used for model training.

## Dataset Files

The training requires three main datasets:

### 1. `resumes_processed.csv`
**Purpose**: User profiles for content-based recommendations and career role classification

**Columns**:
- `id`: Unique user identifier
- `skills_cleaned`: List of skills (as Python list string)
- `experience_years`: Years of professional experience
- `current_role`: Current job role/title
- `target_role`: Target career role (same as current_role for training)
- `education`: List of education levels (e.g., ['bachelor'], ['master'])

**Sample Size**: 1000 profiles

### 2. `jobs_processed.csv`
**Purpose**: Job postings for content-based recommendations

**Columns**:
- `id`: Unique job identifier
- `title`: Job title
- `description`: Job description text
- `description_cleaned`: Cleaned description (lowercase)
- `skills_cleaned`: List of required skills (as Python list string)
- `location`: Job location (optional)

**Sample Size**: 500 job postings

### 3. `interactions_processed.csv`
**Purpose**: User-job interactions for collaborative filtering

**Columns**:
- `user_id`: User identifier (matches resumes id)
- `item_id`: Job identifier (matches jobs id)
- `rating`: Interaction rating (1-5 scale)

**Sample Size**: ~2000 interactions

## Using the Datasets

### Option 1: Use Pre-generated Datasets

1. Download `training_datasets.zip` from the notebook output
2. Upload it to Google Colab
3. Extract it in the notebook (see Step 2 in the notebook)

### Option 2: Generate Datasets in Notebook

The notebook automatically creates sample datasets if `training_datasets.zip` is not found. Just run all cells sequentially.

## Dataset Format Notes

- **Skills**: Stored as Python list strings (e.g., `"['python', 'sql', 'machine learning']"`)
- **Education**: Stored as Python list strings (e.g., `"['bachelor', 'master']"`)
- **Ratings**: Integer values from 1-5 (1=dislike, 5=strongly like)

## Creating Your Own Datasets

If you want to use your own data:

1. **Resume Dataset**: Ensure columns match `resumes_processed.csv` format
2. **Job Dataset**: Ensure columns match `jobs_processed.csv` format  
3. **Interactions Dataset**: Ensure columns match `interactions_processed.csv` format

Place your CSV files in `data/processed/` directory before running the training cells.

## Dataset Statistics

When generated automatically:
- **Resumes**: 1000 samples across 16 different roles
- **Jobs**: 500 job postings across various tech roles
- **Interactions**: ~2000 user-job interactions

These sample sizes are sufficient for training all models, but larger datasets will improve model performance.



