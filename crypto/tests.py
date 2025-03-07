import pytest
from channels.testing import WebsocketCommunicator
from .consumers import BinanceConsumer  # Исправлен импорт
from .models import Price  # Исправлен импорт

@pytest.mark.asyncio
async def test_price_consumer():
    communicator = WebsocketCommunicator(BinanceConsumer.as_asgi(), "/ws/prices/")
    connected, _ = await communicator.connect()
    assert connected

    await communicator.disconnect()

@pytest.mark.django_db
def test_price_model():
    price = Price.objects.create(symbol="BTC/USDT", price="50000.00")
    assert price.symbol == "BTC/USDT"
    assert price.price == "50000.00"