# Dataset Download Links - Quick Reference

This file contains direct links to all datasets used in the Career Guidance System.

## 📥 Direct Download Links

### 1. Resume/User Profile Datasets

#### Resume Dataset

- **Kaggle URL:** https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset
- **Description:** Contains resume data with skills, experience, and job titles
- **Size:** ~1000+ resumes
- **Format:** CSV
- **Save Location:** `backend/data/raw/resume-dataset/`

#### IT Jobs Market Analysis 2023

- **Kaggle URL:** https://www.kaggle.com/datasets/asaniczka/it-jobs-market-analysis-2023
- **Description:** IT job market data with skills and roles
- **Size:** ~5000+ entries
- **Format:** CSV
- **Save Location:** `backend/data/raw/it-jobs-market/`

### 2. Job Postings Datasets

#### Data Science Jobs

- **Kaggle URL:** https://www.kaggle.com/datasets/andrewmvd/data-science-jobs
- **Description:** Data science job postings with descriptions and requirements
- **Size:** ~2000+ jobs
- **Format:** CSV
- **Save Location:** `backend/data/raw/data-science-jobs/`

#### LinkedIn Job Postings

- **Kaggle URL:** https://www.kaggle.com/datasets/arshkon/linkedin-job-postings
- **Description:** Software engineering and tech job postings from LinkedIn
- **Size:** ~5000+ jobs
- **Format:** CSV
- **Save Location:** `backend/data/raw/linkedin-job-postings/`

### 3. User-Job Interactions (Optional)

#### Job Recommendation Datasets

- **Search URL:** https://www.kaggle.com/datasets/search?search=job+recommendation
- **Description:** Datasets with user-job interactions (user_id, job_id, rating)
- **Save Location:** `backend/data/raw/interactions/`

## 🚀 Quick Download Instructions

### Method 1: Using the Download Script

```bash
cd backend
python scripts/download_datasets.py
```

**Note:** Requires Kaggle API setup. See `docs/DOWNLOAD_DATASETS.md` for details.

### Method 2: Manual Download

1. Visit each Kaggle URL above
2. Click "Download" (requires free Kaggle account)
3. Extract ZIP files
4. Copy CSV files to the appropriate directories in `backend/data/raw/`

## 📋 Required Columns

### Resume Dataset

- `skills` or `skills_cleaned` - List of skills
- `experience` or `experience_years` - Years of experience
- `education` - Education background
- `role` or `job_title` - Current or target role

### Job Postings Dataset

- `title` or `job_title` - Job title
- `description` - Job description
- `required_skills` or `skills` - Required skills
- `location` - Job location (optional)

### Interactions Dataset (Optional)

- `user_id` - User identifier
- `item_id` or `job_id` - Job/role identifier
- `rating` or `interaction` - Rating (1-5) or interaction type

## ✅ After Downloading

1. **Verify files are in correct locations:**

   ```bash
   ls -la backend/data/raw/*/
   ```

2. **Preprocess the data:**

   ```bash
   cd backend
   python -m ml.training.data_preprocessing
   ```

3. **Train all models:**
   ```bash
   python -m ml.training.train_all
   ```

## 📝 Notes

- All datasets require a free Kaggle account to download
- Some datasets may require accepting terms and conditions on Kaggle
- The system can work with sample data if real datasets are not available
- Minimum recommended: At least one resume dataset and one job postings dataset

## 🔗 Additional Resources

- **Full Download Guide:** `docs/DOWNLOAD_DATASETS.md`
- **Dataset Documentation:** `docs/DATASETS.md`
- **Preprocessing Script:** `backend/ml/training/data_preprocessing.py`
