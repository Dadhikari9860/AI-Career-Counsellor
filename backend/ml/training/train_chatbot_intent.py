"""
Train chatbot intent classifier using TF-IDF + Logistic Regression/SVM
"""

import pandas as pd
import numpy as np
from pathlib import Path
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import json

class ChatbotIntentClassifier:
    """Intent classifier for chatbot"""
    
    def __init__(self, model_type='logistic_regression'):
        self.model_type = model_type
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),  # Bigrams for better context
            stop_words='english',
            min_df=1,
            max_df=0.9  # Remove very common words
        )
        
        if model_type == 'logistic_regression':
            self.model = LogisticRegression(
                max_iter=2000, 
                C=1.0,  # Balanced regularization
                random_state=42, 
                solver='lbfgs',
                multi_class='multinomial'  # Better for multi-class
            )
        else:
            self.model = SVC(kernel='linear', random_state=42)
        
        self.label_encoder = {}
        self.reverse_label_encoder = {}
        self.is_trained = False
    
    def create_training_data(self):
        """Create training data for intent classification with more examples"""
        # Define intents and expanded sample queries for better accuracy
        intents = {
            'career_advice': [
                'what career should i choose', 'which career is best for me', 'career guidance',
                'help me choose a career', 'what job should i do', 'career recommendations',
                'suggest a career path', 'what are good careers', 'career options for me',
                'what career path should i take', 'recommend a career', 'best career for my skills',
                'career advice please', 'what career suits me', 'career suggestions',
                'guide me on career', 'help with career choice', 'career direction',
                'what should i do for career', 'career planning help', 'career decision',
                'which field should i choose', 'career recommendation', 'suitable career for me'
            ],
            'job_search': [
                'find me a job', 'show available jobs', 'job openings', 'search jobs',
                'find jobs near me', 'job opportunities', 'where can i find work',
                'job listings', 'available positions', 'hiring jobs', 'jobs available',
                'show me jobs', 'job search', 'find employment', 'job vacancies',
                'open positions', 'job postings', 'available jobs', 'find work',
                'job market', 'employment opportunities', 'job board', 'career opportunities',
                'job hunting', 'looking for job', 'need a job', 'job openings near me'
            ],
            'skill_gap': [
                'what skills do i need', 'skill gap analysis', 'what am i missing',
                'skills required for this role', 'what do i need to learn', 'missing skills',
                'skill requirements', 'what skills should i have', 'check my skills',
                'analyze my skills', 'what skills am i lacking', 'skill assessment',
                'required skills', 'skills needed', 'what skills do i lack',
                'skill gap check', 'missing competencies', 'skills gap', 'skill analysis',
                'what skills required', 'check skill gaps', 'identify missing skills',
                'skill requirements for role', 'what skills missing', 'skill evaluation'
            ],
            'learning_path': [
                'how to learn', 'learning resources', 'courses to take', 'what should i study',
                'learning path', 'training resources', 'how to improve', 'study materials',
                'recommended courses', 'where to learn', 'how can i learn', 'learning guide',
                'training path', 'study plan', 'courses recommended', 'how to study',
                'learning materials', 'educational resources', 'training courses',
                'how to develop skills', 'skill development', 'learning roadmap',
                'study resources', 'training plan', 'how to gain skills', 'learning strategy'
            ],
            'recommendation_explanation': [
                'why this recommendation', 'explain recommendation', 'why am i seeing this',
                'how was this recommended', 'reason for suggestion', 'why this job',
                'explain the match', 'why is this recommended', 'explain why',
                'why did you recommend', 'reason for recommendation', 'how was this chosen',
                'explain the suggestion', 'why this match', 'explain job match',
                'why recommend this', 'explanation please', 'why this role',
                'how did you decide', 'reason behind recommendation', 'explain the choice',
                'why is this suitable', 'explain suitability', 'why matched'
            ],
            'general_info': [
                'hello', 'hi', 'help', 'hey', 'greetings', 'good morning', 'good afternoon',
                'good evening', 'how are you', 'what can you do', 'tell me about yourself',
                'what is this', 'introduction', 'who are you', 'what are you',
                'help me', 'assist me', 'support', 'information', 'tell me more',
                'explain', 'what is', 'how does this work', 'guide me', 'instructions',
                'what is this system', 'about', 'thanks', 'thank you'
            ]
        }
        
        # Create training data
        texts = []
        labels = []
        
        for intent, queries in intents.items():
            for query in queries:
                texts.append(query)
                labels.append(intent)
        
        # Add variations
        variations = {
            'career_advice': ['career', 'job', 'role', 'profession', 'occupation'],
            'job_search': ['job', 'position', 'opening', 'vacancy', 'hiring'],
            'skill_gap': ['skill', 'ability', 'competency', 'expertise'],
            'learning_path': ['learn', 'study', 'course', 'training', 'education'],
            'recommendation_explanation': ['why', 'explain', 'reason', 'how'],
            'general_info': ['hello', 'hi', 'help', 'thanks']
        }
        
        # Generate more variations
        for intent, keywords in variations.items():
            for keyword in keywords:
                texts.append(f"i need {keyword}")
                labels.append(intent)
                texts.append(f"tell me about {keyword}")
                labels.append(intent)
                texts.append(f"help with {keyword}")
                labels.append(intent)
                texts.append(f"show me {keyword}")
                labels.append(intent)
                texts.append(f"i want {keyword}")
                labels.append(intent)
        
        # Add more data augmentation with synonyms and paraphrasing
        augmentations = {
            'career_advice': [
                'i need career help', 'career guidance needed', 'what career path',
                'suggest career', 'career options', 'best career choice',
                'career recommendation needed', 'help choose career', 'career advice needed'
            ],
            'job_search': [
                'i need a job', 'find employment', 'job opportunities available',
                'show job openings', 'available positions', 'hiring now',
                'job search help', 'find work', 'employment search'
            ],
            'skill_gap': [
                'what skills required', 'skills i need', 'required competencies',
                'skill assessment needed', 'check my skills', 'skill evaluation',
                'missing abilities', 'what do i need to know', 'skill requirements check'
            ],
            'learning_path': [
                'how to study', 'learning guide', 'training needed',
                'courses available', 'study resources', 'how to improve skills',
                'education path', 'skill development', 'training resources'
            ],
            'recommendation_explanation': [
                'why recommend', 'explain why', 'reason for this',
                'how was this chosen', 'why this match', 'explain the choice',
                'why suitable', 'explain match', 'reason behind'
            ],
            'general_info': [
                'hi there', 'greetings', 'can you help', 'what is this',
                'how does it work', 'tell me more', 'i need help',
                'information please', 'explain system', 'what can you do'
            ]
        }
        
        for intent, augs in augmentations.items():
            for aug in augs:
                texts.append(aug)
                labels.append(intent)
        
        return texts, labels
    
    def train(self, texts=None, labels=None):
        """Train the intent classifier"""
        print("Training chatbot intent classifier...")
        
        if texts is None or labels is None:
            texts, labels = self.create_training_data()
        
        # Create label mapping
        unique_labels = list(set(labels))
        self.label_encoder = {label: idx for idx, label in enumerate(unique_labels)}
        self.reverse_label_encoder = {idx: label for label, idx in self.label_encoder.items()}
        
        # Encode labels
        encoded_labels = [self.label_encoder[label] for label in labels]
        
        # Vectorize texts
        X = self.vectorizer.fit_transform(texts)
        y = np.array(encoded_labels)
        
        # Split data with stratification
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train model
        n_train = X_train.shape[0] if hasattr(X_train, 'shape') else len(X_train)
        print(f"Training {self.model_type} on {n_train} samples...")
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        y_train_pred = self.model.predict(X_train)
        
        train_accuracy = accuracy_score(y_train, y_train_pred)
        test_accuracy = accuracy_score(y_test, y_pred)
        
        # Cross-validation for more reliable estimate
        from sklearn.model_selection import cross_val_score
        cv_scores = cross_val_score(self.model, X_train, y_train, cv=5, scoring='accuracy')
        print(f"\nCross-validation accuracy (5-fold): {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        print(f"\nModel Performance:")
        print(f"Train Accuracy: {train_accuracy:.4f}")
        print(f"Test Accuracy: {test_accuracy:.4f}")
        print(f"Overfitting Gap: {train_accuracy - test_accuracy:.4f} (should be < 0.15)")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=unique_labels))
        
        # Warn if overfitting detected
        if train_accuracy - test_accuracy > 0.15:
            print("\n⚠️  WARNING: Potential overfitting detected! Train accuracy is significantly higher than test accuracy.")
            print("   Consider: increasing regularization (C parameter), reducing features, or adding more training data.")
        
        self.is_trained = True
        
        return accuracy
    
    def predict(self, text):
        """Predict intent for a text"""
        if not self.is_trained:
            raise ValueError("Model not trained yet")
        
        # Vectorize
        X = self.vectorizer.transform([text])
        
        # Predict
        prediction = self.model.predict(X)[0]
        probabilities = self.model.predict_proba(X)[0]
        
        intent = self.reverse_label_encoder[prediction]
        confidence = float(probabilities[prediction])
        
        # Get top intents
        top_indices = np.argsort(probabilities)[::-1][:3]
        top_intents = []
        for idx in top_indices:
            top_intents.append({
                'intent': self.reverse_label_encoder[idx],
                'confidence': float(probabilities[idx])
            })
        
        return {
            'intent': intent,
            'confidence': confidence,
            'top_intents': top_intents
        }
    
    def save(self, model_dir='ml/models'):
        """Save the model"""
        model_path = Path(model_dir)
        model_path.mkdir(parents=True, exist_ok=True)
        
        # Save model and vectorizer
        joblib.dump(self.model, model_path / 'intent_classifier.joblib')
        joblib.dump(self.vectorizer, model_path / 'intent_vectorizer.joblib')
        
        # Save label encoders
        with open(model_path / 'intent_label_encoder.json', 'w') as f:
            json.dump(self.label_encoder, f, indent=2)
        
        with open(model_path / 'intent_reverse_encoder.json', 'w') as f:
            json.dump(self.reverse_label_encoder, f, indent=2)
        
        # Save metadata
        metadata = {
            'model_type': self.model_type,
            'n_intents': len(self.label_encoder),
            'intents': list(self.label_encoder.keys()),
            'is_trained': self.is_trained
        }
        
        with open(model_path / 'intent_metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Model saved to {model_path}")

def main():
    """Train intent classifier"""
    print("Training chatbot intent classifier...")
    
    classifier = ChatbotIntentClassifier(model_type='logistic_regression')
    accuracy = classifier.train()
    
    # Test with sample queries
    test_queries = [
        "what career should I choose?",
        "find me a job",
        "what skills do I need?",
        "how can I learn Python?",
        "why is this job recommended?",
        "hello"
    ]
    
    print("\nTesting with sample queries:")
    for query in test_queries:
        result = classifier.predict(query)
        print(f"Query: '{query}'")
        print(f"Intent: {result['intent']} (confidence: {result['confidence']:.4f})")
        print()
    
    # Save model
    classifier.save()
    
    print("Intent classifier training complete!")

if __name__ == '__main__':
    main()

