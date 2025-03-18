import pdfplumber
import pandas as pd
import os
import re
from typing import Dict, List, Any, Optional, Tuple


class PDFExtractor:
    """Base class for PDF data extraction"""
    
    def __init__(self, pdf_path: str):
        """Initialize with path to PDF file"""
        self.pdf_path = pdf_path
        self._validate_file()
        
    def _validate_file(self) -> None:
        """Validate the PDF file exists and is accessible"""
        if not os.path.exists(self.pdf_path):
            raise FileNotFoundError(f"PDF file not found: {self.pdf_path}")
        if not self.pdf_path.lower().endswith('.pdf'):
            raise ValueError(f"File is not a PDF: {self.pdf_path}")
    
    def extract_text(self) -> List[str]:
        """Extract all text from the PDF as a list of pages"""
        pages = []
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    pages.append(text)
        return pages
    
    def extract_tables(self) -> List[pd.DataFrame]:
        """Extract all tables from the PDF"""
        tables = []
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                extracted_tables = page.extract_tables()
                for table in extracted_tables:
                    if table:
                        # Convert the table to a DataFrame
                        df = pd.DataFrame(table[1:], columns=table[0])
                        tables.append(df)
        return tables


class InvoiceExtractor(PDFExtractor):
    """Specialized extractor for invoice PDFs"""
    
    def extract_invoice_data(self) -> Dict[str, Any]:
        """Extract key data from invoice"""
        pages = self.extract_text()
        
        # Initialize result dictionary
        invoice_data = {
            "invoice_number": None,
            "date": None,
            "total_amount": None,
            "vendor": None,
            "line_items": []
        }
        
        if not pages:
            return invoice_data
            
        # Extract data from the first page
        text = pages[0]
        
        # Extract invoice number (format varies by vendor)
        invoice_match = re.search(r'Invoice\s*#?:?\s*([A-Z0-9\-]+)', text, re.IGNORECASE)
        if invoice_match:
            invoice_data["invoice_number"] = invoice_match.group(1).strip()
            
        # Extract date (multiple formats)
        date_match = re.search(r'Date:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})', text, re.IGNORECASE)
        if date_match:
            invoice_data["date"] = date_match.group(1)
            
        # Extract total amount
        amount_match = re.search(r'Total:?\s*\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)|\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', text, re.IGNORECASE)
        if amount_match:
            amount = amount_match.group(1) or amount_match.group(2)
            if amount:
                # Remove commas for conversion to float
                amount = amount.replace(',', '')
                invoice_data["total_amount"] = float(amount)
                
        # Extract vendor name (usually at the top)
        lines = text.split('\n')
        if lines:
            invoice_data["vendor"] = lines[0].strip()
            
        # Extract line items from tables
        tables = self.extract_tables()
        if tables:
            for table in tables:
                # Look for tables that might contain line items
                price_columns = [col for col in table.columns if any(keyword in col.lower() 
                                for keyword in ['price', 'amount', 'total', 'cost'])]
                if price_columns:
                    # Convert table to line items
                    for _, row in table.iterrows():
                        item = {col: row[col] for col in table.columns}
                        invoice_data["line_items"].append(item)
        
        return invoice_data


class ReportExtractor(PDFExtractor):
    """Specialized extractor for report PDFs"""
    
    def extract_report_data(self) -> Dict[str, Any]:
        """Extract key data from reports"""
        pages = self.extract_text()
        tables = self.extract_tables()
        
        report_data = {
            "title": None,
            "date": None,
            "summary": None,
            "key_metrics": {},
            "tables": tables
        }
        
        if not pages:
            return report_data
            
        # Extract title and date from first page
        text = pages[0]
        lines = text.split('\n')
        
        if lines:
            report_data["title"] = lines[0].strip()
            
        # Look for date
        date_match = re.search(r'Date:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})', text, re.IGNORECASE)
        if date_match:
            report_data["date"] = date_match.group(1)
            
        # Extract key metrics (numbers with labels)
        metric_matches = re.finditer(r'([A-Za-z\s]+):\s*\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', text)
        for match in metric_matches:
            key = match.group(1).strip()
            value = match.group(2).replace(',', '')
            try:
                report_data["key_metrics"][key] = float(value)
            except ValueError:
                report_data["key_metrics"][key] = value
                
        # Extract summary (usually found after title and before first heading)
        summary_match = re.search(r'(?:Summary|Abstract|Executive\s+Summary):(.*?)(?=\n\n|\n[A-Z]|\Z)', 
                                  text, re.DOTALL | re.IGNORECASE)
        if summary_match:
            report_data["summary"] = summary_match.group(1).strip()
            
        return report_data 