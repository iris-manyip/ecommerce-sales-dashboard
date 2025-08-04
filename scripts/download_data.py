#!/usr/bin/env python3
"""
Data Download Script for E-commerce Sales Dataset

This script downloads the e-commerce sales dataset from Kaggle using kagglehub.
"""

import os
import sys
import kagglehub
from pathlib import Path

def download_dataset():
    """
    Download the e-commerce sales dataset from Kaggle.
    
    Returns:
        str: Path to the downloaded dataset files
    """
    try:
        print("🔄 Downloading e-commerce sales dataset from Kaggle...")
        
        # Download the dataset
        path = kagglehub.dataset_download("thedevastator/unlock-profits-with-e-commerce-sales-data")
        
        print(f"✅ Dataset downloaded successfully!")
        print(f"📁 Path to dataset files: {path}")
        
        # Create symbolic link or copy files to data/raw directory
        data_raw_dir = Path("data/raw")
        data_raw_dir.mkdir(parents=True, exist_ok=True)
        
        # List downloaded files
        if os.path.exists(path):
            print("\n📋 Downloaded files:")
            for file in os.listdir(path):
                file_path = os.path.join(path, file)
                if os.path.isfile(file_path):
                    print(f"   - {file}")
        
        return path
        
    except Exception as e:
        print(f"❌ Error downloading dataset: {str(e)}")
        print("Please make sure you have:")
        print("1. Kaggle API credentials configured")
        print("2. Internet connection")
        print("3. Sufficient disk space")
        sys.exit(1)

def setup_data_structure():
    """
    Set up the data directory structure.
    """
    directories = [
        "data/raw",
        "data/processed", 
        "notebooks",
        "scripts",
        "src",
        "reports/figures",
        "reports/insights"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

if __name__ == "__main__":
    print("🚀 Starting dataset download process...")
    
    # Set up directory structure
    setup_data_structure()
    
    # Download the dataset
    dataset_path = download_dataset()
    
    print("\n🎉 Setup complete!")
    print("Next steps:")
    print("1. Explore the downloaded data in data/raw/")
    print("2. Run data processing scripts")
    print("3. Start analysis with Jupyter notebooks") 