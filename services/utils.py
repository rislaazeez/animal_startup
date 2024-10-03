from datetime import datetime
import pytz
import requests
from tenacity import retry, stop_after_attempt, wait_fixed

BASE_URL = "http://localhost:3123"

@retry(stop=stop_after_attempt(5), wait=wait_fixed(3))
def fetch_animal_details(animal_id):
    response = requests.get(f"{BASE_URL}/animals/v1/animals/{animal_id}")

    # Raise an exception for HTTP errors
    response.raise_for_status()
    return response.json()

def transform_animal(animal_info):
    id = animal_info["id"]
    # Fetch animal details with retry logic
    animal = fetch_animal_details(id)
    print(f" response for animal {id} is {animal}")
    # Transform friends from a comma-separated string to a list
    animal['friends'] = animal['friends'].split(',') if 'friends' in animal else []
    
    # Convert born_at from Unix timestamp to ISO8601 UTC timestamp
    if 'born_at' in animal and animal['born_at'] is not None:
        # Convert milliseconds to seconds
        born_at_timestamp = animal['born_at'] / 1000  
        born_at = datetime.fromtimestamp(born_at_timestamp, tz=pytz.UTC) 
        animal['born_at'] = born_at.isoformat()  
    
    return animal

@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def post_animals(animals_batch):
    response = requests.post(f"{BASE_URL}/animals/v1/home", json=animals_batch)
    print("Response after post", response)
    response.raise_for_status()
    return response.json()

def post_batches(animals):
    for i in range(0, len(animals), 100):
        batch = animals[i:i + 100]
        print(f"Batch {i} is {batch}")
        post_animals(batch)