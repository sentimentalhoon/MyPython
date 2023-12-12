import multiprocessing as mp
import pyupbit
import datetime
import time
from kafka import KafkaProducer
import json

class MessageProducer:
    def __init__(self, broker, topic):
        self.broker = broker      
        self.topic = topic 
        self.producer = KafkaProducer(
            bootstrap_servers=self.broker,
            value_serializer=lambda x: json.dumps(x).encode("utf-8"),
            acks=0,
            api_version=(2, 5, 0),
            retries=3,
        )

    def send_message(self, msg, auto_close=False):
        try:
            future = self.producer.send(self.topic, msg)
            self.producer.flush()  # 비우는 작업
            if auto_close:
                self.producer.close()
            future.get(timeout=2)
            return {"status_code": 200, "error": None}
        except Exception as exc:
            raise exc

if __name__ == "__main__":
    krw_tickers = pyupbit.get_tickers(fiat="KRW")
    queue = mp.Queue()
    proc = mp.Process(
        target=pyupbit.WebSocketClient,
        args=('ticker', krw_tickers, queue),
        daemon=True
    )
    proc.start()
    TOPIC = 'upbit'
    brokers = ['59.3.28.12:9092', '59.3.28.12:9093', '59.3.28.12:9094']
    pd = MessageProducer(brokers, TOPIC)
    print(krw_tickers)
    
    while True:
        data = queue.get()
        print(data)
        pd.send_message(data, False)