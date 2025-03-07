import json
import asyncio
import websockets
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Price
from asgiref.sync import sync_to_async

class BinanceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("prices", self.channel_name)
        await self.receive_binance_data()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("prices", self.channel_name)

    async def receive_binance_data(self):
        uri = "wss://stream.binance.com:9443/ws/btcusdt@trade"
        async with websockets.connect(uri) as websocket:
            while True:
                data = await websocket.recv()
                data = json.loads(data)
                price = data['p']  # Цена
                symbol = "BTC/USDT"  # Пара
                await self.save_price(symbol, price)
                await self.channel_layer.group_send(
                    "prices",
                    {
                        "type": "price_update",
                        "symbol": symbol,
                        "price": price,
                    }
                )

    async def price_update(self, event):
        await self.send(text_data=json.dumps({
            'symbol': event['symbol'],
            'price': event['price'],
        }))

    @sync_to_async
    def save_price(self, symbol, price):
        Price.objects.create(symbol=symbol, price=price)