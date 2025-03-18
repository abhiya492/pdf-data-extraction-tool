import pandas as pd
import os
from typing import Dict, List, Any, Optional, Tuple, Union
import json
from datetime import datetime


class DataProcessor:
    """Process extracted data from PDFs"""
    
    def __init__(self, data_list: List[Dict[str, Any]] = None):
        """Initialize with list of extracted data dictionaries"""
        self.data_list = data_list or []
        self.processed_data = pd.DataFrame()
        
    def add_data(self, data: Dict[str, Any]) -> None:
        """Add a single data dictionary to the processor"""
        self.data_list.append(data)
        
    def process_invoice_data(self) -> pd.DataFrame:
        """Process a list of invoice data dictionaries into a structured DataFrame"""
        if not self.data_list:
            return pd.DataFrame()
            
        # Extract the basic invoice information
        invoice_info = []
        for data in self.data_list:
            invoice_info.append({
                'invoice_number': data.get('invoice_number'),
                'date': data.get('date'),
                'vendor': data.get('vendor'),
                'total_amount': data.get('total_amount'),
                'line_item_count': len(data.get('line_items', []))
            })
            
        # Create the DataFrame from the invoice info
        df = pd.DataFrame(invoice_info)
        
        # Convert date strings to datetime objects if they exist
        if 'date' in df.columns and not df['date'].isna().all():
            # Try multiple date formats
            for date_format in ['%m/%d/%Y', '%d/%m/%Y', '%m-%d-%Y', '%d-%m-%Y', '%m.%d.%Y', '%d.%m.%Y']:
                try:
                    df['date'] = pd.to_datetime(df['date'], format=date_format, errors='ignore')
                except:
                    continue
                    
        # Set invoice number as index if available
        if 'invoice_number' in df.columns and not df['invoice_number'].isna().all():
            df.set_index('invoice_number', inplace=True)
            
        self.processed_data = df
        return df
        
    def process_report_data(self) -> pd.DataFrame:
        """Process a list of report data dictionaries into a structured DataFrame"""
        if not self.data_list:
            return pd.DataFrame()
            
        # Extract the basic report information
        report_info = []
        for data in self.data_list:
            # Combine data dictionary with key metrics
            report_dict = {
                'title': data.get('title'),
                'date': data.get('date'),
                'summary': data.get('summary'),
                'table_count': len(data.get('tables', []))
            }
            
            # Add all key metrics to the dictionary
            metrics = data.get('key_metrics', {})
            for key, value in metrics.items():
                safe_key = key.replace(' ', '_').lower()
                report_dict[f'metric_{safe_key}'] = value
                
            report_info.append(report_dict)
            
        # Create DataFrame
        df = pd.DataFrame(report_info)
        
        # Convert date strings to datetime objects if they exist
        if 'date' in df.columns and not df['date'].isna().all():
            # Try multiple date formats
            for date_format in ['%m/%d/%Y', '%d/%m/%Y', '%m-%d-%Y', '%d-%m-%Y', '%m.%d.%Y', '%d.%m.%Y']:
                try:
                    df['date'] = pd.to_datetime(df['date'], format=date_format, errors='ignore')
                except:
                    continue
        
        self.processed_data = df
        return df
    
    def save_to_csv(self, output_path: str) -> None:
        """Save processed data to CSV file"""
        if self.processed_data.empty:
            raise ValueError("No processed data available. Call process_invoice_data or process_report_data first.")
            
        self.processed_data.to_csv(output_path)
        
    def save_to_excel(self, output_path: str) -> None:
        """Save processed data to Excel file"""
        if self.processed_data.empty:
            raise ValueError("No processed data available. Call process_invoice_data or process_report_data first.")
            
        self.processed_data.to_excel(output_path, sheet_name='Processed Data')
        
    def export_as_json(self, output_path: str) -> None:
        """Export original data list as JSON file"""
        with open(output_path, 'w') as f:
            json.dump(self.data_list, f, indent=4, default=str)


class DataAnalyzer:
    """Analyze processed data and generate insights"""
    
    def __init__(self, data: pd.DataFrame):
        """Initialize with processed DataFrame"""
        self.data = data
        self.insights = {}
        
    def analyze_invoices(self) -> Dict[str, Any]:
        """Analyze invoice data to extract insights"""
        if self.data.empty:
            return {'error': 'No data available for analysis'}
            
        insights = {}
        
        # Basic statistics
        if 'total_amount' in self.data.columns:
            insights['total_spend'] = self.data['total_amount'].sum()
            insights['average_invoice_amount'] = self.data['total_amount'].mean()
            insights['max_invoice_amount'] = self.data['total_amount'].max()
            insights['min_invoice_amount'] = self.data['total_amount'].min()
        
        # Vendor analysis
        if 'vendor' in self.data.columns:
            vendor_counts = self.data['vendor'].value_counts()
            insights['vendor_count'] = len(vendor_counts)
            insights['top_vendors'] = vendor_counts.head(3).to_dict()
            
            if 'total_amount' in self.data.columns:
                vendor_amounts = self.data.groupby('vendor')['total_amount'].sum()
                insights['top_vendors_by_spend'] = vendor_amounts.nlargest(3).to_dict()
        
        # Time series analysis
        if 'date' in self.data.columns and pd.api.types.is_datetime64_any_dtype(self.data['date']):
            # Monthly analysis
            self.data['month'] = self.data['date'].dt.to_period('M')
            monthly_totals = self.data.groupby('month')['total_amount'].sum()
            insights['monthly_totals'] = {str(k): v for k, v in monthly_totals.to_dict().items()}
            
            # Find trends - simple month-over-month change
            if len(monthly_totals) > 1:
                monthly_pct_changes = monthly_totals.pct_change() * 100
                insights['monthly_change'] = {str(k): v for k, v in monthly_pct_changes.dropna().to_dict().items()}
        
        self.insights = insights
        return insights
        
    def analyze_reports(self) -> Dict[str, Any]:
        """Analyze report data to extract insights"""
        if self.data.empty:
            return {'error': 'No data available for analysis'}
            
        insights = {}
        
        # Get metrics columns (those starting with 'metric_')
        metric_columns = [col for col in self.data.columns if col.startswith('metric_')]
        
        # Calculate statistics for each metric
        for column in metric_columns:
            # Skip if column has non-numeric data
            if not pd.api.types.is_numeric_dtype(self.data[column]):
                continue
                
            # Get clean metric name without the prefix
            metric_name = column[7:]  # Remove 'metric_' prefix
            
            # Calculate basic statistics
            insights[f'{metric_name}_avg'] = self.data[column].mean()
            insights[f'{metric_name}_min'] = self.data[column].min()
            insights[f'{metric_name}_max'] = self.data[column].max()
            
        # Time series analysis if date is available
        if 'date' in self.data.columns and pd.api.types.is_datetime64_any_dtype(self.data['date']):
            # Add period column for grouping
            self.data['month'] = self.data['date'].dt.to_period('M')
            
            # Analyze each metric over time
            for column in metric_columns:
                if not pd.api.types.is_numeric_dtype(self.data[column]):
                    continue
                    
                metric_name = column[7:]
                monthly_avgs = self.data.groupby('month')[column].mean()
                
                if len(monthly_avgs) > 1:
                    insights[f'{metric_name}_trend'] = {
                        'values': {str(k): v for k, v in monthly_avgs.to_dict().items()},
                        'change': monthly_avgs.iloc[-1] - monthly_avgs.iloc[0],
                        'pct_change': ((monthly_avgs.iloc[-1] / monthly_avgs.iloc[0]) - 1) * 100
                        if monthly_avgs.iloc[0] != 0 else 0
                    }
        
        self.insights = insights
        return insights
        
    def get_anomalies(self, threshold: float = 2.0) -> List[Dict[str, Any]]:
        """Detect anomalies in the data using z-score method"""
        if self.data.empty:
            return []
            
        anomalies = []
        
        # Check numeric columns for anomalies
        numeric_columns = self.data.select_dtypes(include=['number']).columns
        
        for column in numeric_columns:
            # Calculate z-scores
            mean = self.data[column].mean()
            std = self.data[column].std()
            
            if std == 0:  # Skip if there's no variation
                continue
                
            z_scores = (self.data[column] - mean) / std
            
            # Find anomalies where abs(z-score) > threshold
            anomaly_indices = self.data[abs(z_scores) > threshold].index
            
            for idx in anomaly_indices:
                value = self.data.loc[idx, column]
                anomalies.append({
                    'index': idx,
                    'column': column,
                    'value': value,
                    'z_score': z_scores[idx],
                    'mean': mean,
                    'std': std
                })
                
        return anomalies
        
    def save_insights(self, output_path: str) -> None:
        """Save insights to a JSON file"""
        with open(output_path, 'w') as f:
            json.dump(self.insights, f, indent=4, default=str) 