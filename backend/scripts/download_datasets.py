"""
Script to download all datasets used in the Career Guidance System.

This script downloads datasets from Kaggle and other sources.
Requires Kaggle API credentials for automatic download.
"""

import os
import sys
import subprocess
import requests
from pathlib import Path
import zipfile
import json

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

class DatasetDownloader:
    """Download datasets for the career guidance system"""
    
    def __init__(self, raw_data_dir='data/raw'):
        self.raw_data_dir = Path(raw_data_dir)
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)
        self.kaggle_available = self._check_kaggle()
    
    def _check_kaggle(self):
        """Check if Kaggle API is available"""
        try:
            import kaggle
            return True
        except ImportError:
            print("⚠️  Kaggle package not installed. Installing...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "kaggle", "--quiet"])
                import kaggle
                return True
            except:
                print("❌ Could not install kaggle package. Please install manually: pip install kaggle")
                return False
    
    def _check_kaggle_credentials(self):
        """Check if Kaggle credentials are set up"""
        kaggle_dir = Path.home() / '.kaggle'
        kaggle_key = kaggle_dir / 'kaggle.json'
        
        if not kaggle_key.exists():
            print("\n⚠️  Kaggle API credentials not found!")
            print("To download datasets from Kaggle, you need to:")
            print("1. Go to https://www.kaggle.com/account")
            print("2. Scroll down to 'API' section")
            print("3. Click 'Create New API Token'")
            print("4. This will download kaggle.json")
            print("5. Place it in ~/.kaggle/kaggle.json")
            print("\nAlternatively, you can download datasets manually from the URLs below.")
            return False
        return True
    
    def download_resume_dataset(self):
        """Download resume/user profile dataset"""
        print("\n" + "="*60)
        print("Downloading Resume/User Profile Dataset")
        print("="*60)
        
        datasets = [
            {
                'name': 'resume-dataset',
                'kaggle': 'snehaanbhawal/resume-dataset',
                'description': 'Resume dataset with skills, experience, and job titles',
                'manual_url': 'https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset'
            },
            {
                'name': 'it-jobs-market',
                'kaggle': 'asaniczka/it-jobs-market-analysis-2023',
                'description': 'IT job market data with skills and roles',
                'manual_url': 'https://www.kaggle.com/datasets/asaniczka/it-jobs-market-analysis-2023'
            }
        ]
        
        for dataset in datasets:
            print(f"\n📥 Downloading: {dataset['name']}")
            print(f"   Description: {dataset['description']}")
            
            if self.kaggle_available and self._check_kaggle_credentials():
                try:
                    import kaggle
                    api = kaggle.api
                    api.authenticate()
                    
                    output_path = self.raw_data_dir / dataset['name']
                    output_path.mkdir(exist_ok=True)
                    
                    print(f"   Downloading from Kaggle...")
                    api.dataset_download_files(
                        dataset['kaggle'],
                        path=str(output_path),
                        unzip=True
                    )
                    print(f"   ✅ Downloaded to {output_path}")
                except Exception as e:
                    print(f"   ❌ Kaggle download failed: {e}")
                    print(f"   📋 Manual download: {dataset['manual_url']}")
            else:
                print(f"   📋 Please download manually from: {dataset['manual_url']}")
                print(f"   📁 Save files to: {self.raw_data_dir / dataset['name']}")
    
    def download_job_postings_dataset(self):
        """Download job postings dataset"""
        print("\n" + "="*60)
        print("Downloading Job Postings Dataset")
        print("="*60)
        
        datasets = [
            {
                'name': 'data-science-jobs',
                'kaggle': 'andrewmvd/data-science-jobs',
                'description': 'Data science job postings with descriptions and requirements',
                'manual_url': 'https://www.kaggle.com/datasets/andrewmvd/data-science-jobs'
            },
            {
                'name': 'linkedin-job-postings',
                'kaggle': 'arshkon/linkedin-job-postings',
                'description': 'Software engineering and tech job postings from LinkedIn',
                'manual_url': 'https://www.kaggle.com/datasets/arshkon/linkedin-job-postings'
            }
        ]
        
        for dataset in datasets:
            print(f"\n📥 Downloading: {dataset['name']}")
            print(f"   Description: {dataset['description']}")
            
            if self.kaggle_available and self._check_kaggle_credentials():
                try:
                    import kaggle
                    api = kaggle.api
                    api.authenticate()
                    
                    output_path = self.raw_data_dir / dataset['name']
                    output_path.mkdir(exist_ok=True)
                    
                    print(f"   Downloading from Kaggle...")
                    api.dataset_download_files(
                        dataset['kaggle'],
                        path=str(output_path),
                        unzip=True
                    )
                    print(f"   ✅ Downloaded to {output_path}")
                except Exception as e:
                    print(f"   ❌ Kaggle download failed: {e}")
                    print(f"   📋 Manual download: {dataset['manual_url']}")
            else:
                print(f"   📋 Please download manually from: {dataset['manual_url']}")
                print(f"   📁 Save files to: {self.raw_data_dir / dataset['name']}")
    
    def download_interactions_dataset(self):
        """Download or create user-job interactions dataset"""
        print("\n" + "="*60)
        print("User-Job Interactions Dataset")
        print("="*60)
        
        print("\n📝 Note: User-job interactions are typically created from:")
        print("   1. System feedback (stored in Feedback table)")
        print("   2. User behavior data (clicks, saves, applications)")
        print("   3. External recommendation datasets")
        
        # Try to find job recommendation datasets
        datasets = [
            {
                'name': 'job-recommendation',
                'kaggle': None,  # Search for available datasets
                'description': 'Job recommendation datasets with user interactions',
                'manual_url': 'https://www.kaggle.com/datasets/search?search=job+recommendation'
            }
        ]
        
        print("\n💡 Tip: You can search Kaggle for 'job recommendation' datasets")
        print(f"   Search URL: https://www.kaggle.com/datasets/search?search=job+recommendation")
        print(f"\n📁 If you have interaction data, save it to: {self.raw_data_dir / 'interactions'}")
    
    def download_alternative_datasets(self):
        """Download datasets from alternative sources (if Kaggle unavailable)"""
        print("\n" + "="*60)
        print("Alternative Dataset Sources")
        print("="*60)
        
        print("\n📚 If Kaggle is unavailable, you can use these alternatives:")
        print("\n1. Resume Dataset:")
        print("   - GitHub: Search for 'resume dataset' repositories")
        print("   - UCI ML Repository: https://archive.ics.uci.edu/")
        print("   - Data.gov: https://data.gov/")
        
        print("\n2. Job Postings Dataset:")
        print("   - Indeed API (requires API key)")
        print("   - LinkedIn (requires API access)")
        print("   - Glassdoor (web scraping with permission)")
        
        print("\n3. Sample Data:")
        print("   - The system can generate sample data for testing")
        print("   - Run: python -m ml.training.train_all")
        print("   - This will create sample datasets if real ones are missing")
    
    def create_dataset_info(self):
        """Create a JSON file with dataset information"""
        info = {
            'datasets': [
                {
                    'name': 'Resume Dataset',
                    'sources': [
                        'https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset',
                        'https://www.kaggle.com/datasets/asaniczka/it-jobs-market-analysis-2023'
                    ],
                    'location': str(self.raw_data_dir / 'resume-dataset'),
                    'purpose': 'User feature extraction, skill mapping, classifier training'
                },
                {
                    'name': 'Job Postings Dataset',
                    'sources': [
                        'https://www.kaggle.com/datasets/andrewmvd/data-science-jobs',
                        'https://www.kaggle.com/datasets/arshkon/linkedin-job-postings'
                    ],
                    'location': str(self.raw_data_dir / 'data-science-jobs'),
                    'purpose': 'Content-based recommendations, skill gap analysis'
                },
                {
                    'name': 'User-Job Interactions',
                    'sources': [
                        'System feedback (Feedback table)',
                        'Kaggle job recommendation datasets'
                    ],
                    'location': str(self.raw_data_dir / 'interactions'),
                    'purpose': 'Collaborative filtering (SVD), personalization'
                }
            ],
            'download_date': str(Path(__file__).stat().st_mtime),
            'instructions': {
                'kaggle_setup': '1. Install: pip install kaggle\n2. Get API token from kaggle.com/account\n3. Place kaggle.json in ~/.kaggle/',
                'manual_download': 'Download CSV files from Kaggle URLs and place in data/raw/',
                'preprocessing': 'Run: python -m ml.training.data_preprocessing',
                'training': 'Run: python -m ml.training.train_all'
            }
        }
        
        info_path = self.raw_data_dir / 'dataset_info.json'
        with open(info_path, 'w') as f:
            json.dump(info, f, indent=2)
        
        print(f"\n✅ Dataset information saved to: {info_path}")
        return info
    
    def download_all(self):
        """Download all datasets"""
        print("\n" + "="*70)
        print("CAREER GUIDANCE SYSTEM - DATASET DOWNLOADER")
        print("="*70)
        
        print("\nThis script will download the following datasets:")
        print("1. Resume/User Profile Dataset")
        print("2. Job Postings Dataset")
        print("3. User-Job Interactions Dataset (info only)")
        
        # Download datasets
        self.download_resume_dataset()
        self.download_job_postings_dataset()
        self.download_interactions_dataset()
        
        # Create info file
        self.create_dataset_info()
        
        # Show summary
        print("\n" + "="*70)
        print("DOWNLOAD SUMMARY")
        print("="*70)
        
        downloaded = []
        missing = []
        
        for dataset_dir in self.raw_data_dir.iterdir():
            if dataset_dir.is_dir():
                files = list(dataset_dir.glob('*.csv'))
                if files:
                    downloaded.append(f"{dataset_dir.name}: {len(files)} CSV file(s)")
                else:
                    missing.append(dataset_dir.name)
        
        if downloaded:
            print("\n✅ Downloaded datasets:")
            for item in downloaded:
                print(f"   - {item}")
        
        if missing:
            print("\n⚠️  Directories created but no CSV files found:")
            for item in missing:
                print(f"   - {item}")
                print(f"     Please download manually and place CSV files here")
        
        print("\n📋 Next steps:")
        print("   1. Ensure all datasets are in: backend/data/raw/")
        print("   2. Run preprocessing: python -m ml.training.data_preprocessing")
        print("   3. Train models: python -m ml.training.train_all")
        print("\n" + "="*70)


def main():
    """Main function"""
    downloader = DatasetDownloader()
    downloader.download_all()


if __name__ == '__main__':
    main()

