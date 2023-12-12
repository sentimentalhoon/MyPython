import multiprocessing as mp
import pyupbit

from kafka import KafkaProducer
import json
from dotenv import load_dotenv
import os
from datetime import datetime, time

SERVER_IP = '59.3.28.12'

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
def getMarketAll():
    import requests
    header = {'Content-Type': 'application/json; charset=utf-8'}
    response = requests.get('https://api.upbit.com/v1/market/all', headers=header)
    return response.json()

if __name__ == "__main__":
    coinKrNames = getMarketAll()
    krw_tickers = pyupbit.get_tickers(fiat="KRW")
    queue = mp.Queue()
    proc = mp.Process(
        target=pyupbit.WebSocketClient,
        args=('ticker', krw_tickers, queue),
        daemon=True
    )
    
    proc.start()
    TOPIC = 'upbit'
    brokers = ['{SERVER_IP}:9092', '{SERVER_IP}:9093', '{SERVER_IP}:9094']
    pd = MessageProducer(brokers, TOPIC)
    print('=================================================================')
    print(f'Upbit Coin Producer Start!! | {datetime.now()}')
    print('=================================================================')
    while True:
        try:
            data = queue.get()
            code = data['code']
            for value in coinKrNames:
                if (value['market'] == code):
                    data['codeKr'] = value['korean_name']
                    data['codeEn'] = value['english_name']
                    break
            # open = data['opening_price']
            # high = data['high_price']
            # low  = data['low_price']
            # close = data['trade_price']
            # ts = data['trade_timestamp']
            # acc_volume = data['acc_trade_volume']
            # acc_price = data['acc_trade_price']
            # acc_ask_volume = data['acc_ask_volume']
            # acc_bid_volume = data['acc_bid_volume']
            # change_rate = data['signed_change_rate']
            pd.send_message(data, False)
            # print(data)
            # print(dt, code, open, high, low, close, acc_volume, acc_price, change_rate)
        except Exception as e:
            print(f'pyupbit.get_tickers ERROR {datetime.now()}=> {e}')
            print('=================================================================')
            continue
    