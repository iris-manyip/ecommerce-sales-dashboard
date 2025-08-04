#!/bin/bash
# Virtual Environment Activation Script for E-commerce Data Analysis

echo "🚀 E-commerce Data Analysis Environment Setup"
echo "=============================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📁 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if ! python -c "import pandas" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
else
    echo "✅ Dependencies already installed"
fi

echo ""
echo "🎉 Environment is ready!"
echo ""
echo "📝 Available commands:"
echo "  - jupyter notebook notebooks/     # Start Jupyter notebooks"
echo "  - python scripts/quick_export.py  # Export basic charts to PNG"
echo "  - python scripts/export_visualizations.py  # Export all charts to PNG"
echo "  - python scripts/download_data.py # Download Kaggle dataset"
echo ""
echo "💡 Your virtual environment is now active!"
echo "   To deactivate later, run: deactivate" 