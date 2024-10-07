# Animal Startup ETL Processor

This project is an **ETL (Extract, Transform, Load)** pipeline designed to fetch animal data from an API, transform it, and post the data to another endpoint. The project leverages asynchronous requests to improve performance, making the process efficient even for large datasets.

## Features

- Fetches paginated animal data from an API.
- Asynchronously transforms and posts the data in batches.
- Retry mechanisms using `Tenacity` to ensure resilience in case of failures.
- Separation of concerns by organizing logic into individual classes and functions for better maintainability.

## Tech Stack

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python.
- **Python**: Core language used for implementing the ETL logic.
- **Requests**: Used for making HTTP requests to the external API.
- **Tenacity**: A library for retrying operations when certain conditions are met.
- **Docker**: Used to run the external API server for fetching animal data.

## Prerequisites

- Python 3.8+
- pip
- Docker
- virtualenv


## Installation

1. Clone the repository:
```bash
git clone https://github.com/rislaazeez/animal_startup.git
cd animal_startup
```

2. Set up the virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a .env file to store the API base URL.

## Run

1. Run the Docker container and expose port 3123. Check if the API is running by navigating to http://localhost:3123 in your browser.

2. Run the FastAPI application:
```bash
uvicorn app:app --reload
```

The application will be accessible at http://127.0.0.1:8000.

## API Endpoints

	- GET /run-etl: Triggers the ETL process.
	•	Fetches all animal data.
	•	Transforms the data (converts timestamps, formats friends as lists).
	•	Posts the transformed data in batches.

## Logging

This application uses Python’s built-in logging system to log important information, such as:

	•	Successful fetching and posting of data.
	•	Errors encountered during the process.
	•	Retry attempts for failed requests.

## Error Handling & Retry Logic

	•	Tenacity is used to provide retry logic for API calls.
	•	The application retries API calls up to 5 times with a fixed wait time between each retry.