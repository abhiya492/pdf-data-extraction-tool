import matplotlib.pyplot as plt
import pandas as pd
import os
from typing import Dict, List, Any, Optional, Tuple, Union
import json
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import numpy as np


class DataVisualizer:
    """Visualize processed data and insights"""
    
    def __init__(self, data: pd.DataFrame, insights: Dict[str, Any] = None):
        """Initialize with processed DataFrame and optional insights dictionary"""
        self.data = data
        self.insights = insights or {}
        
    def create_invoice_summary_chart(self) -> Tuple[Figure, Axes]:
        """Create a summary chart for invoice data"""
        if self.data.empty:
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, "No data available", ha='center', va='center')
            return fig, ax
            
        # Create a figure with subplots
        fig, axs = plt.subplots(2, 2, figsize=(12, 10))
        
        # Plot 1: Monthly totals if available
        if 'date' in self.data.columns and pd.api.types.is_datetime64_any_dtype(self.data['date']):
            if not self.data.groupby(self.data['date'].dt.to_period('M'))['total_amount'].sum().empty:
                monthly_data = self.data.groupby(self.data['date'].dt.to_period('M'))['total_amount'].sum()
                monthly_data.index = monthly_data.index.astype(str)
                axs[0, 0].bar(monthly_data.index, monthly_data.values)
                axs[0, 0].set_title('Monthly Invoice Totals')
                axs[0, 0].set_xlabel('Month')
                axs[0, 0].set_ylabel('Total Amount')
                plt.setp(axs[0, 0].xaxis.get_majorticklabels(), rotation=45)
        else:
            axs[0, 0].text(0.5, 0.5, "No date data available", ha='center', va='center')
            
        # Plot 2: Top vendors by count
        if 'vendor' in self.data.columns:
            vendor_counts = self.data['vendor'].value_counts().head(5)
            axs[0, 1].bar(vendor_counts.index, vendor_counts.values)
            axs[0, 1].set_title('Top Vendors by Invoice Count')
            axs[0, 1].set_xlabel('Vendor')
            axs[0, 1].set_ylabel('Count')
            plt.setp(axs[0, 1].xaxis.get_majorticklabels(), rotation=45)
        else:
            axs[0, 1].text(0.5, 0.5, "No vendor data available", ha='center', va='center')
            
        # Plot 3: Top vendors by total amount
        if 'vendor' in self.data.columns and 'total_amount' in self.data.columns:
            vendor_amounts = self.data.groupby('vendor')['total_amount'].sum().nlargest(5)
            axs[1, 0].bar(vendor_amounts.index, vendor_amounts.values)
            axs[1, 0].set_title('Top Vendors by Spend')
            axs[1, 0].set_xlabel('Vendor')
            axs[1, 0].set_ylabel('Total Amount')
            plt.setp(axs[1, 0].xaxis.get_majorticklabels(), rotation=45)
        else:
            axs[1, 0].text(0.5, 0.5, "No vendor amount data available", ha='center', va='center')
            
        # Plot a histogram of invoice amounts
        if 'total_amount' in self.data.columns:
            axs[1, 1].hist(self.data['total_amount'].dropna(), bins=10)
            axs[1, 1].set_title('Invoice Amount Distribution')
            axs[1, 1].set_xlabel('Amount')
            axs[1, 1].set_ylabel('Frequency')
        else:
            axs[1, 1].text(0.5, 0.5, "No amount data available", ha='center', va='center')
            
        plt.tight_layout()
        return fig, axs
        
    def create_report_summary_chart(self) -> Tuple[Figure, Axes]:
        """Create a summary chart for report data"""
        if self.data.empty:
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, "No data available", ha='center', va='center')
            return fig, ax
            
        # Get metric columns (those starting with 'metric_')
        metric_columns = [col for col in self.data.columns if col.startswith('metric_')]
        numeric_metrics = [col for col in metric_columns 
                          if pd.api.types.is_numeric_dtype(self.data[col])]
        
        if not numeric_metrics:
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, "No numeric metrics available", ha='center', va='center')
            return fig, ax
            
        # Create a figure with subplots based on number of metrics (up to 4)
        num_metrics = min(len(numeric_metrics), 4)
        fig, axs = plt.subplots(2, 2, figsize=(12, 10))
        axs = axs.flatten()
        
        # Plot time series for each metric if date is available
        if 'date' in self.data.columns and pd.api.types.is_datetime64_any_dtype(self.data['date']):
            for i, column in enumerate(numeric_metrics[:4]):  # Limit to first 4 metrics
                metric_name = column[7:]  # Remove 'metric_' prefix
                
                # Group by month and calculate mean
                monthly_data = self.data.groupby(self.data['date'].dt.to_period('M'))[column].mean()
                monthly_data.index = monthly_data.index.astype(str)
                
                axs[i].plot(monthly_data.index, monthly_data.values, marker='o')
                axs[i].set_title(f'{metric_name.replace("_", " ").title()} Over Time')
                axs[i].set_xlabel('Month')
                axs[i].set_ylabel(metric_name.replace('_', ' ').title())
                plt.setp(axs[i].xaxis.get_majorticklabels(), rotation=45)
                
                # Add trend line
                if len(monthly_data) > 1:
                    z = np.polyfit(range(len(monthly_data)), monthly_data.values, 1)
                    p = np.poly1d(z)
                    axs[i].plot(monthly_data.index, p(range(len(monthly_data))), "r--", alpha=0.8)
        else:
            # If no date, just show box plots of the metrics
            for i, column in enumerate(numeric_metrics[:4]):
                metric_name = column[7:]  # Remove 'metric_' prefix
                axs[i].boxplot(self.data[column].dropna())
                axs[i].set_title(f'{metric_name.replace("_", " ").title()} Distribution')
                axs[i].set_ylabel(metric_name.replace('_', ' ').title())
                
        # Hide unused subplots
        for i in range(num_metrics, 4):
            axs[i].axis('off')
            
        plt.tight_layout()
        return fig, axs
        
    def create_anomaly_chart(self, anomalies: List[Dict[str, Any]]) -> Tuple[Figure, Axes]:
        """Create a chart highlighting anomalies in the data"""
        if self.data.empty or not anomalies:
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, "No anomalies detected", ha='center', va='center')
            return fig, ax
            
        # Group anomalies by column
        anomaly_columns = {}
        for anomaly in anomalies:
            column = anomaly['column']
            if column not in anomaly_columns:
                anomaly_columns[column] = []
            anomaly_columns[column].append(anomaly)
            
        # Create a figure with subplots based on number of columns
        num_columns = len(anomaly_columns)
        fig, axs = plt.subplots(num_columns, 1, figsize=(10, 4 * num_columns))
        
        # Handle the case of a single subplot
        if num_columns == 1:
            axs = [axs]
            
        for i, (column, column_anomalies) in enumerate(anomaly_columns.items()):
            # Plot the full data
            axs[i].plot(range(len(self.data)), self.data[column], 'b-', label='Data')
            
            # Highlight anomalies
            anomaly_indices = [self.data.index.get_loc(a['index']) if a['index'] in self.data.index 
                             else int(a['index']) for a in column_anomalies]
            anomaly_values = [a['value'] for a in column_anomalies]
            
            axs[i].scatter(anomaly_indices, anomaly_values, color='red', 
                          s=100, label='Anomalies')
            
            # Add mean line
            mean = self.data[column].mean()
            axs[i].axhline(y=mean, color='g', linestyle='-', alpha=0.3, label='Mean')
            
            # Add standard deviation bands
            std = self.data[column].std()
            axs[i].axhline(y=mean + 2*std, color='y', linestyle='--', alpha=0.3, label='+2σ')
            axs[i].axhline(y=mean - 2*std, color='y', linestyle='--', alpha=0.3)
            
            axs[i].set_title(f'Anomalies in {column}')
            axs[i].set_xlabel('Data Point')
            axs[i].set_ylabel(column)
            axs[i].legend()
            
        plt.tight_layout()
        return fig, axs
        
    def save_visualizations(self, output_dir: str, prefix: str = "chart") -> List[str]:
        """Save all visualizations to files and return the list of file paths"""
        os.makedirs(output_dir, exist_ok=True)
        saved_files = []
        
        # Determine which chart to create based on available data columns
        if 'vendor' in self.data.columns or 'total_amount' in self.data.columns:
            # Invoice data
            fig, _ = self.create_invoice_summary_chart()
            output_path = os.path.join(output_dir, f"{prefix}_invoice_summary.png")
            fig.savefig(output_path)
            plt.close(fig)
            saved_files.append(output_path)
            
        # Check for metric columns
        metric_columns = [col for col in self.data.columns if col.startswith('metric_')]
        if metric_columns:
            # Report data
            fig, _ = self.create_report_summary_chart()
            output_path = os.path.join(output_dir, f"{prefix}_report_summary.png")
            fig.savefig(output_path)
            plt.close(fig)
            saved_files.append(output_path)
            
        # Create anomaly chart if insights contain anomalies
        if 'anomalies' in self.insights and self.insights['anomalies']:
            fig, _ = self.create_anomaly_chart(self.insights['anomalies'])
            output_path = os.path.join(output_dir, f"{prefix}_anomalies.png")
            fig.savefig(output_path)
            plt.close(fig)
            saved_files.append(output_path)
            
        return saved_files 