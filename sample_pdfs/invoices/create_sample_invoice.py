from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def create_sample_invoice():
    """Create a simple invoice PDF for testing the PDF analyzer"""
    output_path = "sample_invoice.pdf"
    c = canvas.Canvas(output_path, pagesize=letter)
    
    # Add company header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "ACME Corp")
    c.setFont("Helvetica", 12)
    c.drawString(50, 735, "123 Business Ave")
    c.drawString(50, 720, "Cityville, State 12345")
    c.drawString(50, 705, "Phone: (555) 123-4567")
    
    # Add invoice header
    c.setFont("Helvetica-Bold", 14)
    c.drawString(400, 750, "INVOICE")
    c.setFont("Helvetica", 11)
    c.drawString(400, 735, "Invoice #: INV-2023-001")
    c.drawString(400, 720, "Date: 03/18/2023")
    c.drawString(400, 705, "Due Date: 04/18/2023")
    
    # Add customer info
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 650, "Bill To:")
    c.setFont("Helvetica", 11)
    c.drawString(50, 635, "Customer Company Ltd.")
    c.drawString(50, 620, "Attn: John Smith")
    c.drawString(50, 605, "456 Client Street")
    c.drawString(50, 590, "Customertown, State 54321")
    
    # Add table header
    c.setStrokeColorRGB(0, 0, 0)
    c.line(50, 550, 550, 550)
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 530, "Description")
    c.drawString(300, 530, "Quantity")
    c.drawString(370, 530, "Unit Price")
    c.drawString(450, 530, "Amount")
    
    c.line(50, 520, 550, 520)
    
    # Add line items
    y_position = 500
    
    # Item 1
    c.setFont("Helvetica", 11)
    c.drawString(50, y_position, "Professional Services")
    c.drawString(300, y_position, "10")
    c.drawString(370, y_position, "$150.00")
    c.drawString(450, y_position, "$1,500.00")
    
    y_position -= 20
    
    # Item 2
    c.drawString(50, y_position, "Software License")
    c.drawString(300, y_position, "1")
    c.drawString(370, y_position, "$2,000.00")
    c.drawString(450, y_position, "$2,000.00")
    
    y_position -= 20
    
    # Item 3
    c.drawString(50, y_position, "Support Subscription")
    c.drawString(300, y_position, "12")
    c.drawString(370, y_position, "$75.00")
    c.drawString(450, y_position, "$900.00")
    
    # Add totals
    c.line(50, 400, 550, 400)
    
    c.drawString(350, 380, "Subtotal:")
    c.drawString(450, 380, "$4,400.00")
    
    c.drawString(350, 360, "Tax (7%):")
    c.drawString(450, 360, "$308.00")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(350, 340, "Total:")
    c.drawString(450, 340, "$4,708.00")
    
    # Add payment information
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, 280, "Payment Information:")
    c.setFont("Helvetica", 11)
    c.drawString(50, 260, "Bank: First National Bank")
    c.drawString(50, 240, "Account: 1234567890")
    c.drawString(50, 220, "Routing: 987654321")
    
    # Add notes
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, 180, "Notes:")
    c.setFont("Helvetica", 11)
    c.drawString(50, 160, "Please make payment within 30 days.")
    c.drawString(50, 140, "Thank you for your business!")
    
    # Save the PDF
    c.save()
    print(f"Sample invoice created: {os.path.abspath(output_path)}")
    return output_path

if __name__ == "__main__":
    create_sample_invoice() 