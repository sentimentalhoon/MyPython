import json
import logging

from kafka import TopicPartition
from aiokafka import AIOKafkaConsumer
from typing import Set, Any

# initialize logger
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)
STOCK_CODE = ["005930", "373220", "000660", "207940", "005935", "005380", "005490", "051910", "000270", "035420","006400", "068270", "003670", "105560", "028260","012330", "035720", "055550", "066570", "032830",]

STOCK_CODE_TICKERS = {}
for i in STOCK_CODE:
    STOCK_CODE_TICKERS[i] = 0

async def receiveKoreaStockMessage():
    global STOCK_CODE_TICKERS 
    try:
        async for message in koreaStockConsumer:
            messageValueStr = json.loads(message.value.decode('utf-8'))
            # print(f'||| receive_korea_stock_message ||| {messageValueStr}')
            STOCK_CODE_TICKERS[messageValueStr['MKSC_SHRN_ISCD']] = messageValueStr
            # print(message.value['code'])
            # await manager.broadcast(json.dumps(STOCK_CODE_TICKERS))
    except Exception as e:
        print(f'||| receive_korea_stock_message ||| {e}')
    finally:
        # will leave consumer group; perform autocommit if enabled
        log.warning('receive_korea_stock_message Stopping korea_stock_consumer')
        await koreaStockConsumer.stop()

def loadStockCodeTickers():
    return STOCK_CODE_TICKERS


async def initializeKoreaStock(BROKERS):
    # loop = asyncio.get_event_loop()
    global koreaStockConsumer
    KAFKA_TOPIC = 'stock_api'
    koreaStockConsumer = AIOKafkaConsumer(KAFKA_TOPIC,
                                         bootstrap_servers=BROKERS)
    # get cluster layout and join group
    await koreaStockConsumer.start()

    partitions: Set[TopicPartition] = koreaStockConsumer.assignment()
    nr_partitions = len(partitions)
    if nr_partitions != 1:
        log.warning(f'Found {nr_partitions} partitions for topic {KAFKA_TOPIC}. Expecting '
                    f'only one, remaining partitions will be ignored!')
    for tp in partitions:

        # get the log_end_offset
        end_offset_dict = await koreaStockConsumer.end_offsets([tp])
        end_offset = end_offset_dict[tp]

        if end_offset == 0:
            log.warning(f'Topic ({KAFKA_TOPIC}) has no messages (log_end_offset: '
                        f'{end_offset}), skipping initialization ...')
            return

        log.debug(f'Found log_end_offset: {end_offset} seeking to {end_offset-1}')
        koreaStockConsumer.seek(tp, end_offset-1)
        msg = await koreaStockConsumer.getone()
        log.info(f'Initializing API with data from msg: {msg}')
        return