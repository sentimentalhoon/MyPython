from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio

from fastapi import FastAPI, Request

import uvicorn
import logging

from sse_starlette.sse import EventSourceResponse

from kafkaConsumer.UpbitConsumer import  receiveUpbitMessage, loadKrwCoinTickersTradePriceApi, loadKrwCoinTickersAll, initializeUpbit
from kafkaConsumer.KoreaStockConsumer import receiveKoreaStockMessage, loadStockCodeTickers, initializeKoreaStock

# TEST Brokers IP

# BROKERS_IP = '59.3.28.12'

# BROKERS = [f'{BROKERS_IP}:19092', f'{BROKERS_IP}:19093', f'{BROKERS_IP}:19094']

# Docker Container 내부 IP 주소와 포트
BROKERS = ['172.18.0.8:19092', '172.18.0.7:19093', '172.18.0.6:19094']

# Websocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except WebSocketDisconnect as e: # 웹소켓이 닫힌 경우 예외 처리
                print(f"WebSocket disconnected : {e}")
                self.disconnect(connection) # 웹소켓을 목록에서 제거
            except Exception as e: # 웹소켓이 닫힌 경우 예외 처리
                print(f"Error : {e}")

# initialize logger
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)

# kospi, kosdaq WebsocketManager Init
koreaStockWebsocketManager = ConnectionManager()
# upbit coin websocketManager Init
upbitWebsocketManager = ConnectionManager()

# global variables task init
upbit_consumer_task = None
korea_stock_consumer_task = None
sendUpbitPriceByWebSocket_task = None
sendKoreaStockPriceByWebSocket_task = None

# sse event send delay
MESSAGE_STREAM_DELAY = 1  # second
# MESSAGE_STREAM_RETRY_TIMEOUT = 15000  # milisecond

# fastapi Start up!
async def onStartUp():
    log.info('Initializing API ...')
    await initializeKoreaStock(BROKERS)
    await initializeUpbit(BROKERS)
    await consumerTaskStart()

# fastapi Shut Down!
async def onShutDown():
    log.info('Shutting down API')
    upbit_consumer_task.cancel()
    korea_stock_consumer_task.cancel()
    sendUpbitPriceByWebSocket_task.cancel()
    sendKoreaStockPriceByWebSocket_task.cancel()

app = FastAPI(on_startup=[onStartUp], on_shutdown=[onShutDown])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
'''
upbit coin 가격만 제공하는 api 주소
'''
@app.get('/api/coin/tradeprice')
async def krwCoinTradePrice():
    return json.dumps(loadKrwCoinTickersTradePriceApi())

'''
upbit coin 의 모든 실시간 거래 정보 제공 api 주소
'''
@app.get('/api/coin/all')
async def krwCoinAll():
    return json.dumps(loadKrwCoinTickersAll())

'''
kospi, kosdaq 실시간 거래 정보 제공 api 주소
'''
@app.get('/api/stock/all')
async def koreaStockAll():
    return json.dumps(loadStockCodeTickers())

'''
kospi, kosdaq 실시간 websocket
'''
@app.websocket("/ws/koreastock")
async def koreaStockWebsocketEndpoint(websocket: WebSocket):
    await koreaStockWebsocketManager.connect(websocket)
    try:
        while True:
            # 웹소켓으로부터 텍스트 데이터를 수신합니다.
            await websocket.receive_text()
            # 웹소켓으로 텍스트 데이터를 전송합니다.
    except WebSocketDisconnect as e:
        koreaStockWebsocketManager.disconnect(websocket)
    except Exception as e:
        print(f'websocket_endpoint {e}')

'''
upbit coin 실시간 websocket
'''
@app.websocket("/ws/upbit")
async def upbitWebsocketEndpoint(websocket: WebSocket):
    await upbitWebsocketManager.connect(websocket)
    try:
        while True:
            # 웹소켓으로부터 텍스트 데이터를 수신합니다.
            await websocket.receive_text()
            # 웹소켓으로 텍스트 데이터를 전송합니다.
    except WebSocketDisconnect as e:
        upbitWebsocketManager.disconnect(websocket)
    except Exception as e:
        print(f'websocket_endpoint {e}')

'''
upbit coin SSE 처리
'''
@app.get("/krwcoinallstream")
async def message_stream(request: Request):
    async def event_generator():
        while True:
            if await request.is_disconnected():
                log.debug("Request disconnected")
                break

            yield json.dumps(loadKrwCoinTickersAll())
            await asyncio.sleep(MESSAGE_STREAM_DELAY)

    return EventSourceResponse(event_generator())

'''
upbit coin only price SSE 처리
'''
@app.get("/krwcoinstream")
async def message_stream(request: Request):
    async def event_generator():
        while True:
            if await request.is_disconnected():
                log.debug("Request disconnected")
                break

            yield json.dumps(loadKrwCoinTickersTradePriceApi())
            await asyncio.sleep(MESSAGE_STREAM_DELAY)

    return EventSourceResponse(event_generator())

'''
kospi, kosdaq 실시간 거래 SSE 처리
'''
@app.get("/koreastockstream")
async def message_stream(request: Request):
    async def event_generator():
        while True:
            if await request.is_disconnected():
                log.debug("Request disconnected")
                break

            yield json.dumps(loadStockCodeTickers())
            await asyncio.sleep(MESSAGE_STREAM_DELAY)

    return EventSourceResponse(event_generator())

'''
/ws/upbit 로 접속한 websocket 사용자들에게 코인 정보를 보낸다.
'''
async def sendUpbitPriceByWebSocket():
    while True:
        try:
            await upbitWebsocketManager.broadcast(json.dumps(loadKrwCoinTickersAll()))
            await asyncio.sleep(0.5)
        except Exception as e:
            continue

'''
/ws/koreastock 으로 접속한 websocket 사용자들에게 주식 정보를 보낸다.
'''
async def sendKoreaStockPriceByWebSocket():
    while True:
        try:
            await koreaStockWebsocketManager.broadcast(json.dumps(loadStockCodeTickers()))
            await asyncio.sleep(0.5)
        except Exception as e:
            continue

'''
task 생성
'''
async def consumerTaskStart():
    global upbit_consumer_task
    upbit_consumer_task = asyncio.create_task(receiveUpbitMessage())
    global korea_stock_consumer_task
    korea_stock_consumer_task = asyncio.create_task(receiveKoreaStockMessage())
    global sendUpbitPriceByWebSocket_task
    sendUpbitPriceByWebSocket_task = asyncio.create_task(sendUpbitPriceByWebSocket())
    global sendKoreaStockPriceByWebSocket_task
    sendKoreaStockPriceByWebSocket_task = asyncio.create_task(sendKoreaStockPriceByWebSocket())
    
if __name__ == "__main__":
    # TODO 로컬 배포
    #uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
    # TODO 실서버 배포
    uvicorn.run(app, host="0.0.0.0", port=9100)