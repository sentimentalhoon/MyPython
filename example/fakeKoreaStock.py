
import pymysql
import sys
from kafka import KafkaProducer, KafkaConsumer
import json
import pymysql
from kafka.structs import TopicPartition
import time

# kospi_stock = kospi_stock_number()
kospi_stock = "'005930', '373220', '000660', '207940', '005935','005490', '005380', '051910', '035420', '000270', '006400', '068270', '003670', '035720', '105560','028260', '012330', '055550', '066570', '096770', '032830', '003550', '323410', '033780', '086790', '000810', '034730', '015760', '138040', '017670', '018260', '011200', '329180', '010130', '009150', '047050', '259960', '316140', '034020', '024110'"
               
# kosdaq_stock = kosdaq_stock_number()
kosdaq_stock = "'247540', '086520', '091990', '022100', '066970', '028300', '196170', '068760', '035900', '277810', '403870', '058470', '263750', '214150', '293490', '357780', '041510', '039030', '145020', '005290', '095340', '112040', '240810', '036930', '253450', '035760', '000250', '086900', '121600', '214370', '067310', '393890', '025900', '034230', '237690', '078600', '048410', '141080', '365340', '195940'"

try:
    conn = pymysql.connect(
        user="sam9mo",
        passwd="sam9mo!!",
        host="59.3.28.12",
        port=3306,
        db="sam9mo",
    )
    try:
        global stockNoAndName

        with conn.cursor() as cur:
            query = f"select abbreviation_code, korean_name from kospi_code where abbreviation_code in ({kospi_stock})"
            cur.execute(query)

            stockNoAndName = []

            for abbreviation_code, korean_name in cur:
                stockNoAndName.append(
                    { "MKSC_SHRN_ISCD" : abbreviation_code, "korean_name" : korean_name }
                )

            query = f"select abbreviation_code, korean_name from kosdaq_code where abbreviation_code in ({kosdaq_stock})"
            cur.execute(query)

            for abbreviation_code, korean_name in cur:
                stockNoAndName.append(
                    { "MKSC_SHRN_ISCD" : abbreviation_code, "korean_name" : korean_name }   
                )
            
        # while(True):
        #     data = {}
        #     pdbind("삼성전자", data)

    except pymysql.Error as e:
        print(f"Error {e}")
        sys.exit(1)
    finally:
        conn.close()
except pymysql.Error as e:
    print(f"Error {e}")
    sys.exit(1)


def consume_messages():
    # Create a Consumer instance

    CARD_TOPIC = 'stock_api'

    brokers = ['59.3.28.12:9092', '59.3.28.12:9093', '59.3.28.12:9094']
    consumer = KafkaConsumer(CARD_TOPIC, bootstrap_servers=brokers, auto_offset_reset='earliest')
    producer = KafkaProducer(bootstrap_servers=brokers)
    partitions = consumer.partitions_for_topic(CARD_TOPIC)
    for p in partitions:
        topic_partition = TopicPartition(CARD_TOPIC, p)
        # Seek offset 0
        consumer.seek(partition=topic_partition, offset=0)
        for msg in consumer:
            tx = json.loads(msg.value.decode("utf-8"))
            for value in stockNoAndName:
                if value['MKSC_SHRN_ISCD'] == tx['MKSC_SHRN_ISCD']:
                    tx['COMPANY_NAME_KR'] = value['korean_name']
                    break    
            producer.send('korea_stock', json.dumps(tx).encode('utf-8'))    
            time.sleep(0.1)

# Call the function with your values
consume_messages()