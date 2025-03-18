# PDF Data Extraction and Analysis Tool

A Python tool for extracting structured data from PDF files (like invoices or reports), processing this information, and generating actionable insights.

## Features

- **Document Processing**: Extracts key information from PDF documents using pattern recognition
- **Data Organization**: Transforms raw data into structured formats (CSV, Excel, JSON)
- **Automated Analysis**: Performs calculations to identify trends, totals, and anomalies
- **Visualization**: Generates charts and summary reports to highlight key findings

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd pdf_analyzer
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

The tool has two main modes: invoice processing and report processing.

### Processing Invoices

```bash
python src/main.py --type invoice --input /path/to/invoice/pdfs --output /path/to/output
```

### Processing Reports

```bash
python src/main.py --type report --input /path/to/report/pdfs --output /path/to/output
```

## Output

The tool generates several output files:

- **CSV and Excel files**: Containing structured data extracted from PDFs
- **JSON files**: Raw extracted data and analysis insights
- **Charts**: Visual representations of the data and anomalies

## Project Structure

```
pdf_analyzer/
├── src/
│   ├── pdf_extractor.py  - PDF data extraction classes
│   ├── data_processor.py - Data processing and analysis
│   ├── visualizer.py     - Data visualization
│   └── main.py           - Main application entry point
├── tests/
│   └── test_extractor.py - Tests for PDF extractor
├── sample_pdfs/          - Sample PDF files for testing
└── requirements.txt      - Required Python packages
```

## How It Works

1. **PDF Extraction**: The tool uses pattern matching and regular expressions to extract key information from PDFs.
2. **Data Processing**: Extracted data is cleaned and organized into structured formats.
3. **Analysis**: The tool calculates statistics, identifies trends, and detects anomalies.
4. **Visualization**: Results are presented in charts to make the insights easily digestible.

## Customization

The extraction patterns can be customized by modifying the regular expressions in the `InvoiceExtractor` and `ReportExtractor` classes to fit your specific PDF formats.

## Testing

Run the tests with:

```bash
python -m unittest discover tests
```

## License

MIT 