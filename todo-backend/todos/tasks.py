from celery import shared_task
import requests
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime

# MongoDB setup
MONGO_CLIENT = MongoClient(
    "mongodb+srv://rajavatshersinh_db_user:Rajawat@data.s6e82vc.mongodb.net/?appName=data"
)
MONGO_DB = MONGO_CLIENT["Stock_Data"]

@shared_task
def fetch_top_gainers_task():
    """
    Celery task to fetch top gainers from NSE and save to MongoDB.
    Runs every 3 minutes from 9:15 AM to 10:30 AM, Monday to Friday.
    """
    try:
        # NSE API details
        url = "https://www.nseindia.com/api/live-analysis-variations?index=gainers"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "application/json",
            "Referer": "https://www.nseindia.com/market-data/top-gainers-losers"
        }

        # Create session and fetch data
        session = requests.Session()
        session.get("https://www.nseindia.com", headers=headers, timeout=10)
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()

        # Check API response structure
        if "allSec" not in data or "data" not in data["allSec"]:
            raise ValueError("Invalid API response structure")

        top_stocks = data["allSec"]["data"]

        # Prepare data for MongoDB
        collection = MONGO_DB["top_gainers"]
        # Clear today's data
        collection.delete_many({})
        # Insert fresh data with timestamp
        for stock in top_stocks:
            stock['timestamp'] = datetime.utcnow()
        collection.insert_many(top_stocks)

        logging.info(f"Successfully fetched and saved {len(top_stocks)} top gainers to MongoDB.")
        return f"Fetched {len(top_stocks)} top gainers"

    except requests.RequestException as e:
        logging.error(f"API request failed: {str(e)}")
        raise
    except (KeyError, ValueError) as e:
        logging.error(f"Data processing error: {str(e)}")
        raise
    except ConnectionFailure as e:
        logging.error(f"MongoDB connection failed: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error in fetch_top_gainers_task: {str(e)}")
        raise
