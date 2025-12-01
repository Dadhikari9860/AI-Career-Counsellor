"""
Train collaborative filtering model using SVD (Singular Value Decomposition)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import joblib
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import StandardScaler
import json

try:
    from surprise import Dataset, Reader, SVD as SurpriseSVD
    from surprise.model_selection import train_test_split
    SURPRISE_AVAILABLE = True
except ImportError:
    SURPRISE_AVAILABLE = False
    print("Surprise library not available, using sklearn TruncatedSVD")

class CollaborativeFilteringModel:
    """Collaborative filtering using SVD"""
    
    def __init__(self, n_components=50, use_surprise=True):
        self.n_components = n_components
        self.use_surprise = use_surprise and SURPRISE_AVAILABLE
        
        if self.use_surprise:
            self.model = SurpriseSVD(n_factors=n_components, random_state=42)
        else:
            self.model = TruncatedSVD(n_components=n_components, random_state=42)
            self.scaler = StandardScaler()
        
        self.user_mapping = {}
        self.item_mapping = {}
        self.reverse_user_mapping = {}
        self.reverse_item_mapping = {}
        self.interaction_matrix = None
        self.test_interactions = None
        self.is_trained = False
    
    def prepare_interaction_matrix(self, interactions_df, users_df=None, items_df=None):
        """Create user-item interaction matrix"""
        print("Preparing interaction matrix...")
        
        # Map user and item IDs to indices
        unique_users = interactions_df['user_id'].unique()
        unique_items = interactions_df['item_id'].unique()
        
        self.user_mapping = {user_id: idx for idx, user_id in enumerate(unique_users)}
        self.item_mapping = {item_id: idx for idx, item_id in enumerate(unique_items)}
        self.reverse_user_mapping = {idx: user_id for user_id, idx in self.user_mapping.items()}
        self.reverse_item_mapping = {idx: item_id for item_id, idx in self.item_mapping.items()}
        
        # Create interaction matrix
        n_users = len(unique_users)
        n_items = len(unique_items)
        self.interaction_matrix = np.zeros((n_users, n_items))
        
        for _, row in interactions_df.iterrows():
            user_idx = self.user_mapping[row['user_id']]
            item_idx = self.item_mapping[row['item_id']]
            rating = row.get('rating', 1)
            self.interaction_matrix[user_idx, item_idx] = rating
        
        print(f"Created interaction matrix: {n_users} users × {n_items} items")
        print(f"Sparsity: {(self.interaction_matrix == 0).sum() / (n_users * n_items) * 100:.2f}%")
    
    def train(self, interactions_df, test_size=0.2):
        """Train the SVD model with proper train/test split"""
        print("Training collaborative filtering model...")
        
        if self.use_surprise:
            # Use Surprise library (already has proper train/test split)
            reader = Reader(rating_scale=(0, 5))
            data = Dataset.load_from_df(
                interactions_df[['user_id', 'item_id', 'rating']],
                reader
            )
            trainset, testset = train_test_split(data, test_size=test_size, random_state=42)
            self.model.fit(trainset)
            
            # Evaluate on test set
            from surprise import accuracy
            predictions = self.model.test(testset)
            rmse = accuracy.rmse(predictions, verbose=False)
            mae = accuracy.mae(predictions, verbose=False)
            print(f"Test RMSE: {rmse:.4f}, Test MAE: {mae:.4f}")
        else:
            # Use sklearn TruncatedSVD - FIX: Split data before creating matrix
            # Split interactions into train and test
            from sklearn.model_selection import train_test_split as sk_train_test_split
            
            # Create train/test split at interaction level
            train_interactions, test_interactions = sk_train_test_split(
                interactions_df, test_size=test_size, random_state=42
            )
            
            print(f"Training on {len(train_interactions)} interactions, testing on {len(test_interactions)} interactions")
            
            # Create interaction matrix only from training data
            if self.interaction_matrix is None:
                self.prepare_interaction_matrix(train_interactions)
            
            # Store test interactions for evaluation
            self.test_interactions = test_interactions
            
            # Normalize the matrix (fit on training data only)
            self.interaction_matrix = self.scaler.fit_transform(self.interaction_matrix.T).T
            
            # Apply SVD on training data only
            self.model.fit(self.interaction_matrix)
            
            # Evaluate on test set
            if len(test_interactions) > 0:
                test_errors = []
                for _, row in test_interactions.iterrows():
                    user_id = row['user_id']
                    item_id = row['item_id']
                    true_rating = row['rating']
                    
                    if user_id in self.user_mapping and item_id in self.item_mapping:
                        pred_rating = self.predict(user_id, item_id)
                        test_errors.append(abs(pred_rating - true_rating))
                
                if test_errors:
                    mae = np.mean(test_errors)
                    rmse = np.sqrt(np.mean([e**2 for e in test_errors]))
                    print(f"Test MAE: {mae:.4f}, Test RMSE: {rmse:.4f}")
        
        self.is_trained = True
        print("Model training complete!")
    
    def predict(self, user_id, item_id):
        """Predict rating for user-item pair"""
        if not self.is_trained:
            raise ValueError("Model not trained yet")
        
        if self.use_surprise:
            try:
                prediction = self.model.predict(user_id, item_id)
                return prediction.est
            except:
                return 0.0
        else:
            if user_id not in self.user_mapping or item_id not in self.item_mapping:
                return 0.0
            
            user_idx = self.user_mapping[user_id]
            item_idx = self.item_mapping[item_id]
            
            # Reconstruct using SVD components
            user_factors = self.model.transform(self.interaction_matrix[user_idx:user_idx+1])[0]
            item_factors = self.model.components_[:, item_idx]
            
            prediction = np.dot(user_factors, item_factors)
            return float(prediction)
    
    def recommend_items(self, user_id, item_ids, top_k=10):
        """Recommend items for a user"""
        if not self.is_trained:
            return []
        
        predictions = []
        for item_id in item_ids:
            score = self.predict(user_id, item_id)
            predictions.append({
                'item_id': int(item_id),
                'score': float(score)
            })
        
        # Sort by score and return top_k
        predictions.sort(key=lambda x: x['score'], reverse=True)
        return predictions[:top_k]
    
    def get_user_embeddings(self):
        """Get user embeddings from the model"""
        if not self.is_trained or self.use_surprise:
            return None
        
        return self.model.transform(self.interaction_matrix)
    
    def get_item_embeddings(self):
        """Get item embeddings from the model"""
        if not self.is_trained or self.use_surprise:
            return None
        
        return self.model.components_.T
    
    def save(self, model_dir='ml/models'):
        """Save the model"""
        model_path = Path(model_dir)
        model_path.mkdir(parents=True, exist_ok=True)
        
        # Save model
        joblib.dump(self.model, model_path / 'svd_model.joblib')
        
        if not self.use_surprise:
            joblib.dump(self.scaler, model_path / 'svd_scaler.joblib')
            if self.interaction_matrix is not None:
                np.save(model_path / 'interaction_matrix.npy', self.interaction_matrix)
        
        # Save mappings
        with open(model_path / 'svd_user_mapping.json', 'w') as f:
            json.dump({str(k): v for k, v in self.user_mapping.items()}, f)
        
        with open(model_path / 'svd_item_mapping.json', 'w') as f:
            json.dump({str(k): v for k, v in self.item_mapping.items()}, f)
        
        # Save metadata
        metadata = {
            'n_components': self.n_components,
            'use_surprise': self.use_surprise,
            'n_users': len(self.user_mapping),
            'n_items': len(self.item_mapping),
            'is_trained': self.is_trained
        }
        
        with open(model_path / 'svd_metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Model saved to {model_path}")

def main():
    """Train collaborative filtering model"""
    print("Training collaborative filtering model...")
    
    data_dir = Path('data/processed')
    
    # Load interactions data
    interactions_df = pd.read_csv(data_dir / 'interactions_processed.csv') if (data_dir / 'interactions_processed.csv').exists() else None
    
    # Create sample data if not available
    if interactions_df is None or len(interactions_df) == 0:
        print("No interactions data found, creating sample data...")
        n_users = 100
        n_items = 50
        n_interactions = 500
        
        interactions_df = pd.DataFrame({
            'user_id': np.random.randint(0, n_users, n_interactions),
            'item_id': np.random.randint(0, n_items, n_interactions),
            'rating': np.random.randint(1, 6, n_interactions)
        })
        
        # Remove duplicates
        interactions_df = interactions_df.drop_duplicates(subset=['user_id', 'item_id'])
    
    # Train model
    model = CollaborativeFilteringModel(n_components=50, use_surprise=SURPRISE_AVAILABLE)
    model.train(interactions_df)
    
    # Save model
    model.save()
    
    print("Collaborative filtering model training complete!")

if __name__ == '__main__':
    main()

