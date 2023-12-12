
import pymysql
import sys
from kafka import KafkaProducer, KafkaConsumer
import json
import pymysql
from kafka.structs import TopicPartition
import time
# BROKERS = ['59.3.28.12:9092', '59.3.28.12:9093', '59.3.28.12:9094']

# producer = KafkaProducer(bootstrap_servers=BROKERS)

# def pdbind(company, result):
#     tx = {
#         'COMPANY_NAME_KR': company,
#         'MKSC_SHRN_ISCD': result[0],
#         'STCK_CNTG_HOUR': result[1],
#         'STCK_PRPR': result[2],
#         'PRDY_VRSS_SIGN': result[3],
#         'PRDY_VRSS': result[4],
#         'PRDY_CTRT': result[5],
#         'WGHN_AVRG_STCK_PRC': result[6],
#         'STCK_OPRC': result[7],
#         'STCK_HGPR': result[8],
#         'STCK_LWPR': result[9],
#         'ASKP1': result[10],
#         'BIDP1': result[11],
#         'CNTG_VOL': result[12],
#         'ACML_VOL': result[13],
#         'ACML_TR_PBMN': result[14],
#         'SELN_CNTG_CSNU': result[15],
#         'SHNU_CNTG_CSNU': result[16],
#         'NTBY_CNTG_CSNU': result[17],
#         'CTTR': result[18],
#         'SELN_CNTG_SMTN': result[19],
#         'SHNU_CNTG_SMTN': result[20],
#         'CCLD_DVSN': result[21],
#         'SHNU_RATE': result[22],
#         'PRDY_VOL_VRSS_ACML_VOL_RATE': result[23],
#         'OPRC_HOUR': result[24],
#         'OPRC_VRSS_PRPR_SIGN': result[25],
#         'OPRC_VRSS_PRPR': result[26],
#         'HGPR_HOUR': result[27],
#         'HGPR_VRSS_PRPR_SIGN': result[28],
#         'HGPR_VRSS_PRPR': result[29],
#         'LWPR_HOUR': result[30],
#         'LWPR_VRSS_PRPR_SIGN': result[31],
#         'LWPR_VRSS_PRPR': result[32],
#         'BSOP_DATE': result[33],
#         'NEW_MKOP_CLS_CODE': result[34],
#         'TRHT_YN': result[35],
#         'ASKP_RSQN1': result[36],
#         'BIDP_RSQN1': result[37],
#         'TOTAL_ASKP_RSQN': result[38],
#         'TOTAL_BIDP_RSQN': result[39],
#         'VOL_TNRT': result[40],
#         'PRDY_SMNS_HOUR_ACML_VOL': result[41],
#         'PRDY_SMNS_HOUR_ACML_VOL_RATE': result[42],
#         'HOUR_CLS_CODE': result[43],
#         'MRKT_TRTM_CLS_CODE': result[44],
#         'VI_STND_PRC': result[45]
#     }
#     producer.send('korea_stock', json.dumps(tx).encode('utf-8'))

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
            query = f"select abbreviation_code, korean_name from kospi_code"
            cur.execute(query)
            
            stockNoAndName = []

            for abbreviationCode, koreanName in cur:
                stockNoAndName.append(
                    { "MKSC_SHRN_ISCD" : abbreviationCode, "korean_name" : koreanName }
                )

            query = f"select abbreviation_code, korean_name from kosdaq_code"
            cur.execute(query)

            for abbreviationCode, koreanName in cur:
                stockNoAndName.append(
                    { "MKSC_SHRN_ISCD" : abbreviationCode, "korean_name" : koreanName }   
                )            
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
    print('==========================================================')
    print('[stock_api] Fake DATA Start!')
    print('==========================================================')
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
            
            if str.find(str(tx), 'PING') > 0:
                continue

            producer.send('stock_api', json.dumps(tx).encode('utf-8'))    
            time.sleep(0.1)

# Call the function with your values
consume_messages()