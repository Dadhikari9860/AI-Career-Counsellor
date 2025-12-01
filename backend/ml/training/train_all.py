"""
Master script to train all ML models
Run this script to train all models in sequence
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from ml.training.train_content_based import main as train_content_based
from ml.training.train_collaborative_filtering import main as train_collaborative
from ml.training.train_classifier import main as train_classifier
from ml.training.train_chatbot_intent import main as train_intent
from ml.training.data_preprocessing import main as preprocess_data

def main():
    """Train all models"""
    print("=" * 60)
    print("Starting ML Model Training Pipeline")
    print("=" * 60)
    
    # Step 1: Preprocess data
    print("\n[1/5] Preprocessing data...")
    try:
        preprocess_data()
    except Exception as e:
        print(f"Warning: Data preprocessing failed: {e}")
        print("Continuing with training (models will use sample data if needed)...")
    
    # Step 2: Train content-based model
    print("\n[2/5] Training content-based recommendation model...")
    try:
        train_content_based()
    except Exception as e:
        print(f"Error training content-based model: {e}")
        return
    
    # Step 3: Train collaborative filtering
    print("\n[3/5] Training collaborative filtering model...")
    try:
        train_collaborative()
    except Exception as e:
        print(f"Error training collaborative filtering model: {e}")
        return
    
    # Step 4: Train classifier
    print("\n[4/5] Training career role classifier...")
    try:
        train_classifier()
    except Exception as e:
        print(f"Error training classifier: {e}")
        return
    
    # Step 5: Train intent classifier
    print("\n[5/5] Training chatbot intent classifier...")
    try:
        train_intent()
    except Exception as e:
        print(f"Error training intent classifier: {e}")
        return
    
    print("\n" + "=" * 60)
    print("All models trained successfully!")
    print("=" * 60)

if __name__ == '__main__':
    main()

