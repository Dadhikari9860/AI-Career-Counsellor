# Overfitting and Data Leakage Fixes

This document describes the fixes applied to address overfitting and data linkage issues in the ML training pipeline.

## Issues Identified

### 1. Overfitting in Career Role Classifier
**Problem:**
- `max_depth=50` was too high for the dataset size (~2000 samples)
- Synthetic data had minimal noise (only 10% chance), creating overly distinct patterns
- No validation monitoring to detect overfitting

**Fixes Applied:**
- Reduced `max_depth` from 50 to 15
- Reduced `n_estimators` from 500 to 200
- Increased `min_samples_split` from 3 to 10
- Increased `min_samples_leaf` from 3 to 5
- Added `max_samples=0.8` to use 80% of samples per tree
- Increased noise in synthetic data from 10% to 30% with more realistic cross-role skills
- Added overfitting detection that compares train vs test accuracy
- Added warning system when overfitting gap > 0.15

**File:** `backend/ml/training/train_classifier.py`

### 2. Data Leakage in Content-Based Recommender
**Problem:**
- TF-IDF vectorizer was fitted on user data first, then used to transform job/role data
- This created a data linkage where vocabulary was determined by user data only
- Could leak information about user data distribution into job/role representations

**Fixes Applied:**
- Modified training pipeline to fit vectorizer on ALL data combined (users + jobs + roles)
- Vectorizer vocabulary is now determined by the entire corpus, not just one data type
- Each data type is then transformed separately using the same fitted vectorizer
- Added warnings if vectorizer is not properly fitted before transformation

**File:** `backend/ml/training/train_content_based.py`

### 3. Missing Train/Test Split in Collaborative Filtering
**Problem:**
- When using sklearn TruncatedSVD (fallback when Surprise library unavailable), the entire interaction matrix was used for training
- No proper train/test split, leading to potential overfitting

**Fixes Applied:**
- Added proper train/test split at the interaction level BEFORE creating the interaction matrix
- Interaction matrix is now created only from training data
- Test set is evaluated separately with MAE and RMSE metrics
- Added test_interactions attribute to store test data

**File:** `backend/ml/training/train_collaborative_filtering.py`

### 4. Missing Overfitting Detection in Intent Classifier
**Problem:**
- No comparison between train and test accuracy
- Could not detect if model was overfitting

**Fixes Applied:**
- Added train accuracy calculation
- Added overfitting gap calculation (train - test accuracy)
- Added warning when overfitting gap > 0.15
- Provides suggestions for fixing overfitting

**File:** `backend/ml/training/train_chatbot_intent.py`

## Best Practices Implemented

1. **Proper Data Splitting:**
   - All models now use proper train/test splits
   - Stratification used where appropriate (for classification tasks)
   - Test data is never used during training

2. **Overfitting Prevention:**
   - Reduced model complexity (lower max_depth, higher min_samples_split)
   - Added regularization parameters
   - Increased noise in synthetic data to be more realistic
   - Cross-validation for more reliable accuracy estimates

3. **Data Leakage Prevention:**
   - Vectorizers fitted on combined corpus before transformation
   - No information from test set used during training
   - Proper separation of training and inference pipelines

4. **Monitoring and Validation:**
   - Train vs test accuracy comparison
   - Overfitting gap warnings
   - Cross-validation scores
   - Test set evaluation metrics (MAE, RMSE, accuracy, precision, recall, F1)

## Testing Recommendations

After these fixes, you should:

1. **Retrain all models** to see the new metrics:
   ```bash
   cd backend
   python -m ml.training.train_all
   ```

2. **Check for overfitting warnings** in the training output

3. **Compare metrics:**
   - Train accuracy should be close to test accuracy (gap < 0.15)
   - Cross-validation scores should be consistent
   - Test metrics should be reasonable for your use case

4. **Monitor in production:**
   - Track prediction accuracy on new data
   - Compare with training metrics
   - Retrain if performance degrades

## Expected Improvements

- **Better generalization:** Models should perform better on unseen data
- **More realistic performance metrics:** Test accuracy will be more representative of real-world performance
- **Reduced overfitting:** Train/test accuracy gap should be smaller
- **Proper validation:** Can now trust the test metrics as true performance indicators

## Notes

- The classifier may show slightly lower accuracy initially, but this is expected and indicates the model is not overfitting
- The content-based model will have a more robust vocabulary that works across all data types
- Collaborative filtering will have proper evaluation metrics on held-out test data

