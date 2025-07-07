from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import random
import os
from datetime import datetime, timedelta

# Lists for generating varied data
policy_holders = [
    "John Doe", "Jane Smith", "Alex Brown", "Emily Davis", "Michael Chen",
    "Sarah Wilson", "David Lee", "Laura Martinez", "James Taylor", "Emma Clark"
]
claim_types = ["Medical", "Vehicle", "Theft", "Travel", "Home"]
descriptions = [
    "Hospitalization due to emergency surgery",
    "Car accident with minor damage",
    "Theft of personal belongings",
    "Flight cancellation due to weather",
    "Water damage to home"
]
documentations = [
    "Medical bills and hospital records attached",
    "Police report and repair estimate attached",
    "Receipts and photos attached",
    "Travel itinerary and refund request attached",
    "Contractor estimate attached"
]

def random_date(start_year=2024, end_year=2025):
    """Generate a random date between start_year and end_year."""
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return (start_date + timedelta(days=random_days)).strftime("%m/%d/%Y")

def create_sample_claim_pdf(filename, claim_id):
    """Create a single PDF claim document with varied details."""
    try:
        c = canvas.Canvas(filename, pagesize=letter)
        c.setFont("Helvetica", 12)

        # Header
        c.drawString(100, 750, "Insurance Claim Form")
        c.drawString(100, 730, "")  # Spacer

        # Core fields (randomly omit some fields for testing missing data)
        claim_number = f"CLM-{random.randint(10000, 99999)}" if random.random() > 0.1 else None
        policy_holder = random.choice(policy_holders) if random.random() > 0.1 else None
        date_of_incident = random_date() if random.random() > 0.1 else None
        claim_amount = random.randint(1000, 200000) if random.random() > 0.1 else None
        claim_type = random.choice(claim_types) if random.random() > 0.1 else None
        description = random.choice(descriptions)
        documentation = random.choice(documentations)

        # Write fields to PDF (handle None values)
        y_position = 710
        if claim_number:
            c.drawString(100, y_position, f"Claim Number: {claim_number}")
            y_position -= 20
        if policy_holder:
            c.drawString(100, y_position, f"Policy Holder: {policy_holder}")
            y_position -= 20
        if date_of_incident:
            c.drawString(100, y_position, f"Date of Incident: {date_of_incident}")
            y_position -= 20
        if claim_amount:
            formatted_amount = f"${claim_amount:,}"
            c.drawString(100, y_position, f"Claim Amount: {formatted_amount}")
            y_position -= 20
        if claim_type:
            c.drawString(100, y_position, f"Claim Type: {claim_type}")
            y_position -= 20
        c.drawString(100, y_position, f"Description: {description}")
        y_position -= 20
        c.drawString(100, y_position, f"Documentation: {documentation}")
        y_position -= 20
        c.drawString(100, y_position, "1")  # Mimic the trailing '1' from sample

        c.save()
        print(f"Generated {filename}")
    except Exception as e:
        print(f"Error generating {filename}: {e}")

# Create data directory and generate 100 PDFs
try:
    os.makedirs("data", exist_ok=True)
    for i in range(100):
        filename = os.path.join("data", f"claim_{i+1}.pdf")
        create_sample_claim_pdf(filename, i + 1)
    print("Successfully generated 100 sample claim PDFs in data/ directory.")
except Exception as e:
    print(f"Error creating PDFs: {e}")