import json
import os
import logging
import time  # Added for retry delay

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

REVIEW_QUEUE = config['review_queue']
PROCESSED_DIR = config['processed_dir']

os.makedirs(PROCESSED_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=config['log_file'],
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def auto_process_claim(claim_info):
    if not claim_info.get('claim_number'):
        logging.error("Cannot auto-process: Missing claim number")
        return
    try:
        file_path = os.path.join(PROCESSED_DIR, f"{claim_info['claim_number']}.json")
        with open(file_path, 'w') as f:
            json.dump(claim_info, f, indent=4)
        logging.info(f"Auto-processed: {claim_info['claim_number']}")
    except Exception as e:
        logging.error(f"Error auto-processing {claim_info.get('claim_number', 'unknown')}: {e}")

def queue_for_review(claim_info, priority):
    if not claim_info.get('claim_number'):
        logging.error("Cannot queue for review: Missing claim number")
        return

    queue = []
    try:
        if os.path.exists(REVIEW_QUEUE):
            with open(REVIEW_QUEUE, 'r') as f:
                queue = json.load(f)
    except json.JSONDecodeError as e:
        logging.error(f"Error reading review queue: {e}")
        return
    except Exception as e:
        logging.error(f"Unexpected error reading review queue: {e}")
        return

    queue.append({
        "claim_number": claim_info['claim_number'],
        "priority": priority,
        "fields": claim_info
    })
    queue.sort(key=lambda x: x['priority'], reverse=True)

    for attempt in range(3):
        try:
            with open(REVIEW_QUEUE, 'w') as f:
                json.dump(queue, f, indent=4)
            logging.info(f"Queued for review: {claim_info['claim_number']} (Priority: {priority})")
            break
        except Exception as e:
            logging.error(f"Attempt {attempt + 1} failed to write to review queue: {e}")
            if attempt == 2:
                logging.warning(f"Failed to queue {claim_info['claim_number']} after 3 attempts")
            time.sleep(1)
