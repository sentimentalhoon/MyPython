import sys
from kafka import KafkaConsumer
import redis
import json
import time
rd = redis.StrictRedis(host='59.3.28.12', port=6379, db=0, password='sam9mo!!')

STOCK_CODE_TICKERS = {}

def consume_messages():
    # Create a Consumer instance
    print('==========================================================')
    print('[korea_stock_hoka] Start!')
    print('==========================================================')
    CARD_TOPIC = 'korea_stock_hoka'

    brokers = ['59.3.28.12:9092', '59.3.28.12:9093', '59.3.28.12:9094']
    consumer = KafkaConsumer(
        CARD_TOPIC, 
        bootstrap_servers=brokers, 
        #auto_offset_reset='earliest'
        )
    for msg in consumer:
        consumerValue = msg.value.decode('utf-8').replace("[", "").replace("]", "").replace("\"", "").replace(" ", "").split(",")
        valuation = {
            "id" : consumerValue[0],
            "stockCode" : consumerValue[0],
            "tradeTime" : consumerValue[1],
            "askPrice10" : consumerValue[12],
            "askPrice09" : consumerValue[11],
            "askPrice08" : consumerValue[10],
            "askPrice07" : consumerValue[9],
            "askPrice06" : consumerValue[8],
            "askPrice05" : consumerValue[7],
            "askPrice04" : consumerValue[6],
            "askPrice03" : consumerValue[5],
            "askPrice02" : consumerValue[4],
            "askPrice01" : consumerValue[3],
            "askSize10" : consumerValue[32],
            "askSize09" : consumerValue[31],
            "askSize08" : consumerValue[30],
            "askSize07" : consumerValue[29],
            "askSize06" : consumerValue[28],
            "askSize05" : consumerValue[27],
            "askSize04" : consumerValue[26],
            "askSize03" : consumerValue[25],
            "askSize02" : consumerValue[24],
            "askSize01" : consumerValue[23],
            "bidPrice01" : consumerValue[13],
            "bidPrice02" : consumerValue[14],
            "bidPrice03" : consumerValue[15],
            "bidPrice04" : consumerValue[16],
            "bidPrice05" : consumerValue[17],
            "bidPrice06" : consumerValue[18],
            "bidPrice07" : consumerValue[19],
            "bidPrice08" : consumerValue[20],
            "bidPrice09" : consumerValue[21],
            "bidPrice10" : consumerValue[22],
            "bidSize01" : consumerValue[33], 
            "bidSize02" : consumerValue[34], 
            "bidSize03" : consumerValue[35], 
            "bidSize04" : consumerValue[36], 
            "bidSize05" : consumerValue[37], 
            "bidSize06" : consumerValue[38], 
            "bidSize07" : consumerValue[39], 
            "bidSize08" : consumerValue[40], 
            "bidSize09" : consumerValue[41], 
            "bidSize10" : consumerValue[42],
            "totalAskSize" : consumerValue[43], # 총매도호가
            "totalBidSize" : consumerValue[44], # 총매수호가
        }

        # STOCK_CODE_TICKERS[consumerValue[0]] = consumerValue
        rd.set("stock:" + consumerValue[0], json.dumps(valuation, ensure_ascii=False).encode('utf-8'))
        #time.sleep(0.1)

consume_messages()