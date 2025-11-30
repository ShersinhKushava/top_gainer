import requests
from datetime import datetime

# NSE URL
url = "https://www.nseindia.com/api/live-analysis-variations?index=gainers"
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://www.nseindia.com/market-data/top-gainers-losers"
}

try:
    session = requests.Session()
    session.get("https://www.nseindia.com", headers=headers, timeout=10)
    response = session.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    data = response.json()
    print("API response received successfully")
    print("Keys in data:", list(data.keys()))

    if "allSec" in data:
        print("allSec present")
        if "data" in data["allSec"]:
            print("data present in allSec")
            print("Number of stocks:", len(data["allSec"]["data"]))
        else:
            print("data not in allSec")
    else:
        print("allSec not in data")

except Exception as e:
    print(f"Error: {str(e)}")
