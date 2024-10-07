from datetime import datetime
from .animal import Animal
from .fetching import fetch_animals
from .posting import post_batches
import logging

logger = logging.getLogger(__name__)

async def run_etl():
    start_time = datetime.now()
    logger.info(f"ETL started at {start_time}")
    animals_data = fetch_animals()
    transformed_animals = [Animal(animal).transform() for animal in animals_data]
    post_batches([animal.__dict__ for animal in transformed_animals])
    end_time = datetime.now()
    logger.info(f"ETL finished at {end_time}")
    logger.info(f"Total duration: {end_time - start_time}")