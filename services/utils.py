from datetime import datetime
import pytz
import requests
from tenacity import retry, stop_after_attempt, wait_fixed, before_sleep_log
import logging


BASE_URL = "http://localhost:3123"

logger = logging.getLogger(__name__)


"""Stop retry after 5 attempts with waiting time 3 seconds after each retry"""
@retry(stop=stop_after_attempt(5), wait=wait_fixed(3), before_sleep=before_sleep_log(logger, logging.WARNING))
def fetch_animal_details(animal_id):
    try:
        logging.info(f"Fetching details for animal {animal_id}")
        response = requests.get(f"{BASE_URL}/animals/v1/animals/{animal_id}")
        response.raise_for_status()  # Raise an exception for HTTP errors
        logging.info(f"Successfully fetched details for animal {animal_id}")
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch details for animal {animal_id}: {e}")
        raise


"""Transform animal info"""
def transform_animal(animal_info):
    try:
        id = animal_info["id"]
        logging.info(f"Starting transformation for animal {id}")
        animal = fetch_animal_details(id)

        """Transform friends from a comma-separated string to a list"""
        animal['friends'] = animal['friends'].split(',') if 'friends' in animal else []

        """Convert born_at from Unix timestamp to ISO 8601 UTC timestamp"""
        if 'born_at' in animal and animal['born_at'] is not None:
            '''Convert milliseconds to seconds'''
            born_at_timestamp = animal['born_at'] / 1000
            born_at = datetime.fromtimestamp(born_at_timestamp, tz=pytz.UTC)
            animal['born_at'] = born_at.isoformat()

        logging.info(f"Finished transformation for animal {id}: {animal}")
        return animal
    except Exception as e:
        logging.exception(f"Error during transformation for animal {animal_info['id']}: {e}")
        raise


"""Func to call POST api with retry logic"""
@retry(stop=stop_after_attempt(5), wait=wait_fixed(3), before_sleep=before_sleep_log(logger, logging.WARNING))
def post_animals(animals_batch):
    try:
        logging.info(f"Posting batch of animals: {animals_batch}")
        response = requests.post(f"{BASE_URL}/animals/v1/home", json=animals_batch)
        response.raise_for_status()
        logging.info(f"Successfully posted batch: {response.status_code}")
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Failed to post animals batch: {e}")
        raise


"""Calling POST api to post details of 100 animals at a time"""
def post_batches(animals):
    try:
        for i in range(0, len(animals), 100):
            batch = animals[i:i + 100]
            logging.info(f"Processing batch {i // 100 + 1}: {batch}")
            post_animals(batch)
        logging.info("Finished posting all batches")
    except Exception as e:
        logging.exception(f"Error posting batches of animals: {e}")
        raise