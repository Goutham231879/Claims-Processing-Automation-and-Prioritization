import os
import logging
import time
import json
from src.utils import clean_text
from src.complexity_engine import is_complex, assign_priority
from src.routing_engine import auto_process_claim, queue_for_review
from src.document_ingestion import process_document
from src.info_ex import extract_all_fields, check_missing_fields, is_claim_document

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

# Set up logging
logging.basicConfig(
    filename=config['log_file'],
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

input_dir = config['input_dir']
output_dir = config['output_dir']
supported_extensions = config['supported_extensions']

os.makedirs(output_dir, exist_ok=True)

def classify_document(text):
    if is_claim_document(text):
        return 'claim_form'
    if 'General Insurance Claims Guide' in text:
        return 'guide'
    return 'unknown'

failed_files = []
for file_name in os.listdir(input_dir):
    ext = os.path.splitext(file_name)[1].lower()
    if ext not in supported_extensions:
        logging.info(f"Skipping {file_name}: Unsupported file format")
        continue
    file_path = os.path.join(input_dir, file_name)
    logging.info(f"Processing: {file_name}")
    for attempt in range(3):
        try:
            text = process_document(file_path)
            text = clean_text(text)
            doc_type = classify_document(text)
            if doc_type != 'claim_form':
                logging.info(f"Skipping {file_name}: Not a claim document (Type: {doc_type})")
                break
            output_path = os.path.join(output_dir, file_name + ".txt")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            info = extract_all_fields(text)
            logging.info(f"Extracted Info for {file_name}: {info}")
            missing_fields = check_missing_fields(info)
            logging.info(f"Missing Fields: {missing_fields}")
            complex_flag = is_complex(info, config['amount_threshold'])
            priority = assign_priority(info, config['amount_threshold'])
            logging.info(f"Complex Claim: {complex_flag}, Priority Score: {priority}")
            if not complex_flag:
                auto_process_claim(info)
            else:
                queue_for_review(info, priority)
            logging.info(f"Successfully processed: {file_name}")
            break
        except Exception as e:
            logging.error(f"Attempt {attempt + 1} failed for {file_name}: {e}")
            if attempt == 2:
                failed_files.append(file_name)
            time.sleep(1)

if failed_files:
    logging.warning(f"Failed to process: {failed_files}")

print("Processing completed")
