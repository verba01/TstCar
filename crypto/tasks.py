from celery import shared_task
from .models import Price
import websockets
import json
import asyncio
from asgiref.sync import sync_to_async

@shared_task
def fetch_and_save_prices():
    async def fetch_prices():
        uri = "wss://stream.binance.com:9443/ws/btcusdt@trade"
        async with websockets.connect(uri) as websocket:
            data = await websocket.recv()
            data = json.loads(data)
            price = data['p']
            symbol = "BTC/USDT"
            await save_price(symbol, price)

    @sync_to_async
    def save_price(symbol, price):
        Price.objects.create(symbol=symbol, price=price)

    asyncio.run(fetch_prices())