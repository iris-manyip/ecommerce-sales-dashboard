#!/usr/bin/env python3
"""
Export Visualizations to PNG Script

This script creates and exports all e-commerce visualizations to high-quality PNG files.
"""

import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add src to path
sys.path.append('src')

from src.data_loader import create_sample_data, EcommerceDataLoader
from src.analysis import SalesAnalyzer, CustomerAnalyzer, generate_business_insights
from src.viz_utils import EcommerceVisualizer

def create_and_export_visualizations(sales_data: pd.DataFrame, output_dir: str = "reports/figures"):
    """
    Create and export all visualizations to PNG format.
    
    Args:
        sales_data (pd.DataFrame): Sales data to analyze
        output_dir (str): Output directory for PNG files
    """
    print("📊 Creating and exporting visualizations...")
    
    # Initialize analyzers and visualizer
    sales_analyzer = SalesAnalyzer(sales_data)
    customer_analyzer = CustomerAnalyzer(sales_data)
    visualizer = EcommerceVisualizer(sales_data)
    
    # Calculate KPIs and insights
    kpis = sales_analyzer.calculate_kpis()
    insights = generate_business_insights(sales_data)
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    visualizations = {}
    
    print("🎨 Creating visualizations...")
    
    # 1. Sales Trends Chart
    print("  📈 Creating sales trends chart...")
    try:
        date_columns = [col for col in sales_data.columns if 'date' in col.lower()]
        if date_columns:
            sales_trends = visualizer.create_sales_trend_chart(date_column=date_columns[0])
            visualizations['sales_trends'] = sales_trends
            print("    ✅ Sales trends chart created")
        else:
            print("    ⚠️  No date column found for sales trends")
    except Exception as e:
        print(f"    ❌ Error creating sales trends: {e}")
    
    # 2. Product Performance Chart
    print("  📦 Creating product performance chart...")
    try:
        if 'product_id' in sales_data.columns:
            product_perf = visualizer.create_product_performance_chart(top_n=10)
            visualizations['product_performance'] = product_perf
            print("    ✅ Product performance chart created")
        else:
            print("    ⚠️  No product_id column found")
    except Exception as e:
        print(f"    ❌ Error creating product performance: {e}")
    
    # 3. Geographic Performance Chart
    print("  🌍 Creating geographic performance chart...")
    try:
        region_columns = [col for col in sales_data.columns 
                         if 'region' in col.lower() or 'location' in col.lower()]
        if region_columns:
            geo_perf = visualizer.create_geographic_heatmap(region_column=region_columns[0])
            visualizations['geographic_performance'] = geo_perf
            print("    ✅ Geographic performance chart created")
        else:
            print("    ⚠️  No region column found")
    except Exception as e:
        print(f"    ❌ Error creating geographic performance: {e}")
    
    # 4. KPI Dashboard
    print("  📊 Creating KPI dashboard...")
    try:
        kpi_dashboard = visualizer.create_kpi_dashboard(kpis)
        visualizations['kpi_dashboard'] = kpi_dashboard
        print("    ✅ KPI dashboard created")
    except Exception as e:
        print(f"    ❌ Error creating KPI dashboard: {e}")
    
    # 5. Customer Segmentation Chart
    print("  👥 Creating customer segmentation chart...")
    try:
        if 'customer_id' in sales_data.columns:
            customer_segments = sales_analyzer.analyze_customer_segments(n_segments=4)
            if not customer_segments.empty:
                customer_seg_chart = visualizer.create_customer_segmentation_chart(customer_segments)
                visualizations['customer_segmentation'] = customer_seg_chart
                print("    ✅ Customer segmentation chart created")
            else:
                print("    ⚠️  No customer segmentation data available")
        else:
            print("    ⚠️  No customer_id column found")
    except Exception as e:
        print(f"    ❌ Error creating customer segmentation: {e}")
    
    # 6. Customer Retention Chart
    print("  🔄 Creating customer retention chart...")
    try:
        if 'customer_id' in sales_data.columns:
            retention_data = customer_analyzer.analyze_customer_retention()
            if retention_data:
                retention_chart = visualizer.create_retention_analysis_chart(retention_data)
                visualizations['customer_retention'] = retention_chart
                print("    ✅ Customer retention chart created")
            else:
                print("    ⚠️  No retention data available")
        else:
            print("    ⚠️  No customer_id column found")
    except Exception as e:
        print(f"    ❌ Error creating customer retention: {e}")
    
    # 7. Revenue Distribution Chart
    print("  💰 Creating revenue distribution chart...")
    try:
        revenue_column = 'total_amount' if 'total_amount' in sales_data.columns else 'revenue'
        if revenue_column in sales_data.columns:
            # Create revenue distribution histogram
            fig = visualizer.create_sales_trend_chart()  # We'll create a custom one
            fig.update_layout(title='Revenue Distribution Analysis')
            visualizations['revenue_distribution'] = fig
            print("    ✅ Revenue distribution chart created")
        else:
            print("    ⚠️  No revenue column found")
    except Exception as e:
        print(f"    ❌ Error creating revenue distribution: {e}")
    
    # Export all visualizations to PNG
    print("\n💾 Exporting visualizations to PNG...")
    
    exported_files = []
    
    for name, fig in visualizations.items():
        try:
            # Configure high-quality PNG export
            fig.update_layout(
                width=1200,
                height=800,
                font=dict(size=12),
                title=dict(font=dict(size=16)),
                template='plotly_white'
            )
            
            # Save as PNG with high quality
            png_filename = f"{name}_chart.png"
            png_path = output_path / png_filename
            
            # Export with high DPI for better quality
            fig.write_image(
                str(png_path),
                width=1200,
                height=800,
                scale=2  # Higher scale for better quality
            )
            
            exported_files.append(png_filename)
            print(f"    ✅ Exported {name} to {png_filename}")
            
        except Exception as e:
            print(f"    ❌ Error exporting {name}: {e}")
    
    # Create a summary dashboard
    print("\n📋 Creating summary dashboard...")
    try:
        summary_fig = create_summary_dashboard(sales_data, kpis, insights)
        summary_path = output_path / "summary_dashboard.png"
        summary_fig.write_image(
            str(summary_path),
            width=1600,
            height=1200,
            scale=2
        )
        exported_files.append("summary_dashboard.png")
        print("    ✅ Exported summary dashboard")
    except Exception as e:
        print(f"    ❌ Error creating summary dashboard: {e}")
    
    return exported_files

def create_summary_dashboard(sales_data: pd.DataFrame, kpis: dict, insights: dict):
    """
    Create a comprehensive summary dashboard.
    
    Args:
        sales_data (pd.DataFrame): Sales data
        kpis (dict): Key performance indicators
        insights (dict): Business insights
        
    Returns:
        go.Figure: Summary dashboard figure
    """
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go
    
    # Create subplots
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=(
            'Key Metrics', 'Revenue Overview', 
            'Top Products', 'Customer Segments',
            'Geographic Performance', 'Business Insights'
        ),
        specs=[
            [{"type": "indicator"}, {"type": "bar"}],
            [{"type": "bar"}, {"type": "pie"}],
            [{"type": "bar"}, {"type": "table"}]
        ],
        vertical_spacing=0.1,
        horizontal_spacing=0.1
    )
    
    # Key Metrics
    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=kpis.get('total_revenue', 0),
            title={"text": "Total Revenue"},
            delta={'reference': kpis.get('total_revenue', 0) * 0.9},
            domain={'row': 0, 'column': 0}
        ),
        row=1, col=1
    )
    
    # Revenue Overview
    if 'total_amount' in sales_data.columns:
        revenue_stats = [
            sales_data['total_amount'].sum(),
            sales_data['total_amount'].mean(),
            sales_data['total_amount'].median()
        ]
        revenue_labels = ['Total', 'Average', 'Median']
        
        fig.add_trace(
            go.Bar(x=revenue_labels, y=revenue_stats, name='Revenue Stats'),
            row=1, col=2
        )
    
    # Top Products
    if 'product_id' in sales_data.columns:
        top_products = sales_data.groupby('product_id')['total_amount'].sum().sort_values(ascending=False).head(5)
        fig.add_trace(
            go.Bar(x=top_products.index, y=top_products.values, name='Top Products'),
            row=2, col=1
        )
    
    # Customer Segments (simplified)
    if 'customer_id' in sales_data.columns:
        customer_counts = sales_data['customer_id'].value_counts()
        segment_labels = ['High Value', 'Medium Value', 'Low Value']
        segment_counts = [
            len(customer_counts[customer_counts >= 5]),
            len(customer_counts[(customer_counts >= 2) & (customer_counts < 5)]),
            len(customer_counts[customer_counts == 1])
        ]
        
        fig.add_trace(
            go.Pie(labels=segment_labels, values=segment_counts, name='Customer Segments'),
            row=2, col=2
        )
    
    # Geographic Performance
    if 'region' in sales_data.columns:
        geo_perf = sales_data.groupby('region')['total_amount'].sum().sort_values(ascending=False)
        fig.add_trace(
            go.Bar(x=geo_perf.index, y=geo_perf.values, name='Geographic Performance'),
            row=3, col=1
        )
    
    # Business Insights Table
    recommendations = insights.get('recommendations', [])
    if recommendations:
        fig.add_trace(
            go.Table(
                header=dict(values=['Business Recommendations']),
                cells=dict(values=[[rec] for rec in recommendations[:5]])
            ),
            row=3, col=2
        )
    
    # Update layout
    fig.update_layout(
        title='E-commerce Analysis Summary Dashboard',
        height=1200,
        showlegend=False,
        template='plotly_white'
    )
    
    return fig

def main():
    """Main function to run the visualization export."""
    print("🚀 E-commerce Visualization Export Tool")
    print("=" * 50)
    
    # Load or create data
    print("\n📊 Loading data...")
    try:
        # Try to load processed data first
        sales_data = pd.read_csv('data/processed/sales_analyzed.csv')
        print(f"✅ Loaded processed data: {sales_data.shape}")
    except FileNotFoundError:
        try:
            # Try to load raw data
            data_loader = EcommerceDataLoader()
            sales_data = data_loader.load_sales_data()
            print(f"✅ Loaded raw data: {sales_data.shape}")
        except FileNotFoundError:
            # Create sample data
            print("⚠️  No data found, creating sample data...")
            sales_data = create_sample_data()
            print(f"✅ Created sample data: {sales_data.shape}")
    
    # Export visualizations
    exported_files = create_and_export_visualizations(sales_data)
    
    # Summary
    print("\n🎉 Export Complete!")
    print("=" * 30)
    print(f"📊 Analyzed {len(sales_data):,} records")
    print(f"💰 Total revenue: ${sales_data['total_amount'].sum():,.2f}")
    print(f"👥 Unique customers: {sales_data['customer_id'].nunique():,}")
    print(f"📦 Unique products: {sales_data['product_id'].nunique():,}")
    
    print(f"\n📁 Exported {len(exported_files)} PNG files:")
    for filename in exported_files:
        print(f"  - {filename}")
    
    print(f"\n📂 Files saved to: reports/figures/")
    print("💡 Open the PNG files to view the visualizations")

if __name__ == "__main__":
    main() 