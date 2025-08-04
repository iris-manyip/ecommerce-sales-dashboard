#!/usr/bin/env python3
"""
Setup Script for E-commerce Sales Data Analysis Project

This script helps users set up the project environment and download data.
"""

import os
import sys
import subprocess
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        logger.error("Python 3.8+ is required")
        return False
    logger.info(f"✅ Python version: {sys.version}")
    return True

def create_virtual_environment():
    """Create a virtual environment."""
    try:
        logger.info("🔧 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        logger.info("✅ Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to create virtual environment: {e}")
        return False

def install_dependencies():
    """Install project dependencies."""
    try:
        logger.info("📦 Installing dependencies...")
        
        # Determine the correct pip command
        if os.name == 'nt':  # Windows
            pip_cmd = "venv\\Scripts\\pip"
        else:  # Unix/Linux/macOS
            pip_cmd = "venv/bin/pip"
        
        # Install requirements
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        logger.info("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to install dependencies: {e}")
        return False

def setup_directories():
    """Set up project directories."""
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
        logger.info(f"✅ Created directory: {directory}")

def download_data():
    """Download the dataset."""
    try:
        logger.info("📥 Downloading dataset...")
        subprocess.run([sys.executable, "scripts/download_data.py"], check=True)
        logger.info("✅ Dataset downloaded successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to download dataset: {e}")
        return False

def create_sample_notebook():
    """Create a sample notebook for quick start."""
    sample_notebook = """{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Quick Start - E-commerce Data Analysis\\n",
    "\\n",
    "This notebook provides a quick overview of the e-commerce sales data analysis project.\\n",
    "\\n",
    "## Setup\\n",
    "1. Make sure you have activated the virtual environment\\n",
    "2. Install dependencies: `pip install -r requirements.txt`\\n",
    "3. Download data: `python scripts/download_data.py`\\n",
    "\\n",
    "## Quick Analysis\\n",
    "Run the cells below to get started with data analysis.\"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Import required libraries\\n",
    "import pandas as pd\\n",
    "import numpy as np\\n",
    "import sys\\n",
    "sys.path.append('../src')\\n",
    "\\n",
    "from data_loader import EcommerceDataLoader, create_sample_data\\n",
    "from analysis import SalesAnalyzer\\n",
    "from viz_utils import EcommerceVisualizer\\n",
    "\\n",
    "print(\\"🚀 Quick start analysis ready!\\")\"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Load data\\n",
    "try:\\n",
    "    data_loader = EcommerceDataLoader()\\n",
    "    sales_data = data_loader.load_sales_data()\\n",
    "    print(f\\"✅ Loaded data: {sales_data.shape}\\")\\n",
    "except FileNotFoundError:\\n",
    "    print(\\"⚠️  No data found, creating sample data...\\")\\n",
    "    sales_data = create_sample_data()\\n",
    "    print(f\\"✅ Created sample data: {sales_data.shape}\\")\"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Quick analysis\\n",
    "analyzer = SalesAnalyzer(sales_data)\\n",
    "summary = analyzer.get_sales_summary()\\n",
    "\\n",
    "print(\\"📊 Sales Summary:\\")\\n",
    "for key, value in summary.items():\\n",
    "    if key == 'date_range':\\n",
    "        print(f\\"  - {key}: {value['start']} to {value['end']}\\")\\n",
    "    else:\\n",
    "        print(f\\"  - {key}: {value:,.2f}\\")\"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create visualization\\n",
    "visualizer = EcommerceVisualizer(sales_data)\\n",
    "\\n",
    "# Sales trends (if date column exists)\\n",
    "date_columns = [col for col in sales_data.columns if 'date' in col.lower()]\\n",
    "if date_columns:\\n",
    "    fig = visualizer.create_sales_trend_chart(date_column=date_columns[0])\\n",
    "    fig.show()\\n",
    "else:\\n",
    "    print(\\"⚠️  No date column found for trend analysis\\")\"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}"""
    
    with open("notebooks/00_quick_start.ipynb", "w") as f:
        f.write(sample_notebook)
    logger.info("✅ Created quick start notebook")

def main():
    """Main setup function."""
    print("🚀 Setting up E-commerce Sales Data Analysis Project")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Set up directories
    print("\n📁 Setting up project directories...")
    setup_directories()
    
    # Create virtual environment
    print("\n🔧 Setting up virtual environment...")
    if not create_virtual_environment():
        print("⚠️  Virtual environment creation failed. Continuing with system Python...")
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    if not install_dependencies():
        print("⚠️  Dependency installation failed. Please install manually:")
        print("   pip install -r requirements.txt")
    
    # Download data
    print("\n📥 Downloading dataset...")
    if not download_data():
        print("⚠️  Data download failed. You can download manually later:")
        print("   python scripts/download_data.py")
    
    # Create sample notebook
    print("\n📓 Creating sample notebook...")
    create_sample_notebook()
    
    print("\n🎉 Setup complete!")
    print("\n📝 Next Steps:")
    print("1. Activate virtual environment:")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # Unix/Linux/macOS
        print("   source venv/bin/activate")
    print("2. Install dependencies (if not already done):")
    print("   pip install -r requirements.txt")
    print("3. Start Jupyter notebook:")
    print("   jupyter notebook notebooks/")
    print("4. Run the analysis notebooks in order:")
    print("   - 01_data_exploration.ipynb")
    print("   - 02_sales_analysis.ipynb")
    print("   - 03_customer_analysis.ipynb")
    print("   - 04_visualization_dashboard.ipynb")
    print("5. Export visualizations to PNG:")
    print("   python scripts/quick_export.py")
    print("\n📚 For more information, see README.md")

if __name__ == "__main__":
    main() 