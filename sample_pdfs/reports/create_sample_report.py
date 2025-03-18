from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def create_sample_report():
    """Create a simple report PDF for testing the PDF analyzer"""
    output_path = "sample_report.pdf"
    c = canvas.Canvas(output_path, pagesize=letter)
    
    # Add report header
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 750, "Financial Performance Report")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, 730, "Prepared by: Financial Analysis Team")
    c.drawString(50, 710, "Date: 03/18/2023")
    c.drawString(50, 690, "Report ID: REP-2023-Q1")
    
    # Add Executive Summary
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 650, "Executive Summary:")
    
    c.setFont("Helvetica", 11)
    summary_text = """
    This report provides an analysis of the company's financial performance for Q1 2023.
    Overall performance shows strong revenue growth with increased profitability compared
    to the previous quarter. Key metrics indicate positive trends in all business segments.
    """
    y_pos = 630
    for line in summary_text.strip().split('\n'):
        c.drawString(60, y_pos, line.strip())
        y_pos -= 15
    
    # Add Key Metrics section
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 570, "Key Metrics:")
    
    c.setFont("Helvetica", 11)
    metrics = [
        ("Revenue", "$4,250,000"),
        ("Net Profit", "$825,000"),
        ("Profit Margin", "19.4%"),
        ("Operating Expenses", "$1,125,000"),
        ("Customer Acquisition Cost", "$125"),
        ("Customer Lifetime Value", "$1,250")
    ]
    
    y_pos = 550
    for metric, value in metrics:
        c.drawString(60, y_pos, f"{metric}: {value}")
        y_pos -= 20
    
    # Add Quarterly Comparison Table
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 380, "Quarterly Comparison:")
    
    # Table header
    c.setStrokeColorRGB(0, 0, 0)
    c.line(50, 360, 550, 360)
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(60, 340, "Metric")
    c.drawString(200, 340, "Q4 2022")
    c.drawString(300, 340, "Q1 2023")
    c.drawString(400, 340, "Change (%)")
    
    c.line(50, 330, 550, 330)
    
    # Table data
    comparison_data = [
        ("Revenue", "$3,950,000", "$4,250,000", "+7.6%"),
        ("Net Profit", "$750,000", "$825,000", "+10.0%"),
        ("Profit Margin", "19.0%", "19.4%", "+2.1%"),
        ("Operating Expenses", "$1,200,000", "$1,125,000", "-6.2%"),
        ("Customer Count", "15,200", "16,800", "+10.5%")
    ]
    
    y_pos = 310
    for data in comparison_data:
        c.setFont("Helvetica", 11)
        c.drawString(60, y_pos, data[0])
        c.drawString(200, y_pos, data[1])
        c.drawString(300, y_pos, data[2])
        
        # Change percent (colored based on positive/negative)
        if data[3].startswith("+"):
            c.setFillColorRGB(0, 0.5, 0)  # Green for positive
        else:
            c.setFillColorRGB(0.8, 0, 0)  # Red for negative
        c.drawString(400, y_pos, data[3])
        c.setFillColorRGB(0, 0, 0)  # Reset to black
        
        y_pos -= 20
    
    # Add Future Outlook section
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 200, "Future Outlook:")
    
    c.setFont("Helvetica", 11)
    outlook_text = """
    Based on current trends, we project continued growth in Q2 2023. The company is on
    track to meet or exceed annual targets. Strategic initiatives in product development
    and market expansion are expected to drive additional growth in the second half of
    the year. We recommend maintaining the current investment strategy while exploring
    opportunities in emerging markets.
    """
    y_pos = 180
    for line in outlook_text.strip().split('\n'):
        c.drawString(60, y_pos, line.strip())
        y_pos -= 15
    
    # Add footer
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(50, 50, "Confidential - For internal use only")
    c.drawString(400, 50, "Page 1 of 1")
    
    # Save the PDF
    c.save()
    print(f"Sample report created: {os.path.abspath(output_path)}")
    return output_path

if __name__ == "__main__":
    create_sample_report() 