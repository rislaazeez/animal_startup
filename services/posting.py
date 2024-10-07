import logging
import requests
from tenacity import retry, stop_after_attempt, wait_fixed, before_sleep_log
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

BASE_URL = os.getenv("BASE_URL")

logger = logging.getLogger(__name__)

@retry(stop=stop_after_attempt(5), wait=wait_fixed(3), before_sleep=before_sleep_log(logger, logging.WARNING))
def post_animals(animals_batch):
    """Posts a batch of animals to the API"""
    try:
        logging.info(f"Posting batch of animals: {animals_batch}")
        response = requests.post(f"{BASE_URL}/animals/v1/home", json=animals_batch)
        response.raise_for_status()
        logging.info(f"Successfully posted batch: {response.status_code}")
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Failed to post animals batch: {e}")
        raise


def post_batches(animals):
    """Posts animals in batches of 100"""
    try:
        for i in range(0, len(animals), 100):
            batch = animals[i:i + 100]
            logging.info(f"Processing batch {i // 100 + 1}: {batch}")
            post_animals(batch)
        logging.info("Finished posting all batches")
    except Exception as e:
        logging.exception(f"Error posting batches of animals: {e}")
        raise