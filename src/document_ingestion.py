import pytesseract
from PIL import Image
import pdfplumber
import os
import json


with open('config.json', 'r') as f:
    config = json.load(f)



def set_tesseract_path():
    if os.name == 'nt': 
        tesseract_path = config['tesseract_path']
        if os.path.exists(tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        else:
            raise RuntimeError(f"Tesseract executable not found at {tesseract_path}. Please install Tesseract or update the config.")




def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file using pdfplumber.
    Skips pages that have no text.
    """
    text = ''
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + '\n'
        return text
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from PDF: {e}")



def extract_text_from_image(image_path):
    """
    Extracts text from an image file using pytesseract OCR.
    """
    try:
        set_tesseract_path()
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from image: {e}")



def process_document(file_path):
    """
    Detects file type and processes accordingly:
    - PDF: uses pdfplumber
    - JPG/PNG: uses pytesseract
    - Others: raises error
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext in config['supported_extensions']:
        return extract_text_from_image(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")