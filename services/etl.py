# services/etl.py
import requests
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed
from .utils import transform_animal, post_batches

BASE_URL = "http://localhost:3123"


@retry(stop=stop_after_attempt(5), wait=wait_fixed(2),retry=retry_if_exception_type(requests.RequestException))
def fetch_page(page):
    response = requests.get(f"{BASE_URL}/animals/v1/animals", params={"page": page})
    response.raise_for_status()
    return response

def fetch_animals():
    animals = []
    page = 1
    while True:
        response = fetch_page(page)
        # Check if the response is successful
        if response.ok: 
            data = response.json()
            print("data", data)

            # Extend the animals list with items from the response
            animals.extend(data['items'])

            # Check if we have reached the last page
            if page == data['total_pages']:
                break
            page += 1
        else:
            print(f"Error: Received status code {response.status_code}")
            break  # Exit the loop on error

    return animals

async def run_etl():
    animals = fetch_animals()
    # transformed_animals = [transform_animal(animal) for animal in animals]
    # post_batches(transformed_animals)