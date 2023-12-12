from kafka import KafkaProducer
import time
import json
# from pykis import *
# from prettytable import PrettyTable
import os
import json
import requests
# import pandas as pd

try:
    import websocket

except ImportError:
    print("websocket-client 설치중입니다.")
    os.system('python3 -m pip3 install websocket-client')

import os
from dotenv import load_dotenv

load_dotenv()

BROKERS = ['59.3.28.12:9092', '59.3.28.12:9093', '59.3.28.12:9094']

KRW_TICKERS_VALUE = ['KRW-BTC', 'KRW-ETH', 'KRW-NEO', 'KRW-MTL', 'KRW-XRP', 'KRW-ETC', 'KRW-SNT', 'KRW-WAVES', 'KRW-XEM', 'KRW-QTUM', 'KRW-LSK', 'KRW-STEEM', 'KRW-XLM', 'KRW-ARDR', 'KRW-ARK', 'KRW-STORJ', 'KRW-GRS', 'KRW-ADA', 'KRW-SBD', 'KRW-POWR', 'KRW-BTG', 'KRW-ICX', 'KRW-EOS', 'KRW-TRX', 'KRW-SC', 'KRW-ONT', 'KRW-ZIL', 'KRW-POLYX', 'KRW-ZRX', 'KRW-LOOM', 'KRW-BCH', 'KRW-BAT', 'KRW-IOST', 'KRW-CVC', 'KRW-IQ', 'KRW-IOTA', 'KRW-HIFI', 'KRW-ONG', 'KRW-GAS', 'KRW-UPP', 'KRW-ELF', 'KRW-KNC', 'KRW-BSV', 'KRW-THETA', 'KRW-QKC', 'KRW-BTT', 'KRW-MOC', 'KRW-TFUEL', 'KRW-MANA', 'KRW-ANKR', 'KRW-AERGO', 'KRW-ATOM', 'KRW-TT', 'KRW-CRE', 'KRW-MBL', 'KRW-WAXP', 'KRW-HBAR',
                     'KRW-MED', 'KRW-MLK', 'KRW-STPT', 'KRW-ORBS', 'KRW-VET', 'KRW-CHZ', 'KRW-STMX', 'KRW-DKA', 'KRW-HIVE', 'KRW-KAVA', 'KRW-AHT', 'KRW-LINK', 'KRW-XTZ', 'KRW-BORA', 'KRW-JST', 'KRW-CRO', 'KRW-TON', 'KRW-SXP', 'KRW-HUNT', 'KRW-PLA', 'KRW-DOT', 'KRW-MVL', 'KRW-STRAX', 'KRW-AQT', 'KRW-GLM', 'KRW-SSX', 'KRW-META', 'KRW-FCT2', 'KRW-CBK', 'KRW-SAND', 'KRW-HPO', 'KRW-DOGE', 'KRW-STRK', 'KRW-PUNDIX', 'KRW-FLOW', 'KRW-AXS', 'KRW-STX', 'KRW-XEC', 'KRW-SOL', 'KRW-MATIC', 'KRW-AAVE', 'KRW-1INCH', 'KRW-ALGO', 'KRW-NEAR', 'KRW-AVAX', 'KRW-T', 'KRW-CELO', 'KRW-GMT', 'KRW-APT', 'KRW-SHIB', 'KRW-MASK', 'KRW-ARB', 'KRW-EGLD', 'KRW-SUI', 'KRW-GRT', 'KRW-BLUR', 'KRW-IMX', 'KRW-SEI', 'KRW-MINA']

STOCK_CODE = ["005930", "373220", "000660", "207940", "005935", "005380", "005490", "051910", "000270",
              "035420", "006400", "068270", "003670", "105560", "028260", "012330", "035720", "055550", "066570", "032830",]

I_STOCK = ["005930", "373220", "000660", "207940", "005935", "005380", "005490", "051910", "000270", "035420",
           "006400", "068270", "003670", "105560", "028260", "012330", "035720", "055550", "066570", "032830",]

I_APPKEY = os.getenv("I_APPKEY")
I_APPSECRET = os.getenv("I_APPSECRET")

producer = KafkaProducer(bootstrap_servers=BROKERS)

# 웹소켓 접속키 발급


def get_approval(key, secret):
    # url = https://openapivts.koreainvestment.com:29443' # 모의투자계좌
    url = 'https://openapi.koreainvestment.com:9443'  # 실전투자계좌
    headers = {"content-type": "application/json"}
    body = {"grant_type": "client_credentials",
            "appkey": key,
            "secretkey": secret}
    PATH = "oauth2/Approval"
    URL = f"{url}/{PATH}"
    res = requests.post(URL, headers=headers, data=json.dumps(body))
    approval_key = res.json()["approval_key"]
    return approval_key


i_approval_key = get_approval(I_APPKEY, I_APPSECRET)
print("approval_key [%s]" % (i_approval_key))

stockHeader = []
for stockNumber in I_STOCK:
    stockHeader.append(
        {
            "header": {"approval_key": i_approval_key, "custtype": "P", "tr_type": "1", "content-type": "utf-8"},
            "body": {"input": {"tr_id": "H0STCNT0",  # API명
                               "tr_key": stockNumber  # 종목번호
                               }
                     }
        }
    )
# Pandas DataFrame 이용

'''
result 값 예제
유가증권단축종목코드,주식체결시간,주식현재가,전일대비부호,전일대비,
'451760', '101312', '19920', '2', '1290', 
전일대비율,가중평균주식가격,주식시가,주식최고가,주식최저가,
'6.92', '19901.40', '20050', '20500', '19280',
매도호가1,매수호가1,체결거래량,누적거래량,누적거래대금,
'19920', '19910', '2', '3746668', '74563639420',
매도체결건수,매수체결건수,순매수 체결건수,체결강도,총 매도수량,
'23406', '28400', '4994', '84.08', '1964850', 
총 매수수량,체결구분 ,매수비율 ,전일 거래량대비등락율,시가시간 ,
'1652041', '1', '0.45', '44.33', '090015', 
시가대비 구분,시가대비,최고가 시간,고가대비구분,고가대비,
'5', '-130', '090213', '5', '-580', 
최저가시간,저가대비구분,저가대비 ,영업일자 ,신 장운영 구분코드,
'091103', '2', '640', '20231117', '20', 
거래정지 여부,매도호가잔량,매수호가잔량,총 매도호가잔량,총 매수호가잔량,
'N', '148', '187', '17529', '4549',
거래량 회전율,전일 동시간 누적거래량,전일 동시간 누적거래량 비율,시간구분코드,임의종료구분코드,
'26.05', '692648', '540.92', '0', '', 
정적VI발동기준가
'20050', 
'''


def pdbind(result):
    tx = {
        'COMPANY_NAME_KR': result[0],
        'MKSC_SHRN_ISCD': result[0],
        'STCK_CNTG_HOUR': result[1],
        'STCK_PRPR': result[2],
        'PRDY_VRSS_SIGN': result[3],
        'PRDY_VRSS': result[4],
        'PRDY_CTRT': result[5],
        'WGHN_AVRG_STCK_PRC': result[6],
        'STCK_OPRC': result[7],
        'STCK_HGPR': result[8],
        'STCK_LWPR': result[9],
        'ASKP1': result[10],
        'BIDP1': result[11],
        'CNTG_VOL': result[12],
        'ACML_VOL': result[13],
        'ACML_TR_PBMN': result[14],
        'SELN_CNTG_CSNU': result[15],
        'SHNU_CNTG_CSNU': result[16],
        'NTBY_CNTG_CSNU': result[17],
        'CTTR': result[18],
        'SELN_CNTG_SMTN': result[19],
        'SHNU_CNTG_SMTN': result[20],
        'CCLD_DVSN': result[21],
        'SHNU_RATE': result[22],
        'PRDY_VOL_VRSS_ACML_VOL_RATE': result[23],
        'OPRC_HOUR': result[24],
        'OPRC_VRSS_PRPR_SIGN': result[25],
        'OPRC_VRSS_PRPR': result[26],
        'HGPR_HOUR': result[27],
        'HGPR_VRSS_PRPR_SIGN': result[28],
        'HGPR_VRSS_PRPR': result[29],
        'LWPR_HOUR': result[30],
        'LWPR_VRSS_PRPR_SIGN': result[31],
        'LWPR_VRSS_PRPR': result[32],
        'BSOP_DATE': result[33],
        'NEW_MKOP_CLS_CODE': result[34],
        'TRHT_YN': result[35],
        'ASKP_RSQN1': result[36],
        'BIDP_RSQN1': result[37],
        'TOTAL_ASKP_RSQN': result[38],
        'TOTAL_BIDP_RSQN': result[39],
        'VOL_TNRT': result[40],
        'PRDY_SMNS_HOUR_ACML_VOL': result[41],
        'PRDY_SMNS_HOUR_ACML_VOL_RATE': result[42],
        'HOUR_CLS_CODE': result[43],
        'MRKT_TRTM_CLS_CODE': result[44],
        'VI_STND_PRC': result[45]
    }
    producer.send('korea_stock', json.dumps(tx).encode('utf-8'))


def on_message(ws, data):
    # print('type=', type(data), '\ndata=', data)

    if data[0] in ['0', '1']:  # 시세데이터가 아닌경우
        d1 = data.split("|")
        if len(d1) >= 4:
            isEncrypt = d1[0]
            tr_id = d1[1]
            tr_cnt = d1[2]
            recvData = d1[3]
            result = recvData.split("^")
            # print("start time=", result[1])
            pdbind(result)  # pandas dataframe 이용 변경
        else:
            print('Data Size Error=', len(d1))
    else:
        recv_dic = json.loads(data)
        tr_id = recv_dic['header']['tr_id']

        if tr_id == 'PINGPONG':
            send_ping = recv_dic
            ws.send(data, websocket.ABNF.OPCODE_PING)
        else:  # parser data
            print('tr_id=', tr_id, '\nmsg=', data)


def on_error(ws, error):
    print(f'error({time.time()})=', error)


def on_close(ws, status_code, close_msg):
    print('on_close close_status_code=', status_code, " close_msg=", close_msg)


def on_open(ws):
    for value in stockHeader:
        print('on_open send data=', json.dumps(value))
        ws.send(json.dumps(value), websocket.ABNF.OPCODE_TEXT)
        time.sleep(1)

# 모의투자
# ws = websocket.WebSocketApp("ws://ops.koreainvestment.com:31000",
#           on_open=on_open, on_message=on_message, on_error=on_error)


ws = websocket.WebSocketApp("ws://ops.koreainvestment.com:21000",
                            on_open=on_open, on_message=on_message, on_error=on_error)

ws.run_forever()
