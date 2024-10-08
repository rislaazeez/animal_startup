from fastapi import FastAPI
from config import configure_logging
from services.etl import run_etl

app = FastAPI()

configure_logging()

@app.post("/run-etl")
async def run_etl_route():
    # Call the ETL process asynchronously
    await run_etl()

    return {"message": "ETL process completed successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")