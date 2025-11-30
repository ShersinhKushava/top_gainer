# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Stock
from .serializers import StockSerializer
import requests
from django.conf import settings
from datetime import datetime
from pymongo.errors import ConnectionFailure

def safe_float(value, default=0.0):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default




@api_view(['GET', 'POST'])
def stock_list(request):
    if request.method == 'GET':
        stocks = Stock.objects.all()
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = StockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def stock_detail(request, pk):
    try:
        stock = Stock.objects.get(id=pk)
    except Stock.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StockSerializer(stock)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = StockSerializer(stock, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        stock.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def top_gainers(request):
    """
    Fetch NSE Top Gainers, save them in MongoDB inside a DAILY collection,
    and return today's saved data.
    """

    # NSE URL
    url = "https://www.nseindia.com/api/live-analysis-variations?index=gainers"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": "https://www.nseindia.com/market-data/top-gainers-losers"
    }

    try:
        # --- 1. Prepare Today's Collection Name ---
        today = datetime.utcnow().strftime("%d-%m-%Y")    # e.g. "30-11-2025"
        collection_name = f"gainers_{today}"              # e.g. "gainers_30-11-2025"

        db = settings.MONGO_DB
        collection = db[collection_name]   # dynamic collection

        # --- 2. Fetch NSE Data ---
        session = requests.Session()
        session.get("https://www.nseindia.com", headers=headers, timeout=10)
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()

        # Check API response structure
        if "allSec" not in data or "data" not in data["allSec"]:
            raise ValueError("Invalid API response structure")

        top_stocks = []
        for stock in data["allSec"]["data"][:20]:
            top_stocks.append({
                "symbol": stock.get("symbol"),
                "LTP": safe_float(stock.get("ltp", 0)),
                "open": safe_float(stock.get("open_price", 0)),
                "previous_close": safe_float(stock.get("prev_price", 0)),
                "%change": safe_float(stock.get("net_price", 0)),
                "high": safe_float(stock.get("high_price", 0)),
                "low": safe_float(stock.get("low_price", 0)),
                "volume": safe_int(stock.get("trade_quantity", 0)),
                "timestamp": datetime.utcnow()
            })

        # --- 3. Save inside today’s collection ---
        try:
            collection.delete_many({})          # clear only today's data
            collection.insert_many(top_stocks)  # insert fresh data
        except ConnectionFailure:
            return Response({"error": "Database connection failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # --- 4. Fetch data from today’s collection ---
        try:
            saved_data = list(collection.find({}, {"_id": 0}))
        except ConnectionFailure:
            return Response({"error": "Database query failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(saved_data, status=200)

    except requests.RequestException as e:
        return Response({"error": f"API request failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except (KeyError, ValueError) as e:
        return Response({"error": f"Data processing error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
