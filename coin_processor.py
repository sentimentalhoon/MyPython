from kafka import KafkaProducer, KafkaConsumer
import json
import pymysql

COIN_TOPIC = 'coin_payments'

brokers = ['localhost:9092', 'localhost:9093', 'localhost:9094']
consumer = KafkaConsumer(COIN_TOPIC, bootstrap_servers=brokers)


conn = pymysql.connect(host='localhost',
                        user='root',
                        password='password12#$',
                        db='myDb',
                        charset='utf8')
with conn:
    with conn.cursor() as cur:
        for message in consumer:
            msg = json.loads(message.value.decode())

            to = msg['TO']
            amt = msg['AMT']
            date = msg['DATE']
            time = msg['TIME']
            payment_type = msg['PAYMENT_TYPE']

            sql = f"INSERT INTO payment (target, amt, regdate, regtime, payment_type) VALUES ('{to}', '{amt}', '{date}', '{time}', '{payment_type}')"

            cur.execute(sql)
            conn.commit()