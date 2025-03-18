import os
import sys
import argparse
from typing import Dict, List, Any, Optional, Tuple
import json
import glob
from datetime import datetime

from pdf_extractor import PDFExtractor, InvoiceExtractor, ReportExtractor
from data_processor import DataProcessor, DataAnalyzer
from visualizer import DataVisualizer


def process_invoices(input_dir: str, output_dir: str) -> Dict[str, Any]:
    """Process all invoice PDFs in the input directory"""
    # Find all PDF files in the input directory
    pdf_files = glob.glob(os.path.join(input_dir, "*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in {input_dir}")
        return {}
        
    # Process each PDF
    processor = DataProcessor()
    for pdf_file in pdf_files:
        print(f"Processing invoice: {os.path.basename(pdf_file)}")
        try:
            # Extract data from the PDF
            extractor = InvoiceExtractor(pdf_file)
            invoice_data = extractor.extract_invoice_data()
            
            # Add filename to the data
            invoice_data['filename'] = os.path.basename(pdf_file)
            
            # Add the data to the processor
            processor.add_data(invoice_data)
        except Exception as e:
            print(f"Error processing {pdf_file}: {str(e)}")
            continue
    
    # Process the combined data
    df = processor.process_invoice_data()
    if df.empty:
        print("No valid data extracted from PDFs")
        return {}
        
    # Make sure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the processed data
    output_csv = os.path.join(output_dir, "processed_invoices.csv")
    output_excel = os.path.join(output_dir, "processed_invoices.xlsx")
    output_json = os.path.join(output_dir, "raw_invoice_data.json")
    
    processor.save_to_csv(output_csv)
    processor.save_to_excel(output_excel)
    processor.export_as_json(output_json)
    
    print(f"Processed data saved to {output_csv} and {output_excel}")
    print(f"Raw extracted data saved to {output_json}")
    
    # Analyze the data
    analyzer = DataAnalyzer(df)
    insights = analyzer.analyze_invoices()
    
    # Add anomalies to insights
    anomalies = analyzer.get_anomalies()
    insights['anomalies'] = anomalies
    
    # Save insights
    insights_path = os.path.join(output_dir, "invoice_insights.json")
    analyzer.save_insights(insights_path)
    print(f"Analysis insights saved to {insights_path}")
    
    # Create visualizations
    visualizer = DataVisualizer(df, insights)
    chart_output_dir = os.path.join(output_dir, "charts")
    saved_charts = visualizer.save_visualizations(chart_output_dir, "invoice")
    
    print(f"Visualizations saved to: {chart_output_dir}")
    
    return {
        'data': df,
        'insights': insights,
        'charts': saved_charts,
        'output_files': {
            'csv': output_csv,
            'excel': output_excel,
            'json': output_json,
            'insights': insights_path
        }
    }


def process_reports(input_dir: str, output_dir: str) -> Dict[str, Any]:
    """Process all report PDFs in the input directory"""
    # Find all PDF files in the input directory
    pdf_files = glob.glob(os.path.join(input_dir, "*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in {input_dir}")
        return {}
        
    # Process each PDF
    processor = DataProcessor()
    for pdf_file in pdf_files:
        print(f"Processing report: {os.path.basename(pdf_file)}")
        try:
            # Extract data from the PDF
            extractor = ReportExtractor(pdf_file)
            report_data = extractor.extract_report_data()
            
            # Add filename to the data
            report_data['filename'] = os.path.basename(pdf_file)
            
            # Add the data to the processor
            processor.add_data(report_data)
        except Exception as e:
            print(f"Error processing {pdf_file}: {str(e)}")
            continue
    
    # Process the combined data
    df = processor.process_report_data()
    if df.empty:
        print("No valid data extracted from PDFs")
        return {}
        
    # Make sure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the processed data
    output_csv = os.path.join(output_dir, "processed_reports.csv")
    output_excel = os.path.join(output_dir, "processed_reports.xlsx")
    output_json = os.path.join(output_dir, "raw_report_data.json")
    
    processor.save_to_csv(output_csv)
    processor.save_to_excel(output_excel)
    processor.export_as_json(output_json)
    
    print(f"Processed data saved to {output_csv} and {output_excel}")
    print(f"Raw extracted data saved to {output_json}")
    
    # Analyze the data
    analyzer = DataAnalyzer(df)
    insights = analyzer.analyze_reports()
    
    # Add anomalies to insights
    anomalies = analyzer.get_anomalies()
    insights['anomalies'] = anomalies
    
    # Save insights
    insights_path = os.path.join(output_dir, "report_insights.json")
    analyzer.save_insights(insights_path)
    print(f"Analysis insights saved to {insights_path}")
    
    # Create visualizations
    visualizer = DataVisualizer(df, insights)
    chart_output_dir = os.path.join(output_dir, "charts")
    saved_charts = visualizer.save_visualizations(chart_output_dir, "report")
    
    print(f"Visualizations saved to: {chart_output_dir}")
    
    return {
        'data': df,
        'insights': insights,
        'charts': saved_charts,
        'output_files': {
            'csv': output_csv,
            'excel': output_excel,
            'json': output_json,
            'insights': insights_path
        }
    }


def main():
    """Main function to parse arguments and run the appropriate processor"""
    parser = argparse.ArgumentParser(description='Extract and analyze data from PDF files')
    parser.add_argument('--type', choices=['invoice', 'report'], required=True,
                      help='Type of PDFs to process (invoice or report)')
    parser.add_argument('--input', required=True, help='Input directory containing PDFs')
    parser.add_argument('--output', default='./output', help='Output directory for results')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Input directory not found: {args.input}")
        return 1
        
    if args.type == 'invoice':
        process_invoices(args.input, args.output)
    else:
        process_reports(args.input, args.output)
        
    return 0


if __name__ == "__main__":
    sys.exit(main()) 