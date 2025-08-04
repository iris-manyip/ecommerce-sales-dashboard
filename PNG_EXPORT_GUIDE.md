# 📊 PNG Export Guide

This guide shows you how to export e-commerce visualizations to high-quality PNG files.

## 🎯 Quick Export

### Method 1: Quick Export Script
```bash
# 1. Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run quick export
python scripts/quick_export.py
```

This will create:
- `sales_trends.png`
- `product_performance.png`
- `kpi_dashboard.png`
- `geographic_performance.png`

### Method 2: Comprehensive Export
```bash
# 1. Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run full export with all visualizations
python scripts/export_visualizations.py
```

This creates all available visualizations including:
- Sales trends
- Product performance
- Customer segmentation
- Geographic analysis
- KPI dashboard
- Customer retention
- Summary dashboard

## 🛠️ Manual Export

### Step 1: Activate Virtual Environment and Install Dependencies
```bash
# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

**Important:** Make sure `kaleido` is installed for PNG export:
```bash
pip install kaleido
```

### Step 2: Create Visualizations
```python
import sys
sys.path.append('src')

from src.data_loader import create_sample_data
from src.analysis import SalesAnalyzer
from src.viz_utils import EcommerceVisualizer

# Load data
sales_data = create_sample_data()

# Create visualizer
visualizer = EcommerceVisualizer(sales_data)

# Create charts
sales_fig = visualizer.create_sales_trend_chart()
product_fig = visualizer.create_product_performance_chart()
```

### Step 3: Export to PNG
```python
# High-quality PNG export
sales_fig.write_image(
    "sales_trends.png",
    width=1200,
    height=800,
    scale=2  # Higher scale for better quality
)

product_fig.write_image(
    "product_performance.png",
    width=1200,
    height=800,
    scale=2
)
```

## 📊 Available Visualizations

### 1. Sales Trends Chart
```python
fig = visualizer.create_sales_trend_chart()
fig.write_image("sales_trends.png", width=1200, height=600, scale=2)
```

### 2. Product Performance Chart
```python
fig = visualizer.create_product_performance_chart(top_n=10)
fig.write_image("product_performance.png", width=1200, height=600, scale=2)
```

### 3. KPI Dashboard
```python
kpis = analyzer.calculate_kpis()
fig = visualizer.create_kpi_dashboard(kpis)
fig.write_image("kpi_dashboard.png", width=1200, height=600, scale=2)
```

### 4. Geographic Performance
```python
fig = visualizer.create_geographic_heatmap()
fig.write_image("geographic_performance.png", width=1200, height=600, scale=2)
```

### 5. Customer Segmentation
```python
customer_segments = analyzer.analyze_customer_segments()
fig = visualizer.create_customer_segmentation_chart(customer_segments)
fig.write_image("customer_segmentation.png", width=1200, height=800, scale=2)
```

### 6. Customer Retention
```python
retention_data = customer_analyzer.analyze_customer_retention()
fig = visualizer.create_retention_analysis_chart(retention_data)
fig.write_image("customer_retention.png", width=1200, height=600, scale=2)
```

## 🎨 Customization Options

### High-Quality Export Settings
```python
# Configure for high-quality PNG
fig.update_layout(
    width=1200,
    height=800,
    font=dict(size=12),
    title=dict(font=dict(size=16)),
    template='plotly_white'
)

# Export with high DPI
fig.write_image(
    "chart.png",
    width=1200,
    height=800,
    scale=2  # 2x scale for better quality
)
```

### Different Sizes
```python
# Standard size
fig.write_image("standard.png", width=800, height=600, scale=1)

# Large size
fig.write_image("large.png", width=1600, height=1200, scale=2)

# Presentation size
fig.write_image("presentation.png", width=1920, height=1080, scale=2)
```

### Custom Styling
```python
# Apply custom styling before export
fig.update_layout(
    title="Custom Title",
    font=dict(family="Arial", size=14),
    plot_bgcolor='white',
    paper_bgcolor='white'
)

fig.write_image("styled_chart.png", width=1200, height=800, scale=2)
```

## 📁 Output Organization

### Recommended File Structure
```
reports/
├── figures/
│   ├── sales_trends.png
│   ├── product_performance.png
│   ├── kpi_dashboard.png
│   ├── geographic_performance.png
│   ├── customer_segmentation.png
│   ├── customer_retention.png
│   └── summary_dashboard.png
└── insights/
    └── analysis_insights.json
```

### Batch Export Script
```python
import os
from pathlib import Path

# Create output directory
output_dir = Path("reports/figures")
output_dir.mkdir(parents=True, exist_ok=True)

# Export all visualizations
visualizations = {
    'sales_trends': sales_fig,
    'product_performance': product_fig,
    'kpi_dashboard': kpi_fig,
    'geographic_performance': geo_fig
}

for name, fig in visualizations.items():
    png_path = output_dir / f"{name}.png"
    fig.write_image(str(png_path), width=1200, height=800, scale=2)
    print(f"✅ Exported {name}.png")
```

## 🔧 Troubleshooting

### Common Issues

1. **"No module named 'kaleido'"**
   ```bash
   pip install kaleido
   ```

2. **"No module named 'pandas'"**
   ```bash
   pip install -r requirements.txt
   ```

3. **Low quality images**
   ```python
   # Increase scale for better quality
   fig.write_image("chart.png", scale=3)
   ```

4. **Large file sizes**
   ```python
   # Reduce scale for smaller files
   fig.write_image("chart.png", scale=1)
   ```

### Performance Tips

1. **Use appropriate sizes:**
   - Web: 800x600, scale=1
   - Print: 1200x800, scale=2
   - Presentation: 1920x1080, scale=2

2. **Optimize for your use case:**
   ```python
   # For web
   fig.write_image("web_chart.png", width=800, height=600, scale=1)
   
   # For print
   fig.write_image("print_chart.png", width=1200, height=800, scale=2)
   
   # For high-res display
   fig.write_image("high_res_chart.png", width=1600, height=1200, scale=3)
   ```

## 📈 Example Output

After running the export scripts, you'll get PNG files like:

- **sales_trends.png** - Time series of sales data
- **product_performance.png** - Top products by revenue
- **kpi_dashboard.png** - Key performance indicators
- **geographic_performance.png** - Regional sales heatmap
- **customer_segmentation.png** - Customer clusters
- **customer_retention.png** - Retention analysis
- **summary_dashboard.png** - Comprehensive overview

## 🚀 Quick Start Commands

```bash
# 1. Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Quick export (4 basic charts)
python scripts/quick_export.py

# 4. Full export (all charts + summary)
python scripts/export_visualizations.py

# 5. Check results
ls reports/figures/*.png
```

## 📊 Quality Settings

| Use Case | Width | Height | Scale | File Size |
|----------|-------|--------|-------|-----------|
| Web | 800 | 600 | 1 | ~200KB |
| Print | 1200 | 800 | 2 | ~500KB |
| Presentation | 1600 | 1200 | 2 | ~800KB |
| High-res | 1920 | 1080 | 3 | ~1.5MB |

---

🎉 **You're ready to export high-quality PNG visualizations!** Start with `python scripts/quick_export.py` for a quick test. 