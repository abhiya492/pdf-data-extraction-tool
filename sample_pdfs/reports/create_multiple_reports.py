from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import os
import random
from datetime import datetime, timedelta

# List of report titles
REPORT_TITLES = [
    "Quarterly Financial Performance",
    "Annual Market Analysis",
    "Customer Satisfaction Survey Results",
    "Product Development Progress",
    "Operations Efficiency Report"
]

# List of summary templates
SUMMARY_TEMPLATES = [
    "This report analyzes the {period} performance metrics with focus on {focus_area}. Overall trends show {trend} in key indicators.",
    "An overview of {period} data, highlighting {focus_area} and providing recommendations for {improvement_area}.",
    "Comprehensive analysis of {period} {focus_area}, with comparisons to previous periods and industry benchmarks.",
    "Detailed examination of {focus_area} for {period}, including challenges faced and opportunities identified.",
    "Assessment of {period} performance in {focus_area}, with strategic recommendations for future improvements."
]

# Areas to focus on
FOCUS_AREAS = [
    "revenue growth", "cost reduction", "market expansion", "customer acquisition",
    "operational efficiency", "product innovation", "customer retention", "profit margins"
]

# Improvement areas
IMPROVEMENT_AREAS = [
    "the next quarter", "strategic planning", "resource allocation",
    "process optimization", "market positioning", "competitive advantage"
]

# Performance trends
TRENDS = [
    "positive growth", "steady improvement", "mixed results", "significant progress", 
    "challenges with opportunities", "promising indicators", "areas for improvement"
]

def generate_random_date(start_date, end_date):
    """Generate a random date between start_date and end_date"""
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + timedelta(days=random_number_of_days)

def create_report_pdf(index):
    """Create a sample report PDF for testing"""
    # Set random values for this report
    title = REPORT_TITLES[index]
    
    # Generate date in the last 6 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    report_date = generate_random_date(start_date, end_date)
    report_date_str = report_date.strftime("%m/%d/%Y")
    
    # Generate a report ID
    report_id = f"REP-{report_date.year}-{random.randint(1000, 9999)}"
    
    # Generate the quarter and year for the report
    quarter = (report_date.month - 1) // 3 + 1
    year = report_date.year
    period = f"Q{quarter} {year}"
    
    # Choose random elements for summary
    focus_area = random.choice(FOCUS_AREAS)
    improvement_area = random.choice(IMPROVEMENT_AREAS)
    trend = random.choice(TRENDS)
    
    # Format the summary
    summary_template = random.choice(SUMMARY_TEMPLATES)
    summary = summary_template.format(period=period, focus_area=focus_area, 
                                     improvement_area=improvement_area, trend=trend)
    
    # Create the PDF
    output_path = f"sample_report_{index+1}.pdf"
    c = canvas.Canvas(output_path, pagesize=letter)
    
    # Add report header
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 750, title)
    
    c.setFont("Helvetica", 12)
    c.drawString(50, 730, f"Prepared by: Analysis Team {index+1}")
    c.drawString(50, 710, f"Date: {report_date_str}")
    c.drawString(50, 690, f"Report ID: {report_id}")
    
    # Add Executive Summary
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 650, "Executive Summary:")
    
    c.setFont("Helvetica", 11)
    y_pos = 630
    # Split the summary into lines
    for line in [summary[i:i+70] for i in range(0, len(summary), 70)]:
        c.drawString(60, y_pos, line.strip())
        y_pos -= 15
    
    # Generate random metrics for the report
    metrics = {}
    
    # Revenue (in thousands)
    metrics["Revenue"] = round(random.uniform(500, 10000), 1)
    
    # Net Profit (in thousands)
    profit_margin = random.uniform(0.05, 0.30)
    metrics["Net Profit"] = round(metrics["Revenue"] * profit_margin, 1)
    
    # Profit Margin (as percentage)
    metrics["Profit Margin"] = round(profit_margin * 100, 1)
    
    # Operating Expenses (in thousands)
    metrics["Operating Expenses"] = round(metrics["Revenue"] * random.uniform(0.3, 0.7), 1)
    
    # Customer Metrics
    metrics["Customer Count"] = random.randint(100, 10000)
    metrics["Customer Acquisition Cost"] = round(random.uniform(50, 500), 2)
    metrics["Customer Lifetime Value"] = round(random.uniform(500, 5000), 2)
    
    # Add Key Metrics section
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 570, "Key Metrics:")
    
    c.setFont("Helvetica", 11)
    y_pos = 550
    for metric, value in metrics.items():
        # Format the values appropriately based on metric type
        if metric in ["Revenue", "Net Profit", "Operating Expenses"]:
            # Format as currency in thousands
            formatted_value = f"${value:,.1f}K"
        elif metric in ["Profit Margin"]:
            # Format as percentage
            formatted_value = f"{value}%"
        elif metric in ["Customer Acquisition Cost", "Customer Lifetime Value"]:
            # Format as currency
            formatted_value = f"${value:.2f}"
        else:
            # Format as number
            formatted_value = f"{value:,}"
            
        c.drawString(60, y_pos, f"{metric}: {formatted_value}")
        y_pos -= 20
    
    # Generate comparison data for previous quarter
    previous_metrics = {}
    for metric, value in metrics.items():
        # Previous quarter values differ by -15% to +15%
        change_factor = random.uniform(0.85, 1.15)
        previous_metrics[metric] = value / change_factor
    
    # Add Quarterly Comparison Table
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 380, "Quarterly Comparison:")
    
    # Table header
    c.setStrokeColorRGB(0, 0, 0)
    c.line(50, 360, 550, 360)
    
    c.setFont("Helvetica-Bold", 11)
    c.drawString(60, 340, "Metric")
    previous_quarter = f"Q{quarter-1 if quarter > 1 else 4} {year if quarter > 1 else year-1}"
    c.drawString(180, 340, previous_quarter)
    c.drawString(280, 340, period)
    c.drawString(380, 340, "Change (%)")
    
    c.line(50, 330, 550, 330)
    
    # Table data
    y_pos = 310
    
    # Select 5 metrics to show in the comparison table
    comparison_metrics = random.sample(list(metrics.keys()), min(5, len(metrics)))
    
    for metric in comparison_metrics:
        current_value = metrics[metric]
        previous_value = previous_metrics[metric]
        
        # Calculate percent change
        pct_change = ((current_value - previous_value) / previous_value) * 100
        is_positive = pct_change >= 0
        
        # Format values
        if metric in ["Revenue", "Net Profit", "Operating Expenses"]:
            current_str = f"${current_value:,.1f}K"
            previous_str = f"${previous_value:,.1f}K"
        elif metric in ["Profit Margin"]:
            current_str = f"{current_value}%"
            previous_str = f"{previous_value:.1f}%"
        elif metric in ["Customer Acquisition Cost", "Customer Lifetime Value"]:
            current_str = f"${current_value:.2f}"
            previous_str = f"${previous_value:.2f}"
        else:
            current_str = f"{int(current_value):,}"
            previous_str = f"{int(previous_value):,}"
            
        # Format the change percentage
        change_str = f"{'+' if is_positive else ''}{pct_change:.1f}%"
        
        c.setFont("Helvetica", 11)
        c.drawString(60, y_pos, metric)
        c.drawString(180, y_pos, previous_str)
        c.drawString(280, y_pos, current_str)
        
        # Set color based on positive/negative change
        if is_positive:
            c.setFillColorRGB(0, 0.5, 0)  # Green for positive
        else:
            c.setFillColorRGB(0.8, 0, 0)  # Red for negative
        c.drawString(380, y_pos, change_str)
        c.setFillColorRGB(0, 0, 0)  # Reset to black
        
        y_pos -= 20
    
    # Add Future Outlook section
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 200, "Future Outlook:")
    
    # Generate a random outlook
    outlook_templates = [
        "Based on current trends, we project {trend} in {next_period}. The company is {position} to meet annual targets. Strategic initiatives in {initiative_area} are expected to drive additional growth in the {timeline}.",
        "Our analysis indicates {trend} moving into {next_period}. Key opportunities exist in {initiative_area}, which should be prioritized in the {timeline}.",
        "Looking ahead to {next_period}, we anticipate {trend}. Success will depend on effectively executing our strategy in {initiative_area} over the {timeline}."
    ]
    
    trend_options = ["continued growth", "stabilization", "marginal improvement", "significant progress"]
    next_period_options = [f"Q{(quarter % 4) + 1}", "the next two quarters", "the remainder of the year"]
    position_options = ["well-positioned", "on track", "taking steps", "implementing strategies"]
    initiative_area_options = ["product development", "market expansion", "operational efficiency", "customer retention", "digital transformation"]
    timeline_options = ["coming months", "second half of the year", "next two quarters", "near term"]
    
    outlook_text = random.choice(outlook_templates).format(
        trend=random.choice(trend_options),
        next_period=random.choice(next_period_options),
        position=random.choice(position_options),
        initiative_area=random.choice(initiative_area_options),
        timeline=random.choice(timeline_options)
    )
    
    c.setFont("Helvetica", 11)
    y_pos = 180
    # Split the outlook into lines
    for line in [outlook_text[i:i+70] for i in range(0, len(outlook_text), 70)]:
        c.drawString(60, y_pos, line.strip())
        y_pos -= 15
    
    # Add footer
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(50, 50, "Confidential - For internal use only")
    c.drawString(400, 50, "Page 1 of 1")
    
    # Save the PDF
    c.save()
    print(f"Created sample report: {output_path}")
    return output_path

if __name__ == "__main__":
    print("Generating 5 sample report PDFs...")
    for i in range(5):
        create_report_pdf(i)
    print("Done!") 