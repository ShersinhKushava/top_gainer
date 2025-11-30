import requests
import pandas as pd
import logging

def get_all_top_gainers():
    url = "https://www.nseindia.com/api/live-analysis-variations?index=gainers"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json",
        "Referer": "https://www.nseindia.com/market-data/top-gainers-losers"
    }

    try:
        s = requests.Session()
        s.get("https://www.nseindia.com", headers=headers, timeout=10)
        r = s.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()   # SAFE — we know it returns JSON

        # extract ALL securities
        all_stocks = data.get("allSec", {}).get("data", [])
        if not all_stocks:
            logging.warning("No data found under 'allSec.data' in NSE response.")
            return pd.DataFrame()

        # convert into DataFrame
        df = pd.DataFrame(all_stocks)

        # rename columns for clarity
        df = df.rename(columns={
            "open_price": "open",
            "prev_price": "previous_close",
            "net_price": "%change",
            "high_price": "high",
            "low_price": "low",
            "ltp": "LTP",
            "trade_quantity": "volume"
        })

        return df

    except requests.RequestException as e:
        logging.error(f"Request failed in get_all_top_gainers: {e}")
    except ValueError as e:
        logging.error(f"JSON decoding failed in get_all_top_gainers: {e}")
    except Exception as e:
        logging.error(f"Unexpected error in get_all_top_gainers: {e}")

    # Return empty DataFrame on error
    return pd.DataFrame()
