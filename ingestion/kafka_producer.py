import json
import time
import yfinance as yf
from kafka import KafkaProducer
from datetime import datetime

PRODUCER = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

STOCKS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
TOPIC = 'stock_ticks'

def fetch_and_produce():
    while True:
        for symbol in STOCKS:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period='1d', interval='1m').tail(1)
            if not data.empty:
                record = {
                    'symbol': symbol,
                    'timestamp': datetime.utcnow().isoformat(),
                    'open': round(float(data['Open'].iloc[0]), 2),
                    'high': round(float(data['High'].iloc[0]), 2),
                    'low': round(float(data['Low'].iloc[0]), 2),
                    'close': round(float(data['Close'].iloc[0]), 2),
                    'volume': int(data['Volume'].iloc[0])
                }
                PRODUCER.send(TOPIC, value=record)
                print(f"[PRODUCED] {record}")
        time.sleep(60)  # Fetch every minute

if __name__ == '__main__':
    fetch_and_produce()
