import re

def clean_text(text):
    text = re.sub(r'\n+', '\n', text)         
    text = re.sub(r'\s{2,}', ' ', text)    
    text = re.sub(r'(1\s+){2,}', '', text)    
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    return text.strip()