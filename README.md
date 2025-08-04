# E-commerce Sales Data Analysis & Visualization Dashboard

A comprehensive data analysis and visualization project for e-commerce sales data from Kaggle. This repository provides insights into sales patterns, customer behavior, and business performance through interactive visualizations and detailed analysis.

## 📊 Dataset

This project analyzes the "Unlock Profits with E-commerce Sales Data" dataset from Kaggle, which contains comprehensive e-commerce sales information including:
- Sales transactions
- Customer demographics
- Product information
- Geographic data
- Temporal patterns

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ecommerce-sales-dashboard
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download the dataset**
   ```bash
   python scripts/download_data.py
   ```

5. **Run the analysis**
   ```bash
   jupyter notebook notebooks/
   ```

6. **Export visualizations to PNG**
   ```bash
   python scripts/quick_export.py
   ```

## 📁 Project Structure

```
ecommerce-sales-dashboard/
├── data/                   # Raw and processed data
│   ├── raw/               # Original dataset files
│   └── processed/         # Cleaned and processed data
├── notebooks/             # Jupyter notebooks for analysis
│   ├── 01_data_exploration.ipynb
│   ├── 02_sales_analysis.ipynb
│   ├── 03_customer_analysis.ipynb
│   └── 04_visualization_dashboard.ipynb
├── scripts/               # Python scripts
│   ├── download_data.py   # Dataset download script
│   ├── data_processing.py # Data cleaning and processing
│   └── visualization.py   # Visualization utilities
├── src/                   # Source code modules
│   ├── __init__.py
│   ├── data_loader.py     # Data loading utilities
│   ├── analysis.py        # Analysis functions
│   └── viz_utils.py       # Visualization utilities
├── reports/               # Generated reports and outputs
│   ├── figures/           # Saved plots and charts
│   └── insights/          # Analysis insights and summaries
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🔍 Analysis Components

### 1. Data Exploration
- Dataset overview and statistics
- Data quality assessment
- Missing value analysis
- Data type verification

### 2. Sales Analysis
- Revenue trends and patterns
- Product performance analysis
- Geographic sales distribution
- Seasonal patterns and trends

### 3. Customer Analysis
- Customer segmentation
- Purchase behavior analysis
- Customer lifetime value
- Retention analysis

### 4. Visualization Dashboard
- Interactive dashboards using Plotly
- Key performance indicators (KPIs)
- Sales forecasting models
- Business insights and recommendations

## 📈 Key Features

- **Interactive Visualizations**: Plotly-based interactive charts and dashboards
- **Comprehensive Analysis**: From basic statistics to advanced predictive modeling
- **Modular Code**: Reusable functions and utilities
- **Documentation**: Detailed explanations and insights
- **Export Capabilities**: Generate reports and visualizations for presentations

## 🛠️ Usage

### Running Analysis Notebooks
```bash
jupyter notebook notebooks/01_data_exploration.ipynb
```

### Generating Visualizations
```bash
python scripts/visualization.py
```

### Creating Reports
```bash
python scripts/generate_report.py
```

## 📊 Sample Visualizations

The project includes various types of visualizations:
- Time series analysis of sales trends
- Geographic heatmaps of sales distribution
- Customer segmentation clusters
- Product performance comparisons
- Interactive dashboards with filters

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Dataset provided by [The Devastator](https://www.kaggle.com/thedevastator) on Kaggle
- Built with Python data science ecosystem (pandas, numpy, matplotlib, seaborn, plotly)

## 📞 Contact

For questions or suggestions, please open an issue in this repository.