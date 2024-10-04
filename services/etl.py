import logging
import requests
from tenacity import before_sleep_log, retry, retry_if_exception_type, stop_after_attempt, wait_fixed
from .utils import transform_animal, post_batches

BASE_URL = "http://localhost:3123"


logger = logging.getLogger(__name__)

"""Stop retry after 5 attempts with waiting time 3 seconds after each retry"""
@retry(stop=stop_after_attempt(5), 
       wait=wait_fixed(2),
       retry=retry_if_exception_type(requests.RequestException),
       before_sleep=before_sleep_log(logger, logging.WARNING))
def fetch_page(page):
    try:
        response = requests.get(f"{BASE_URL}/animals/v1/animals", params={"page": page})
        response.raise_for_status()
        return response
    
    except requests.RequestException as e:
        """Log error after retries are exhausted"""
        logging.error(f"Failed to fetch page {page} after retries: {e}")
        raise


"""Fetch animals until last page"""
def fetch_animals():
    animals = []
    page = 1

    logging.info("Starting to fetch animals")

    while True:
        try:
            # Fetch the page
            response = fetch_page(page)

            # Check if the response is successful
            if response.ok:
                data = response.json()
                logging.info(f"Successfully fetched data for page {page}: {data}")

                # Extend the animals list with items from the response
                animals.extend(data['items'])

                # Check if we have reached the last page
                if page == data['total_pages']:
                    logging.info("Reached the last page of animals.")
                    break
                page += 1
            else:
                # Log the error if the status code is not 200
                logging.error(f"Error: Received status code {response.status_code} on page {page}")
                break
        except Exception as e:
            # Log unexpected exceptions
            logging.exception(f"An error occurred while fetching page {page}: {e}")
            break

    logging.info(f"Finished fetching animals. Total animals fetched: {len(animals)}")
    return animals



"""Run ETL Asynchronously"""
async def run_etl():
    animals = fetch_animals()
    transformed_animals = [transform_animal(animal) for animal in animals]
    post_batches(transformed_animals)