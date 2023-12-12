from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Response
import json
import asyncio
from pymongo import MongoClient
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI
import uvicorn
import time
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from stock_API_output2 import get_domestic_stock_price
from STOCKCODE import STOCK_CODE, KOSPI_STOCK_CODE, KOSDAQ_STOCK_CODE
#from kafka import KafkaProducer
import json
import time
import threading
import redis
from ast import literal_eval
import tenacity
from kafka import KafkaProducer
from kafka.structs import TopicPartition
from kafka import KafkaConsumer

#------------------------------------------------------------------------------------

STOCK_CODE_TICKERS = {}

# 현재시간 호출
current_hour = int(datetime.now().strftime("%H%M")) 
    
#-------------------------------------------------------------------------------------
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

# 브로커와 토픽명을 지정한다.
brokers = ['59.3.28.12:9092', '59.3.28.12:9093', '59.3.28.12:9094']
topic = "fastapi_check"
pr = MessageProducer(brokers, topic)

def check_message(content1:str, content2:str):
    check_message ={    #현황체크
                    "consummer" : "stock_api",
                    "check_situation" : content1,
                    "ERROR_content" : content2
            }
    pr.send_message(check_message,False)# kafka전달turn document

#-------------------------------------------------------------------------------------
receive_korea_stock_message_task = None
initial_restart_threading_timer = None
def onStartUp():    
    global initial_restart_threading_timer
    initial_restart_threading_timer = threading.Timer(3600, initial_restart)
    start_Server()
    print('server start')
def onShutDown():
    receive_korea_stock_message_task.cancel()
    initial_restart_threading_timer.cancel()

app = FastAPI(on_startup=[onStartUp], on_shutdown=[onShutDown])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# param에 담기는 데이터 형식을 정형화
# company: str
# initial: list
# current_trade: list
class Item(BaseModel):  #BaseModel은 정형화하기 위함
    company: str    # 회사는 단일(str)
    initial: list   # initial에 해당하는 컬럼은 list
    current_trade: list # current_trade에 해당하는 컬럼은 list

#
def makeData(company: str, initial: list, current_trade: list):
    stockData = {}  # 최종 데이터를 담을 dict
    stockData[company] = {} # 일단 회사num을 key지정해놓는다
    try:
        responseJsonCompanyInfo = STOCK_CODE_TICKERS[company]
        responseInitial = responseJsonCompanyInfo['initial']
        responseCurrentTrade = responseJsonCompanyInfo['current_trade']
        # responseJsonCompanyInfo에 담겨있는 데이터 형태
        # stockData ={
        #       company : {
        #                     initial : {},
        #                     current_trade : {}
        #                   }
        #            }

        initialData = {}
        if (len(responseInitial) > 0):  # responseInitial은 리스트 형태이다! 배열의 길이를 체크
            for key, value in responseInitial.items():
                if key in initial:  # initial은 자료형이 리스트임                           
                    initialData.update({key : value }) 

        stockData[company]['initial'] = initialData

        currentTradeData = {}
        if (len(responseCurrentTrade) > 0):  # responseCurrentTrade은 리스트 형태이다! 배열의 길이를 체크
            for key, value in responseCurrentTrade.items():
                if key in current_trade:  # # responseInitial은 자료형이 리스트임    
                    currentTradeData.update({key : value })

        stockData[company]['current_trade'] = currentTradeData
    except Exception as e:
        stockData = { "status" : "error" }
        print(f'::::::: makeData Error => {e}')        
    finally:
        return stockData


@app.post(path="/stock_api",
         name="실시간 종목별 데이터API",
         description="코스피, 코스닥 각40종목씩 실시간 거래 및 자본,재무정보 확인가능",
         )
def consummer(item: Item):
    if STOCK_CODE_TICKERS is not None:
        company = item.company
        initial = item.initial
        current_trade = item.current_trade
        returnData = {}
        if company != '0':
            # STOCK_CODE_TICKERS에 들어오는 dict의 key값이 일치하는 지 확인
            if company in STOCK_CODE_TICKERS:
                # 일치하는 key값이 있을 경우 그에 해당하는 데이터 추출
                returnData.update(makeData(company, initial, current_trade))  
            else:
                # STOCK_CODE_TICKERS에에 들어있는 key값이 없을시 실행
                returnData = { "status" : "company is not found"}
        else:
            # 0을 입력시 모든 데이터를 추출함            
            for companyCode in STOCK_CODE_TICKERS:
                returnData.update(makeData(companyCode, initial, current_trade))
                
        return returnData
    else:
        return { "status" : "none" }  


@app.get(path="/stock_api_all")
def stock_appi_all():
    return STOCK_CODE_TICKERS

# 1시간 마다 initial값을 초기화합니다!
def initial_restart():
    # 오늘 날짜 가져오기
    today = datetime.today().strftime("%Y%m%d")
    # 초기값을 몽고DB의
    # time.sleep(10)
    print("inital ok") 
    for key, value in STOCK_CODE.items():
        result = get_domestic_stock_price(key,today,today)
        if result:
            stock_data = result["output1"]
            if stock_data:
                stock_data["COMPANY"] = value
                STOCK_CODE_TICKERS[key] = {
                    "initial":stock_data,    # API로 가져온 값
                    "current_trade": ""         # websocket의 변화되는 거래값 
                    }      
    initial_restart_threading_timer.start()# 한시간마다 재귀함수로 다시 돌고 있음!!!

async def receive_korea_stock_message():
    global finalConsumerTime
    PAYMENT_TOPIC = 'stock_api'
    brokers = ['59.3.28.12:9092', '59.3.28.12:9093', '59.3.28.12:9094']
    consumer = KafkaConsumer(
        topics=PAYMENT_TOPIC,
        bootstrap_servers=brokers,
        value_deserializer=lambda m:json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest'
    )
    
    try:
        for message in consumer:
            try :
                print(message)
                STOCK_CODE_TICKERS[message.value["MKSC_SHRN_ISCD"]]["current_trade"] = message.value
                finalConsumerTime = time.time()
            except Exception as e:
                continue
    except Exception as e:
        check_message("ERROR", e)
        print(e)

# fastapi startup
def start_Server():
    initial_restart(),
    global receive_korea_stock_message_task
    receive_korea_stock_message_task = asyncio.create_task(    receive_korea_stock_message()    )

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8821)
