import logging
import requests
from tenacity import retry, stop_after_attempt, wait_fixed, before_sleep_log
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_URL = os.getenv("BASE_URL")
logger = logging.getLogger(__name__)

@retry(stop=stop_after_attempt(5), wait=wait_fixed(3), before_sleep=before_sleep_log(logger, logging.WARNING))
def fetch_animal_details(animal_id):
    """Fetches the details of a specific animal by its ID"""
    try:
        logging.info(f"Fetching details for animal {animal_id}")
        response = requests.get(f"{BASE_URL}/animals/v1/animals/{animal_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch details for animal {animal_id}: {e}")
        raise


@retry(stop=stop_after_attempt(5), wait=wait_fixed(2), before_sleep=before_sleep_log(logger, logging.WARNING))
def fetch_page(page):
    """Fetches a page of animals"""
    try:
        response = requests.get(f"{BASE_URL}/animals/v1/animals", params={"page": page})
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        logging.error(f"Failed to fetch page {page} after retries: {e}")
        raise


def fetch_animals():
    """Fetches all animals across multiple pages"""
    animals = []
    page = 1
    logging.info("Starting to fetch animals")

    while True:
        try:
            response = fetch_page(page)
            if response.ok:
                data = response.json()
                logging.info(f"Successfully fetched data for page {page}: {data}")
                animals.extend(data['items'])

                if page == data['total_pages']:
                    logging.info("Reached the last page of animals.")
                    break
                page += 1
            else:
                logging.error(f"Error: Received status code {response.status_code} on page {page}")
                break
        except Exception as e:
            logging.exception(f"An error occurred while fetching page {page}: {e}")
            break

    logging.info(f"Finished fetching animals. Total animals fetched: {len(animals)}")
    return animals