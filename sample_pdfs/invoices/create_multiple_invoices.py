from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
import random
from datetime import datetime, timedelta

# List of company names to use for invoices
COMPANIES = [
    "TechSolutions Inc.",
    "Global Logistics Ltd.",
    "CreativeDesign Studios",
    "Professional Services Group",
    "EcoFriendly Manufacturing"
]

# List of services for line items
SERVICES = [
    "Consulting Services",
    "Software Development",
    "Design Work",
    "Project Management",
    "Technical Support",
    "Web Hosting",
    "Cloud Storage",
    "Training Services",
    "Maintenance",
    "Marketing Services"
]

def generate_invoice_number():
    """Generate a random invoice number"""
    year = datetime.now().year
    return f"INV-{year}-{random.randint(1000, 9999)}"

def generate_random_date(start_date, end_date):
    """Generate a random date between start_date and end_date"""
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + timedelta(days=random_number_of_days)

def create_invoice_pdf(company_index):
    """Create a sample invoice PDF for testing"""
    # Set random values for this invoice
    company = COMPANIES[company_index]
    invoice_number = generate_invoice_number()
    
    # Generate date in the last 3 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    invoice_date = generate_random_date(start_date, end_date)
    due_date = invoice_date + timedelta(days=30)
    
    # Format dates
    invoice_date_str = invoice_date.strftime("%m/%d/%Y")
    due_date_str = due_date.strftime("%m/%d/%Y")
    
    # Create PDF
    output_path = f"sample_invoice_{company_index+1}.pdf"
    c = canvas.Canvas(output_path, pagesize=letter)
    
    # Add company header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, company)
    c.setFont("Helvetica", 12)
    c.drawString(50, 735, f"{123 + company_index} Business Avenue")
    c.drawString(50, 720, f"Cityville, State {10000 + company_index * 1000}")
    c.drawString(50, 705, f"Phone: (555) {100 + company_index}-{4000 + company_index}")
    
    # Add invoice header
    c.setFont("Helvetica-Bold", 14)
    c.drawString(400, 750, "INVOICE")
    c.setFont("Helvetica", 11)
    c.drawString(400, 735, f"Invoice #: {invoice_number}")
    c.drawString(400, 720, f"Date: {invoice_date_str}")
    c.drawString(400, 705, f"Due Date: {due_date_str}")
    
    # Add customer info
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 650, "Bill To:")
    c.setFont("Helvetica", 11)
    c.drawString(50, 635, f"Customer {company_index + 1} Ltd.")
    c.drawString(50, 620, f"Attn: Customer Contact {company_index + 1}")
    c.drawString(50, 605, f"{400 + company_index * 10} Client Street")
    c.drawString(50, 590, f"Customertown, State {54000 + company_index * 100}")
    
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
    total = 0
    
    # Generate between 2 and 4 line items
    num_items = random.randint(2, 4)
    for i in range(num_items):
        service = random.choice(SERVICES)
        quantity = random.randint(1, 20)
        unit_price = random.randint(50, 300)
        amount = quantity * unit_price
        total += amount
        
        c.setFont("Helvetica", 11)
        c.drawString(50, y_position, service)
        c.drawString(300, y_position, str(quantity))
        c.drawString(370, y_position, f"${unit_price:.2f}")
        c.drawString(450, y_position, f"${amount:.2f}")
        
        y_position -= 20
    
    # Add totals
    c.line(50, y_position - 10, 550, y_position - 10)
    
    # Calculate tax and total
    tax_rate = random.uniform(0.05, 0.09)  # 5-9% tax rate
    tax = total * tax_rate
    grand_total = total + tax
    
    y_position -= 30
    c.drawString(350, y_position, "Subtotal:")
    c.drawString(450, y_position, f"${total:.2f}")
    
    y_position -= 20
    c.drawString(350, y_position, f"Tax ({tax_rate:.1%}):")
    c.drawString(450, y_position, f"${tax:.2f}")
    
    y_position -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(350, y_position, "Total:")
    c.drawString(450, y_position, f"${grand_total:.2f}")
    
    # Add payment information
    y_position -= 40
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y_position, "Payment Information:")
    c.setFont("Helvetica", 11)
    y_position -= 20
    c.drawString(50, y_position, f"Bank: {company} Financial")
    y_position -= 20
    c.drawString(50, y_position, f"Account: {random.randint(10000000, 99999999)}")
    y_position -= 20
    c.drawString(50, y_position, f"Routing: {random.randint(100000000, 999999999)}")
    
    # Add notes
    y_position -= 40
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y_position, "Notes:")
    c.setFont("Helvetica", 11)
    y_position -= 20
    c.drawString(50, y_position, "Please make payment within 30 days.")
    y_position -= 20
    c.drawString(50, y_position, "Thank you for your business!")
    
    # Save the PDF
    c.save()
    print(f"Created sample invoice: {output_path}")
    return output_path

if __name__ == "__main__":
    print("Generating 5 sample invoice PDFs...")
    for i in range(5):
        create_invoice_pdf(i)
    print("Done!") 