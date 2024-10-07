import logging
from datetime import datetime
import pytz
from .fetching import fetch_animal_details

logger = logging.getLogger(__name__)

class Animal:
    def __init__(self, animal_info):
        self.id = animal_info["id"]
        self.name = animal_info.get("name")
        self.born_at = animal_info.get("born_at")
        self.friends = animal_info.get("friends", "")

    def transform(self):
        """Transforms the animal information"""
        try:
            logging.info(f"Starting transformation for animal {self.id}")
            details = fetch_animal_details(self.id)

            # Transform friends from a comma-separated string to a list
            self.friends = details['friends'].split(',') if 'friends' in details else []

            # Convert born_at from Unix timestamp to ISO 8601 UTC timestamp
            if self.born_at is not None:
                born_at_timestamp = self.born_at / 1000  # Convert milliseconds to seconds
                born_at = datetime.fromtimestamp(born_at_timestamp, tz=pytz.UTC)
                self.born_at = born_at.isoformat()

            logging.info(f"Finished transformation for animal {self.id}")
            return self

        except Exception as e:
            logging.exception(f"Error during transformation for animal {self.id}: {e}")
            raise