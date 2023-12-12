import json
import logging

from kafka import TopicPartition
from aiokafka import AIOKafkaConsumer
from typing import Set, Any

# initialize logger
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)

KRW_TICKERS_VALUE = ['KRW-BTC', 'KRW-ETH', 'KRW-NEO', 'KRW-MTL', 'KRW-XRP', 'KRW-ETC', 'KRW-SNT', 'KRW-WAVES', 'KRW-XEM', 'KRW-QTUM', 'KRW-LSK', 'KRW-STEEM', 'KRW-XLM', 'KRW-ARDR', 'KRW-ARK', 'KRW-STORJ', 'KRW-GRS', 'KRW-ADA', 'KRW-SBD', 'KRW-POWR', 'KRW-BTG', 'KRW-ICX', 'KRW-EOS', 'KRW-TRX', 'KRW-SC', 'KRW-ONT', 'KRW-ZIL', 'KRW-POLYX', 'KRW-ZRX', 'KRW-LOOM', 'KRW-BCH', 'KRW-BAT', 'KRW-IOST', 'KRW-CVC', 'KRW-IQ', 'KRW-IOTA', 'KRW-HIFI', 'KRW-ONG', 'KRW-GAS', 'KRW-UPP', 'KRW-ELF', 'KRW-KNC', 'KRW-BSV', 'KRW-THETA', 'KRW-QKC', 'KRW-BTT', 'KRW-MOC', 'KRW-TFUEL', 'KRW-MANA', 'KRW-ANKR', 'KRW-AERGO', 'KRW-ATOM', 'KRW-TT', 'KRW-CRE', 'KRW-MBL', 'KRW-WAXP', 'KRW-HBAR', 'KRW-MED', 'KRW-MLK', 'KRW-STPT', 'KRW-ORBS', 'KRW-VET', 'KRW-CHZ', 'KRW-STMX', 'KRW-DKA', 'KRW-HIVE', 'KRW-KAVA', 'KRW-AHT', 'KRW-LINK', 'KRW-XTZ', 'KRW-BORA', 'KRW-JST', 'KRW-CRO', 'KRW-TON', 'KRW-SXP', 'KRW-HUNT', 'KRW-PLA', 'KRW-DOT', 'KRW-MVL', 'KRW-STRAX', 'KRW-AQT', 'KRW-GLM', 'KRW-SSX', 'KRW-META', 'KRW-FCT2', 'KRW-CBK', 'KRW-SAND', 'KRW-HPO', 'KRW-DOGE', 'KRW-STRK', 'KRW-PUNDIX', 'KRW-FLOW', 'KRW-AXS', 'KRW-STX', 'KRW-XEC', 'KRW-SOL', 'KRW-MATIC', 'KRW-AAVE', 'KRW-1INCH', 'KRW-ALGO', 'KRW-NEAR', 'KRW-AVAX', 'KRW-T', 'KRW-CELO', 'KRW-GMT', 'KRW-APT', 'KRW-SHIB', 'KRW-MASK', 'KRW-ARB', 'KRW-EGLD', 'KRW-SUI', 'KRW-GRT', 'KRW-BLUR', 'KRW-IMX', 'KRW-SEI', 'KRW-MINA']

KRW_COIN_TICKERS_ALL_API = {}
KRW_COIN_TICKERS_TRADE_PRICE_API = {}
for i in KRW_TICKERS_VALUE:
    KRW_COIN_TICKERS_ALL_API[i] = 0
    KRW_COIN_TICKERS_TRADE_PRICE_API[i] = 0

async def receiveUpbitMessage():       
    global KRW_COIN_TICKERS_ALL_API
    global KRW_COIN_TICKERS_TRADE_PRICE_API

    try:
        # consume messages
        async for message in upbitConsumer:
            messageValueStr = json.loads(message.value.decode('utf-8'))
            KRW_COIN_TICKERS_ALL_API[messageValueStr['code']] = messageValueStr
            KRW_COIN_TICKERS_TRADE_PRICE_API[messageValueStr['code']] = messageValueStr['trade_price']
            # print(message.value['code'])
            # await manager.broadcast(json.dumps(KRW_COIN_TICKERS_ALL_API))
    except Exception as e:
        print(f'receive_upbit_message {e}')
    finally:
        # will leave consumer group; perform autocommit if enabled
        log.warning('receive_upbit_message Stopping upbitconsumer')
        await upbitConsumer.stop()

def loadKrwCoinTickersTradePriceApi():
    return KRW_COIN_TICKERS_TRADE_PRICE_API
def loadKrwCoinTickersAll():
    return KRW_COIN_TICKERS_ALL_API

async def initializeUpbit(BROKERS):
    # loop = asyncio.get_event_loop()
    global upbitConsumer
    KAFKA_TOPIC = 'upbit'
    upbitConsumer = AIOKafkaConsumer(KAFKA_TOPIC,
                                         bootstrap_servers=BROKERS)
    # get cluster layout and join group
    await upbitConsumer.start()

    partitions: Set[TopicPartition] = upbitConsumer.assignment()
    nr_partitions = len(partitions)
    if nr_partitions != 1:
        log.warning(f'Found {nr_partitions} partitions for topic {KAFKA_TOPIC}. Expecting '
                    f'only one, remaining partitions will be ignored!')
    for tp in partitions:

        # get the log_end_offset
        end_offset_dict = await upbitConsumer.end_offsets([tp])
        end_offset = end_offset_dict[tp]

        if end_offset == 0:
            log.warning(f'Topic ({KAFKA_TOPIC}) has no messages (log_end_offset: '
                        f'{end_offset}), skipping initialization ...')
            return

        log.debug(f'Found log_end_offset: {end_offset} seeking to {end_offset-1}')
        upbitConsumer.seek(tp, end_offset-1)
        msg = await upbitConsumer.getone()
        log.info(f'Initializing API with data from msg: {msg}')
        return
    return upbitConsumer
    