"""
Visualization Utilities for E-commerce Sales Data

This module provides comprehensive visualization functions for creating
charts, dashboards, and interactive plots for e-commerce sales analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from typing import Dict, List, Optional, Tuple
import logging

# Set up plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

logger = logging.getLogger(__name__)

class EcommerceVisualizer:
    """
    A class for creating comprehensive visualizations for e-commerce sales data.
    """
    
    def __init__(self, sales_data: pd.DataFrame):
        """
        Initialize the visualizer.
        
        Args:
            sales_data (pd.DataFrame): Sales transaction data
        """
        self.sales_data = sales_data.copy()
        self._preprocess_data()
        
    def _preprocess_data(self):
        """
        Preprocess data for visualization.
        """
        # Convert date columns
        date_columns = [col for col in self.sales_data.columns if 'date' in col.lower()]
        for col in date_columns:
            try:
                self.sales_data[col] = pd.to_datetime(self.sales_data[col])
            except:
                pass
                
        # Ensure numeric columns are properly typed
        numeric_columns = ['quantity', 'unit_price', 'total_amount', 'revenue']
        for col in numeric_columns:
            if col in self.sales_data.columns:
                self.sales_data[col] = pd.to_numeric(self.sales_data[col], errors='coerce')
    
    def create_sales_trend_chart(self, date_column: str = 'order_date', 
                                freq: str = 'D', figsize: Tuple[int, int] = (12, 6)) -> go.Figure:
        """
        Create an interactive sales trend chart.
        
        Args:
            date_column (str): Name of the date column
            freq (str): Frequency for resampling
            figsize (Tuple[int, int]): Figure size
            
        Returns:
            go.Figure: Plotly figure object
        """
        if date_column not in self.sales_data.columns:
            logger.warning(f"Date column '{date_column}' not found")
            return go.Figure()
            
        # Prepare time series data
        self.sales_data[date_column] = pd.to_datetime(self.sales_data[date_column])
        
        # Group by date
        daily_sales = self.sales_data.groupby(pd.Grouper(key=date_column, freq=freq)).agg({
            'total_amount': 'sum',
            'order_id': 'count'
        }).fillna(0)
        
        daily_sales.columns = ['revenue', 'order_count']
        
        # Create figure
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Daily Revenue', 'Daily Order Count'),
            vertical_spacing=0.1
        )
        
        # Revenue line
        fig.add_trace(
            go.Scatter(
                x=daily_sales.index,
                y=daily_sales['revenue'],
                mode='lines+markers',
                name='Revenue',
                line=dict(color='#1f77b4', width=2),
                marker=dict(size=4)
            ),
            row=1, col=1
        )
        
        # Order count line
        fig.add_trace(
            go.Scatter(
                x=daily_sales.index,
                y=daily_sales['order_count'],
                mode='lines+markers',
                name='Order Count',
                line=dict(color='#ff7f0e', width=2),
                marker=dict(size=4)
            ),
            row=2, col=1
        )
        
        # Update layout
        fig.update_layout(
            title='Sales Trends Over Time',
            height=600,
            showlegend=True,
            hovermode='x unified'
        )
        
        return fig
    
    def create_product_performance_chart(self, top_n: int = 10) -> go.Figure:
        """
        Create a product performance visualization.
        
        Args:
            top_n (int): Number of top products to show
            
        Returns:
            go.Figure: Plotly figure object
        """
        if 'product_id' not in self.sales_data.columns:
            logger.warning("Product ID column not found")
            return go.Figure()
            
        # Calculate product performance
        product_performance = self.sales_data.groupby('product_id').agg({
            'total_amount': 'sum',
            'quantity': 'sum',
            'order_id': 'count'
        }).fillna(0)
        
        product_performance.columns = ['total_revenue', 'total_quantity', 'order_count']
        product_performance = product_performance.sort_values('total_revenue', ascending=False).head(top_n)
        
        # Create figure
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Top Products by Revenue', 'Revenue vs Order Count'),
            specs=[[{"type": "bar"}, {"type": "scatter"}]]
        )
        
        # Bar chart
        fig.add_trace(
            go.Bar(
                x=product_performance.index,
                y=product_performance['total_revenue'],
                name='Revenue',
                marker_color='#1f77b4'
            ),
            row=1, col=1
        )
        
        # Scatter plot
        fig.add_trace(
            go.Scatter(
                x=product_performance['order_count'],
                y=product_performance['total_revenue'],
                mode='markers+text',
                text=product_performance.index,
                textposition="top center",
                name='Revenue vs Orders',
                marker=dict(
                    size=product_performance['total_quantity'] / 100,
                    color=product_performance['total_revenue'],
                    colorscale='Viridis',
                    showscale=True
                )
            ),
            row=1, col=2
        )
        
        # Update layout
        fig.update_layout(
            title=f'Top {top_n} Products Performance',
            height=500,
            showlegend=False
        )
        
        return fig
    
    def create_customer_segmentation_chart(self, customer_data: pd.DataFrame) -> go.Figure:
        """
        Create customer segmentation visualization.
        
        Args:
            customer_data (pd.DataFrame): Customer segmentation data
            
        Returns:
            go.Figure: Plotly figure object
        """
        if customer_data.empty:
            logger.warning("Customer data is empty")
            return go.Figure()
            
        # Create figure
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Customer Segments Distribution', 'Revenue by Segment',
                          'Order Count by Segment', 'Average Order Value by Segment'),
            specs=[[{"type": "pie"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )
        
        # Pie chart for segment distribution
        segment_counts = customer_data['segment'].value_counts()
        fig.add_trace(
            go.Pie(
                labels=segment_counts.index,
                values=segment_counts.values,
                name="Segments"
            ),
            row=1, col=1
        )
        
        # Bar charts for segment metrics
        segment_metrics = customer_data.groupby('segment').agg({
            'total_spent': 'mean',
            'order_count': 'mean',
            'avg_order_value': 'mean'
        })
        
        # Revenue by segment
        fig.add_trace(
            go.Bar(
                x=segment_metrics.index,
                y=segment_metrics['total_spent'],
                name='Avg Revenue',
                marker_color='#1f77b4'
            ),
            row=1, col=2
        )
        
        # Order count by segment
        fig.add_trace(
            go.Bar(
                x=segment_metrics.index,
                y=segment_metrics['order_count'],
                name='Avg Orders',
                marker_color='#ff7f0e'
            ),
            row=2, col=1
        )
        
        # Average order value by segment
        fig.add_trace(
            go.Bar(
                x=segment_metrics.index,
                y=segment_metrics['avg_order_value'],
                name='Avg Order Value',
                marker_color='#2ca02c'
            ),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title='Customer Segmentation Analysis',
            height=600,
            showlegend=False
        )
        
        return fig
    
    def create_geographic_heatmap(self, region_column: str = 'region') -> go.Figure:
        """
        Create a geographic performance heatmap.
        
        Args:
            region_column (str): Name of the region column
            
        Returns:
            go.Figure: Plotly figure object
        """
        if region_column not in self.sales_data.columns:
            logger.warning(f"Region column '{region_column}' not found")
            return go.Figure()
            
        # Calculate regional performance
        regional_performance = self.sales_data.groupby(region_column).agg({
            'total_amount': 'sum',
            'order_id': 'count',
            'customer_id': 'nunique'
        }).fillna(0)
        
        regional_performance.columns = ['total_revenue', 'order_count', 'unique_customers']
        
        # Create heatmap data
        heatmap_data = regional_performance.values
        
        # Create figure
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            x=['Revenue', 'Orders', 'Customers'],
            y=regional_performance.index,
            colorscale='Viridis',
            text=heatmap_data.round(0),
            texttemplate="%{text}",
            textfont={"size": 10},
            hoverongaps=False
        ))
        
        # Update layout
        fig.update_layout(
            title='Geographic Performance Heatmap',
            xaxis_title='Metrics',
            yaxis_title='Regions',
            height=400
        )
        
        return fig
    
    def create_kpi_dashboard(self, kpis: Dict) -> go.Figure:
        """
        Create a KPI dashboard with key metrics.
        
        Args:
            kpis (Dict): Dictionary of KPIs
            
        Returns:
            go.Figure: Plotly figure object
        """
        # Create subplots for KPIs
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Total Revenue', 'Average Order Value', 
                          'Unique Customers', 'Total Orders'),
            specs=[[{"type": "indicator"}, {"type": "indicator"}],
                   [{"type": "indicator"}, {"type": "indicator"}]]
        )
        
        # Revenue indicator
        fig.add_trace(
            go.Indicator(
                mode="number+delta",
                value=kpis.get('total_revenue', 0),
                title={"text": "Total Revenue"},
                delta={'reference': kpis.get('total_revenue', 0) * 0.9},
                gauge={'axis': {'visible': False}},
                domain={'row': 0, 'column': 0}
            ),
            row=1, col=1
        )
        
        # Average order value indicator
        fig.add_trace(
            go.Indicator(
                mode="number+delta",
                value=kpis.get('avg_order_value', 0),
                title={"text": "Avg Order Value"},
                delta={'reference': kpis.get('avg_order_value', 0) * 0.9},
                gauge={'axis': {'visible': False}},
                domain={'row': 0, 'column': 1}
            ),
            row=1, col=2
        )
        
        # Customer count indicator
        fig.add_trace(
            go.Indicator(
                mode="number+delta",
                value=kpis.get('unique_customers', 0),
                title={"text": "Unique Customers"},
                delta={'reference': kpis.get('unique_customers', 0) * 0.9},
                gauge={'axis': {'visible': False}},
                domain={'row': 1, 'column': 0}
            ),
            row=2, col=1
        )
        
        # Order count indicator
        fig.add_trace(
            go.Indicator(
                mode="number+delta",
                value=kpis.get('total_orders', 0),
                title={"text": "Total Orders"},
                delta={'reference': kpis.get('total_orders', 0) * 0.9},
                gauge={'axis': {'visible': False}},
                domain={'row': 1, 'column': 1}
            ),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title='Key Performance Indicators',
            height=500,
            showlegend=False
        )
        
        return fig
    
    def create_retention_analysis_chart(self, retention_data: Dict) -> go.Figure:
        """
        Create customer retention analysis visualization.
        
        Args:
            retention_data (Dict): Customer retention analysis data
            
        Returns:
            go.Figure: Plotly figure object
        """
        # Create figure
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Customer Retention Metrics', 'Customer Distribution'),
            specs=[[{"type": "bar"}, {"type": "pie"}]]
        )
        
        # Bar chart for retention metrics
        metrics = ['Total Customers', 'Repeat Customers', 'Active Customers']
        values = [
            retention_data.get('total_customers', 0),
            retention_data.get('repeat_customers', 0),
            retention_data.get('active_customers', 0)
        ]
        
        fig.add_trace(
            go.Bar(
                x=metrics,
                y=values,
                marker_color=['#1f77b4', '#ff7f0e', '#2ca02c']
            ),
            row=1, col=1
        )
        
        # Pie chart for customer distribution
        customer_types = ['New Customers', 'Repeat Customers', 'Active Customers']
        customer_counts = [
            retention_data.get('total_customers', 0) - retention_data.get('repeat_customers', 0),
            retention_data.get('repeat_customers', 0),
            retention_data.get('active_customers', 0)
        ]
        
        fig.add_trace(
            go.Pie(
                labels=customer_types,
                values=customer_counts,
                hole=0.3
            ),
            row=1, col=2
        )
        
        # Update layout
        fig.update_layout(
            title='Customer Retention Analysis',
            height=400,
            showlegend=False
        )
        
        return fig
    
    def save_figure(self, fig: go.Figure, filename: str, 
                   output_dir: str = "reports/figures"):
        """
        Save a Plotly figure to HTML and PNG formats.
        
        Args:
            fig (go.Figure): Plotly figure to save
            filename (str): Base filename
            output_dir (str): Output directory
        """
        import os
        from pathlib import Path
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save as HTML
        html_path = output_path / f"{filename}.html"
        fig.write_html(str(html_path))
        logger.info(f"Saved interactive chart to {html_path}")
        
        # Save as PNG
        png_path = output_path / f"{filename}.png"
        fig.write_image(str(png_path))
        logger.info(f"Saved static chart to {png_path}")

def create_sample_visualizations(sales_data: pd.DataFrame) -> Dict[str, go.Figure]:
    """
    Create a comprehensive set of sample visualizations.
    
    Args:
        sales_data (pd.DataFrame): Sales data
        
    Returns:
        Dict[str, go.Figure]: Dictionary of visualization figures
    """
    visualizer = EcommerceVisualizer(sales_data)
    
    visualizations = {}
    
    # Sales trends
    visualizations['sales_trends'] = visualizer.create_sales_trend_chart()
    
    # Product performance
    visualizations['product_performance'] = visualizer.create_product_performance_chart()
    
    # Geographic performance
    visualizations['geographic_performance'] = visualizer.create_geographic_heatmap()
    
    # KPI dashboard
    from src.analysis import SalesAnalyzer
    analyzer = SalesAnalyzer(sales_data)
    kpis = analyzer.calculate_kpis()
    visualizations['kpi_dashboard'] = visualizer.create_kpi_dashboard(kpis)
    
    return visualizations 