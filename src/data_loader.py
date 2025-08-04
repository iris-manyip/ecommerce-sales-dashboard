"""
Data Loading Utilities for E-commerce Sales Dataset

This module provides functions to load, validate, and preprocess
the e-commerce sales dataset.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import os
from typing import Dict, List, Optional, Tuple
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EcommerceDataLoader:
    """
    A class to handle loading and preprocessing of e-commerce sales data.
    """
    
    def __init__(self, data_path: str = "data/raw"):
        """
        Initialize the data loader.
        
        Args:
            data_path (str): Path to the raw data directory
        """
        self.data_path = Path(data_path)
        self.data_files = {}
        self.processed_data = {}
        
    def discover_data_files(self) -> Dict[str, str]:
        """
        Discover available data files in the raw data directory.
        
        Returns:
            Dict[str, str]: Dictionary mapping file types to file paths
        """
        if not self.data_path.exists():
            logger.warning(f"Data path {self.data_path} does not exist")
            return {}
            
        data_files = {}
        for file in self.data_path.glob("*.csv"):
            # Try to identify file type based on filename
            filename = file.stem.lower()
            if "sales" in filename or "transaction" in filename:
                data_files["sales"] = str(file)
            elif "customer" in filename or "user" in filename:
                data_files["customers"] = str(file)
            elif "product" in filename or "item" in filename:
                data_files["products"] = str(file)
            else:
                data_files[filename] = str(file)
                
        self.data_files = data_files
        logger.info(f"Discovered {len(data_files)} data files: {list(data_files.keys())}")
        return data_files
    
    def load_sales_data(self, file_path: Optional[str] = None) -> pd.DataFrame:
        """
        Load sales/transaction data.
        
        Args:
            file_path (str, optional): Path to sales data file
            
        Returns:
            pd.DataFrame: Sales data
        """
        if file_path is None:
            if "sales" in self.data_files:
                file_path = self.data_files["sales"]
            else:
                # Try to find any CSV file
                csv_files = list(self.data_path.glob("*.csv"))
                if csv_files:
                    file_path = str(csv_files[0])
                else:
                    raise FileNotFoundError("No sales data file found")
        
        logger.info(f"Loading sales data from {file_path}")
        df = pd.read_csv(file_path)
        
        # Basic data validation
        logger.info(f"Sales data shape: {df.shape}")
        logger.info(f"Columns: {list(df.columns)}")
        
        return df
    
    def load_all_data(self) -> Dict[str, pd.DataFrame]:
        """
        Load all available data files.
        
        Returns:
            Dict[str, pd.DataFrame]: Dictionary of loaded datasets
        """
        if not self.data_files:
            self.discover_data_files()
            
        loaded_data = {}
        
        for data_type, file_path in self.data_files.items():
            try:
                logger.info(f"Loading {data_type} data from {file_path}")
                df = pd.read_csv(file_path)
                loaded_data[data_type] = df
                logger.info(f"Loaded {data_type} data: {df.shape}")
            except Exception as e:
                logger.error(f"Error loading {data_type} data: {e}")
                
        self.processed_data = loaded_data
        return loaded_data
    
    def get_data_info(self, df: pd.DataFrame) -> Dict:
        """
        Get comprehensive information about a dataset.
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            Dict: Data information including shape, dtypes, missing values, etc.
        """
        info = {
            "shape": df.shape,
            "columns": list(df.columns),
            "dtypes": df.dtypes.to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "memory_usage": df.memory_usage(deep=True).sum(),
            "numeric_columns": df.select_dtypes(include=[np.number]).columns.tolist(),
            "categorical_columns": df.select_dtypes(include=['object']).columns.tolist(),
            "datetime_columns": df.select_dtypes(include=['datetime']).columns.tolist()
        }
        
        return info
    
    def validate_data(self, df: pd.DataFrame, expected_columns: Optional[List[str]] = None) -> bool:
        """
        Validate data quality and structure.
        
        Args:
            df (pd.DataFrame): Dataframe to validate
            expected_columns (List[str], optional): Expected column names
            
        Returns:
            bool: True if validation passes
        """
        validation_passed = True
        
        # Check for empty dataframe
        if df.empty:
            logger.error("Dataframe is empty")
            validation_passed = False
            
        # Check for expected columns
        if expected_columns:
            missing_columns = set(expected_columns) - set(df.columns)
            if missing_columns:
                logger.error(f"Missing expected columns: {missing_columns}")
                validation_passed = False
                
        # Check for excessive missing values
        missing_pct = df.isnull().sum() / len(df) * 100
        high_missing = missing_pct[missing_pct > 50]
        if not high_missing.empty:
            logger.warning(f"Columns with >50% missing values: {list(high_missing.index)}")
            
        return validation_passed
    
    def save_processed_data(self, data: Dict[str, pd.DataFrame], output_dir: str = "data/processed"):
        """
        Save processed data to the processed data directory.
        
        Args:
            data (Dict[str, pd.DataFrame]): Dictionary of processed dataframes
            output_dir (str): Output directory path
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for name, df in data.items():
            output_file = output_path / f"{name}.csv"
            df.to_csv(output_file, index=False)
            logger.info(f"Saved {name} data to {output_file}")
    
    def load_sample_data(self) -> pd.DataFrame:
        """
        Load a sample of the data for quick exploration.
        
        Returns:
            pd.DataFrame: Sample of the data
        """
        df = self.load_sales_data()
        return df.head(1000)  # Return first 1000 rows for quick exploration

def create_sample_data() -> pd.DataFrame:
    """
    Create sample e-commerce data for testing purposes.
    
    Returns:
        pd.DataFrame: Sample e-commerce sales data
    """
    np.random.seed(42)
    
    # Generate sample data
    n_records = 10000
    
    data = {
        'order_id': range(1, n_records + 1),
        'customer_id': np.random.randint(1, 1001, n_records),
        'product_id': np.random.randint(1, 101, n_records),
        'order_date': pd.date_range('2023-01-01', periods=n_records, freq='H'),
        'quantity': np.random.randint(1, 11, n_records),
        'unit_price': np.random.uniform(10, 500, n_records),
        'total_amount': np.random.uniform(50, 2000, n_records),
        'category': np.random.choice(['Electronics', 'Clothing', 'Books', 'Home', 'Sports'], n_records),
        'region': np.random.choice(['North', 'South', 'East', 'West'], n_records),
        'payment_method': np.random.choice(['Credit Card', 'Debit Card', 'PayPal', 'Cash'], n_records)
    }
    
    df = pd.DataFrame(data)
    df['total_amount'] = df['quantity'] * df['unit_price']
    
    return df 