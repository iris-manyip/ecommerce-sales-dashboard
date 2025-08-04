"""
Analysis Functions for E-commerce Sales Data

This module provides comprehensive analysis functions for e-commerce sales data,
including sales analysis, customer analysis, and business insights.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime, timedelta
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

class SalesAnalyzer:
    """
    A class for analyzing sales data and generating insights.
    """
    
    def __init__(self, sales_data: pd.DataFrame):
        """
        Initialize the sales analyzer.
        
        Args:
            sales_data (pd.DataFrame): Sales transaction data
        """
        self.sales_data = sales_data.copy()
        self._preprocess_data()
        
    def _preprocess_data(self):
        """
        Preprocess the sales data for analysis.
        """
        # Convert date columns if they exist
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
    
    def get_sales_summary(self) -> Dict:
        """
        Get a comprehensive summary of sales data.
        
        Returns:
            Dict: Sales summary statistics
        """
        summary = {
            'total_orders': len(self.sales_data),
            'total_revenue': self.sales_data.get('total_amount', pd.Series([0])).sum(),
            'avg_order_value': self.sales_data.get('total_amount', pd.Series([0])).mean(),
            'unique_customers': self.sales_data.get('customer_id', pd.Series([0])).nunique(),
            'unique_products': self.sales_data.get('product_id', pd.Series([0])).nunique(),
            'date_range': {
                'start': self.sales_data.get('order_date', pd.Series([pd.Timestamp.now()])).min(),
                'end': self.sales_data.get('order_date', pd.Series([pd.Timestamp.now()])).max()
            }
        }
        
        return summary
    
    def analyze_sales_trends(self, date_column: str = 'order_date', 
                           freq: str = 'D') -> pd.DataFrame:
        """
        Analyze sales trends over time.
        
        Args:
            date_column (str): Name of the date column
            freq (str): Frequency for resampling ('D', 'W', 'M', 'Q', 'Y')
            
        Returns:
            pd.DataFrame: Time series analysis of sales
        """
        if date_column not in self.sales_data.columns:
            logger.warning(f"Date column '{date_column}' not found")
            return pd.DataFrame()
            
        # Create time series
        self.sales_data[date_column] = pd.to_datetime(self.sales_data[date_column])
        
        # Group by date and calculate metrics
        daily_sales = self.sales_data.groupby(pd.Grouper(key=date_column, freq=freq)).agg({
            'total_amount': ['sum', 'mean', 'count'],
            'quantity': 'sum'
        }).fillna(0)
        
        daily_sales.columns = ['revenue', 'avg_order_value', 'order_count', 'total_quantity']
        
        return daily_sales
    
    def analyze_product_performance(self, top_n: int = 10) -> pd.DataFrame:
        """
        Analyze product performance metrics.
        
        Args:
            top_n (int): Number of top products to return
            
        Returns:
            pd.DataFrame: Product performance analysis
        """
        if 'product_id' not in self.sales_data.columns:
            logger.warning("Product ID column not found")
            return pd.DataFrame()
            
        product_analysis = self.sales_data.groupby('product_id').agg({
            'total_amount': ['sum', 'mean', 'count'],
            'quantity': 'sum'
        }).fillna(0)
        
        product_analysis.columns = ['total_revenue', 'avg_order_value', 'order_count', 'total_quantity']
        product_analysis = product_analysis.sort_values('total_revenue', ascending=False)
        
        return product_analysis.head(top_n)
    
    def analyze_customer_segments(self, n_segments: int = 4) -> pd.DataFrame:
        """
        Perform customer segmentation based on purchase behavior.
        
        Args:
            n_segments (int): Number of customer segments to create
            
        Returns:
            pd.DataFrame: Customer segmentation results
        """
        if 'customer_id' not in self.sales_data.columns:
            logger.warning("Customer ID column not found")
            return pd.DataFrame()
            
        # Calculate customer metrics
        customer_metrics = self.sales_data.groupby('customer_id').agg({
            'total_amount': ['sum', 'mean', 'count'],
            'order_date': ['min', 'max']
        }).fillna(0)
        
        customer_metrics.columns = ['total_spent', 'avg_order_value', 'order_count', 
                                 'first_order', 'last_order']
        
        # Calculate additional metrics
        customer_metrics['days_since_first'] = (pd.Timestamp.now() - 
                                              customer_metrics['first_order']).dt.days
        customer_metrics['days_since_last'] = (pd.Timestamp.now() - 
                                             customer_metrics['last_order']).dt.days
        
        # Prepare features for clustering
        features = ['total_spent', 'avg_order_value', 'order_count', 
                   'days_since_first', 'days_since_last']
        
        X = customer_metrics[features].fillna(0)
        
        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Perform clustering
        kmeans = KMeans(n_clusters=n_segments, random_state=42)
        customer_metrics['segment'] = kmeans.fit_predict(X_scaled)
        
        return customer_metrics
    
    def analyze_geographic_performance(self, region_column: str = 'region') -> pd.DataFrame:
        """
        Analyze sales performance by geographic region.
        
        Args:
            region_column (str): Name of the region column
            
        Returns:
            pd.DataFrame: Geographic performance analysis
        """
        if region_column not in self.sales_data.columns:
            logger.warning(f"Region column '{region_column}' not found")
            return pd.DataFrame()
            
        geo_analysis = self.sales_data.groupby(region_column).agg({
            'total_amount': ['sum', 'mean', 'count'],
            'customer_id': 'nunique',
            'product_id': 'nunique'
        }).fillna(0)
        
        geo_analysis.columns = ['total_revenue', 'avg_order_value', 'order_count', 
                              'unique_customers', 'unique_products']
        
        return geo_analysis.sort_values('total_revenue', ascending=False)
    
    def calculate_kpis(self) -> Dict:
        """
        Calculate key performance indicators.
        
        Returns:
            Dict: Dictionary of KPIs
        """
        kpis = {}
        
        # Revenue KPIs
        total_revenue = self.sales_data.get('total_amount', pd.Series([0])).sum()
        kpis['total_revenue'] = total_revenue
        kpis['avg_order_value'] = self.sales_data.get('total_amount', pd.Series([0])).mean()
        
        # Customer KPIs
        unique_customers = self.sales_data.get('customer_id', pd.Series([0])).nunique()
        kpis['unique_customers'] = unique_customers
        kpis['revenue_per_customer'] = total_revenue / unique_customers if unique_customers > 0 else 0
        
        # Product KPIs
        unique_products = self.sales_data.get('product_id', pd.Series([0])).nunique()
        kpis['unique_products'] = unique_products
        kpis['revenue_per_product'] = total_revenue / unique_products if unique_products > 0 else 0
        
        # Order KPIs
        total_orders = len(self.sales_data)
        kpis['total_orders'] = total_orders
        kpis['orders_per_customer'] = total_orders / unique_customers if unique_customers > 0 else 0
        
        return kpis

class CustomerAnalyzer:
    """
    A class for analyzing customer behavior and patterns.
    """
    
    def __init__(self, sales_data: pd.DataFrame):
        """
        Initialize the customer analyzer.
        
        Args:
            sales_data (pd.DataFrame): Sales transaction data
        """
        self.sales_data = sales_data.copy()
        self._preprocess_data()
        
    def _preprocess_data(self):
        """
        Preprocess the data for customer analysis.
        """
        # Convert date columns
        date_columns = [col for col in self.sales_data.columns if 'date' in col.lower()]
        for col in date_columns:
            try:
                self.sales_data[col] = pd.to_datetime(self.sales_data[col])
            except:
                pass
    
    def analyze_purchase_frequency(self) -> pd.DataFrame:
        """
        Analyze customer purchase frequency patterns.
        
        Returns:
            pd.DataFrame: Purchase frequency analysis
        """
        if 'customer_id' not in self.sales_data.columns:
            logger.warning("Customer ID column not found")
            return pd.DataFrame()
            
        customer_frequency = self.sales_data.groupby('customer_id').agg({
            'order_date': ['count', 'min', 'max'],
            'total_amount': 'sum'
        }).fillna(0)
        
        customer_frequency.columns = ['purchase_count', 'first_purchase', 'last_purchase', 'total_spent']
        
        # Calculate time between purchases
        customer_frequency['purchase_span_days'] = (
            customer_frequency['last_purchase'] - customer_frequency['first_purchase']
        ).dt.days
        
        customer_frequency['avg_days_between_purchases'] = (
            customer_frequency['purchase_span_days'] / 
            (customer_frequency['purchase_count'] - 1)
        ).fillna(0)
        
        return customer_frequency
    
    def analyze_customer_lifetime_value(self) -> pd.DataFrame:
        """
        Calculate customer lifetime value (CLV).
        
        Returns:
            pd.DataFrame: CLV analysis
        """
        if 'customer_id' not in self.sales_data.columns:
            logger.warning("Customer ID column not found")
            return pd.DataFrame()
            
        clv_data = self.sales_data.groupby('customer_id').agg({
            'total_amount': ['sum', 'mean', 'count'],
            'order_date': ['min', 'max']
        }).fillna(0)
        
        clv_data.columns = ['total_revenue', 'avg_order_value', 'order_count', 
                           'first_order', 'last_order']
        
        # Calculate customer age
        clv_data['customer_age_days'] = (
            clv_data['last_order'] - clv_data['first_order']
        ).dt.days
        
        # Calculate CLV metrics
        clv_data['clv'] = clv_data['total_revenue']
        clv_data['clv_per_day'] = clv_data['clv'] / clv_data['customer_age_days'].replace(0, 1)
        clv_data['clv_per_order'] = clv_data['clv'] / clv_data['order_count'].replace(0, 1)
        
        return clv_data.sort_values('clv', ascending=False)
    
    def analyze_customer_retention(self, period_days: int = 30) -> Dict:
        """
        Analyze customer retention patterns.
        
        Args:
            period_days (int): Period in days to analyze retention
            
        Returns:
            Dict: Customer retention analysis
        """
        if 'customer_id' not in self.sales_data.columns or 'order_date' not in self.sales_data.columns:
            logger.warning("Customer ID or order date column not found")
            return {}
            
        # Get customer first and last purchase dates
        customer_dates = self.sales_data.groupby('customer_id')['order_date'].agg(['min', 'max'])
        
        # Calculate retention metrics
        total_customers = len(customer_dates)
        repeat_customers = len(customer_dates[customer_dates['max'] > customer_dates['min']])
        
        # Calculate time-based retention
        current_date = pd.Timestamp.now()
        active_customers = len(customer_dates[
            (current_date - customer_dates['max']).dt.days <= period_days
        ])
        
        retention_analysis = {
            'total_customers': total_customers,
            'repeat_customers': repeat_customers,
            'repeat_rate': repeat_customers / total_customers if total_customers > 0 else 0,
            'active_customers': active_customers,
            'retention_rate': active_customers / total_customers if total_customers > 0 else 0,
            'avg_customer_lifespan_days': (customer_dates['max'] - customer_dates['min']).dt.days.mean()
        }
        
        return retention_analysis

def generate_business_insights(sales_data: pd.DataFrame) -> Dict:
    """
    Generate comprehensive business insights from sales data.
    
    Args:
        sales_data (pd.DataFrame): Sales transaction data
        
    Returns:
        Dict: Business insights and recommendations
    """
    insights = {}
    
    # Initialize analyzers
    sales_analyzer = SalesAnalyzer(sales_data)
    customer_analyzer = CustomerAnalyzer(sales_data)
    
    # Get basic metrics
    summary = sales_analyzer.get_sales_summary()
    kpis = sales_analyzer.calculate_kpis()
    
    insights['summary'] = summary
    insights['kpis'] = kpis
    
    # Top performing products
    top_products = sales_analyzer.analyze_product_performance(top_n=5)
    insights['top_products'] = top_products.to_dict('index')
    
    # Customer segments
    customer_segments = sales_analyzer.analyze_customer_segments()
    insights['customer_segments'] = {
        'segment_counts': customer_segments['segment'].value_counts().to_dict(),
        'segment_metrics': customer_segments.groupby('segment').agg({
            'total_spent': 'mean',
            'order_count': 'mean',
            'avg_order_value': 'mean'
        }).to_dict('index')
    }
    
    # Customer retention
    retention = customer_analyzer.analyze_customer_retention()
    insights['retention'] = retention
    
    # Generate recommendations
    insights['recommendations'] = _generate_recommendations(insights)
    
    return insights

def _generate_recommendations(insights: Dict) -> List[str]:
    """
    Generate business recommendations based on insights.
    
    Args:
        insights (Dict): Business insights
        
    Returns:
        List[str]: List of recommendations
    """
    recommendations = []
    
    # Revenue recommendations
    avg_order_value = insights.get('kpis', {}).get('avg_order_value', 0)
    if avg_order_value < 100:
        recommendations.append("Consider implementing upselling strategies to increase average order value")
    
    # Customer retention recommendations
    retention_rate = insights.get('retention', {}).get('retention_rate', 0)
    if retention_rate < 0.3:
        recommendations.append("Focus on customer retention strategies - current retention rate is low")
    
    # Product recommendations
    if 'top_products' in insights:
        recommendations.append("Analyze top-performing products to understand success factors")
    
    # General recommendations
    recommendations.extend([
        "Implement customer loyalty programs to improve retention",
        "Consider seasonal marketing campaigns based on sales trends",
        "Analyze customer segments for targeted marketing strategies"
    ])
    
    return recommendations 