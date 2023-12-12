import json
from kafka import KafkaProducer, KafkaConsumer

PAYMENT_TOPIC = 'payments'
COIN_TOPIC = 'coin_payments'
CARD_TOPIC = 'card_payments'

brokers = ['localhost:9092', 'localhost:9093', 'localhost:9094']
consumer = KafkaConsumer(PAYMENT_TOPIC, bootstrap_servers=brokers)
producer = KafkaProducer(bootstrap_servers=brokers)

def is_suspicious(tx):
    if tx['PAYMENT_TYPE'] == 'BITCOIN':
        return True
    return False

for message in consumer:
    msg = json.loads(message.value.decode('utf-8'))
    print(msg)
    print(is_suspicious(msg))

    topic = COIN_TOPIC if is_suspicious(msg) else CARD_TOPIC
    producer.send(topic, json.dumps(msg).encode('utf-8'))
