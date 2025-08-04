#!/usr/bin/env python3
"""
Quick PNG Export Script

A simple script to quickly export e-commerce visualizations to PNG format.
"""

import sys
import pandas as pd
from pathlib import Path

# Add src to path
sys.path.append('src')

from src.data_loader import create_sample_data
from src.analysis import SalesAnalyzer
from src.viz_utils import EcommerceVisualizer

def quick_export():
    """Quickly export basic visualizations to PNG."""
    print("🚀 Quick PNG Export")
    print("=" * 30)
    
    # Create sample data
    print("📊 Creating sample data...")
    sales_data = create_sample_data()
    
    # Initialize analyzers
    analyzer = SalesAnalyzer(sales_data)
    visualizer = EcommerceVisualizer(sales_data)
    
    # Get KPIs
    kpis = analyzer.calculate_kpis()
    
    # Create output directory
    output_dir = Path("reports/figures")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("🎨 Creating visualizations...")
    
    # 1. Sales Trends
    print("  📈 Sales trends...")
    sales_fig = visualizer.create_sales_trend_chart()
    sales_fig.write_image(str(output_dir / "sales_trends.png"), width=1200, height=600, scale=2)
    print("    ✅ Exported sales_trends.png")
    
    # 2. Product Performance
    print("  📦 Product performance...")
    product_fig = visualizer.create_product_performance_chart()
    product_fig.write_image(str(output_dir / "product_performance.png"), width=1200, height=600, scale=2)
    print("    ✅ Exported product_performance.png")
    
    # 3. KPI Dashboard
    print("  📊 KPI dashboard...")
    kpi_fig = visualizer.create_kpi_dashboard(kpis)
    kpi_fig.write_image(str(output_dir / "kpi_dashboard.png"), width=1200, height=600, scale=2)
    print("    ✅ Exported kpi_dashboard.png")
    
    # 4. Geographic Performance
    print("  🌍 Geographic performance...")
    geo_fig = visualizer.create_geographic_heatmap()
    geo_fig.write_image(str(output_dir / "geographic_performance.png"), width=1200, height=600, scale=2)
    print("    ✅ Exported geographic_performance.png")
    
    print("\n🎉 Export complete!")
    print("📁 Files saved to: reports/figures/")
    print("📊 Files created:")
    print("  - sales_trends.png")
    print("  - product_performance.png")
    print("  - kpi_dashboard.png")
    print("  - geographic_performance.png")

if __name__ == "__main__":
    quick_export() 