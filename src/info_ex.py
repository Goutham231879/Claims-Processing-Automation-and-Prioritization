import re
from datetime import datetime

def is_claim_document(text):
    keywords = ['Claim Number', 'Policy Holder', 'Date of Incident']
    return any(keyword in text for keyword in keywords)

def extract_claim_number(text):
    match = re.search(r'Claim Number[:\- ]*\s*([A-Z]{3}-?\d{5,6})', text, re.I)
    if match:
        claim_num = match.group(1)
        
        claim_num = claim_num.replace('-', '')
        if len(claim_num) > 9:
            claim_num = claim_num[:9]  
        return f"{claim_num[:3]}-{claim_num[3:]}"
    return None


def extract_policy_holder(text):
    match = re.search(r'Policy(?: Holder)?[:\- ]*\s*([A-Z][a-z]+\s[A-Z][a-z]+)', text)
    return match.group(1) if match else None


def extract_date(text):
    match = re.search(r'Date of Incident[:\- ]*\s*([0-9]{2}/[0-9]{2}/[0-9]{4})', text)
    if match:
        try:
            datetime.strptime(match.group(1), '%m/%d/%Y') 
            return match.group(1)
        except ValueError:
            return None
    return None


def extract_amount(text):
    match = re.search(r'Claim Amount[:\- ₹$]*\s*([\d,/]+)', text)
    if match:
        amount = match.group(1)
        
        amount = amount.replace('/', ',')
        if ',' not in amount and len(amount) >= 4:
            amount = amount[:-3] + ',' + amount[-3:]
        try:
            int(amount.replace(',', ''))  
            return amount
        except ValueError:
            return None
    return None


def extract_claim_type(text):
    types = ['Medical', 'Vehicle', 'Travel', 'Home', 'Theft']
    for t in types:
        if t.lower() in text.lower():
            return t
    return 'Unknown'


def extract_all_fields(text):
    if not is_claim_document(text):
        return {'error': 'Not a claim document'}
    return {
        'claim_number': extract_claim_number(text),
        'policy_holder': extract_policy_holder(text),
        'incident_date': extract_date(text),
        'claim_amount': extract_amount(text),
        'claim_type': extract_claim_type(text),
    }


def check_missing_fields(info_dict):
    if info_dict.get('error'):
        return False
    return any(v is None for k, v in info_dict.items() if k != 'error')