# Dataset Download Guide

This guide explains how to download all datasets used in the Career Guidance and Job Recommendation System.

## Quick Start

### Option 1: Automatic Download (Requires Kaggle API)

1. **Install Kaggle package:**

   ```bash
   pip install kaggle
   ```

2. **Get Kaggle API credentials:**

   - Go to https://www.kaggle.com/account
   - Scroll to "API" section
   - Click "Create New API Token"
   - This downloads `kaggle.json`

3. **Set up credentials:**

   ```bash
   mkdir -p ~/.kaggle
   # Move kaggle.json to ~/.kaggle/kaggle.json
   chmod 600 ~/.kaggle/kaggle.json
   ```

4. **Run download script:**
   ```bash
   cd backend
   python scripts/download_datasets.py
   ```

### Option 2: Manual Download

Download datasets manually from the links below and place them in `backend/data/raw/`.

## Required Datasets

### 1. Resume/User Profile Dataset

**Purpose:** Extract user features, skills, and map to career roles

**Required Files:**

- CSV files with columns: `skills`, `experience`, `education`, `role` (or `job_title`)

**Download Sources:**

1. **Resume Dataset**

   - **URL:** https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset
   - **Size:** ~1000+ resumes
   - **Format:** CSV
   - **Save to:** `backend/data/raw/resume-dataset/`

2. **IT Jobs Market Analysis**
   - **URL:** https://www.kaggle.com/datasets/asaniczka/it-jobs-market-analysis-2023
   - **Size:** ~5000+ entries
   - **Format:** CSV
   - **Save to:** `backend/data/raw/it-jobs-market/`

**Manual Download Steps:**

1. Visit the Kaggle dataset page
2. Click "Download" button (requires Kaggle account)
3. Extract the ZIP file
4. Copy CSV files to `backend/data/raw/resume-dataset/` or `backend/data/raw/it-jobs-market/`

### 2. Job Postings Dataset

**Purpose:** Job/role content-based recommendation and skill gap analysis

**Required Files:**

- CSV files with columns: `title` (or `job_title`), `description`, `required_skills` (or `skills`), `location`

**Download Sources:**

1. **Data Science Jobs**

   - **URL:** https://www.kaggle.com/datasets/andrewmvd/data-science-jobs
   - **Size:** ~2000+ jobs
   - **Format:** CSV
   - **Save to:** `backend/data/raw/data-science-jobs/`

2. **LinkedIn Job Postings**
   - **URL:** https://www.kaggle.com/datasets/arshkon/linkedin-job-postings
   - **Size:** ~5000+ jobs
   - **Format:** CSV
   - **Save to:** `backend/data/raw/linkedin-job-postings/`

**Manual Download Steps:**

1. Visit the Kaggle dataset page
2. Click "Download" button
3. Extract the ZIP file
4. Copy CSV files to the appropriate directory

### 3. User-Job Interactions Dataset

**Purpose:** Collaborative filtering and learning user preferences

**Note:** This dataset is optional. The system can create interaction data from:

- User feedback stored in the database
- System-generated sample interactions

**If you want to download external interaction data:**

- Search Kaggle for "job recommendation" datasets
- Look for datasets with `user_id`, `job_id`, `rating` columns
- **Save to:** `backend/data/raw/interactions/`

## Directory Structure

After downloading, your `backend/data/raw/` directory should look like:

```
backend/data/raw/
├── resume-dataset/
│   ├── Resume.csv
│   └── ...
├── it-jobs-market/
│   ├── it_jobs_market_2023.csv
│   └── ...
├── data-science-jobs/
│   ├── DataScience.csv
│   └── ...
├── linkedin-job-postings/
│   ├── jobs.csv
│   └── ...
└── interactions/  (optional)
    └── interactions.csv
```

## After Downloading

1. **Preprocess the data:**

   ```bash
   cd backend
   python -m ml.training.data_preprocessing
   ```

2. **Train all models:**
   ```bash
   python -m ml.training.train_all
   ```

## Alternative Data Sources

If Kaggle datasets are unavailable, you can use:

1. **GitHub Repositories:**

   - Search for "resume dataset" or "job postings dataset"
   - Many repositories have CSV files available

2. **UCI Machine Learning Repository:**

   - URL: https://archive.ics.uci.edu/
   - Search for relevant datasets

3. **Data.gov:**

   - URL: https://data.gov/
   - Government job postings and employment data

4. **Sample Data (for testing):**
   - The system can generate sample data if real datasets are missing
   - Run training scripts without datasets to use sample data

## Troubleshooting

### Kaggle API Issues

**Error: "Could not find kaggle.json"**

- Make sure `kaggle.json` is in `~/.kaggle/` or `~/.config/kaggle/`
- Check file permissions: `chmod 600 ~/.kaggle/kaggle.json`

**Error: "403 Forbidden"**

- Your Kaggle API token may be expired
- Generate a new token from https://www.kaggle.com/account

**Error: "Dataset not found"**

- Check if the dataset URL is correct
- Some datasets may require acceptance of terms
- Visit the dataset page and click "I Understand and Accept"

### File Format Issues

**CSV files not found:**

- Make sure CSV files are directly in the dataset directories
- Some datasets may have nested folders - move CSV files to the root

**Column name mismatches:**

- The preprocessing script handles common column name variations
- Check `data_preprocessing.py` if your dataset has different column names

## Dataset Information File

After running the download script, a `dataset_info.json` file is created in `backend/data/raw/` with:

- Dataset sources and URLs
- Download locations
- Purpose of each dataset
- Setup instructions

## Support

If you encounter issues:

1. Check the dataset URLs are still valid
2. Ensure you have a Kaggle account (free)
3. Verify file permissions and directory structure
4. Check the preprocessing logs for specific errors
