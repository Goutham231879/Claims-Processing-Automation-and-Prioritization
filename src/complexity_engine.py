from src.info_ex import check_missing_fields
import json



with open('config.json', 'r') as f:
    config = json.load(f)


def is_complex(claim_info, amount_threshold=None):
    if amount_threshold is None:
        amount_threshold = config['amount_threshold']
    if claim_info.get('error'):
        return False
    try:
        if claim_info['claim_amount'] and int(claim_info['claim_amount'].replace(',', '')) > amount_threshold:
            return True
    except (ValueError, TypeError):
        return True  
    if claim_info['claim_type'] in ['Medical', 'Theft']:
        return True
    if check_missing_fields(claim_info):
        return True
    return False


def assign_priority(claim_info, amount_threshold=None):
    if amount_threshold is None:
        amount_threshold = config['amount_threshold']
    score = 1
    if claim_info.get('error'):
        return 0
    if claim_info['claim_type'] in ['Medical', 'Theft']:
        score += 3
    try:
        if claim_info['claim_amount'] and int(claim_info['claim_amount'].replace(',', '')) > amount_threshold:
            score += 3
    except (ValueError, TypeError):
        score += 3 
    if check_missing_fields(claim_info):
        score += 3
    return min(score, 10)