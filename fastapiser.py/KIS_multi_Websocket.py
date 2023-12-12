from kafka import KafkaProducer
import time
import json
# from pykis import *
# from prettytable import PrettyTable
import os
import json
import requests
# import pandas as pd
import pandas as pd
import websocket

BROKERS = ['59.3.28.12:9092', '59.3.28.12:9093', '59.3.28.12:9094']

STOCK_CODE_LIST = {
    '005930': '삼성전자',    '373220': 'LG에너지솔루션',    '000660': 'SK하이닉스',    '207940': '삼성바이오로직스',    '005935': '삼성전자우',
    '005490': 'POSCO홀딩스',    '005380': '현대차',    '051910': 'LG화학',    '035420': 'NAVER',    '000270': '기아',
    '006400': '삼성SDI',    '068270': '셀트리온',    '003670': '포스코퓨처엠',    '035720': '카카오',    '105560': 'KB금융',
    '028260': '삼성물산',    '012330': '현대모비스',    '055550': '신한지주',    '066570': 'LG전자',    '096770': 'SK이노베이션',
    '032830': '삼성생명',    '003550': 'LG',    '323410': '카카오뱅크',    '033780': 'KT&G',    '086790': '하나금융지주',
    '000810': '삼성화재',    '034730': 'SK',    '015760': '한국전력',    '138040': '메리츠금융지주',    '017670': 'SK텔레콤',
    '018260': '삼성에스디에스',    '011200': 'HMM',    '329180': 'HD현대중공업',    '010130': '고려아연',    '009150': '삼성전기',
    '047050': '포스코인터내셔널',    '259960': '크래프톤',    '316140': '우리금융지주',    '034020': '두산에너빌리티',    '024110': '기업은행',    
    
    # '247540': '에코프로비엠',    '086520': '에코프로',    '091990': '셀트리온헬스케어',    '022100': '포스코DX',    '066970': '엘앤에프',
    # '028300': 'HLB',    '196170': '알테오젠',    '068760': '셀트리온제약',    '035900': 'JYP Ent.',    '277810': '레인보우로보틱스',    '403870': 'HPSP',
    # '058470': '리노공업',    '263750': '펄어비스',    '214150': '클래시스',    '293490': '카카오게임즈',    '357780': '솔브레인',    '041510': '에스엠',
    # '039030': '이오테크닉스',    '145020': '휴젤',    '005290': '동진쎄미켐',    '095340': 'ISC',    '112040': '위메이드',
    # '240810': '원익IPS',    '036930': '주성엔지니어링',    '253450': '스튜디오드래곤',    '035760': 'CJ ENM',    '000250': '삼천당제약',
    # '086900': '메디톡스',    '121600': '나노신소재',    '214370': '케어젠',    '067310': '하나마이크론',    '393890': '더블유씨피',
    # '025900': '동화기업',    '034230': '파라다이스',    '237690': '에스티팜',    '078600': '대주전자재료',    '048410': '현대바이오',
    # '141080': '레고켐바이오',    '365340': '성일하이텍',    '195940': 'HK이노엔'
}

# 홍지수의 KIS AppKey, SecretKey
I_APPKEY = "PSOSKutnofaOWCauDnvn2OAsTrEahXIgCRZU"
I_APPSECRET = "8sZiuecLLHigC0MqiXR8xfJm8WLSZ56r2qfU8pDEIcAqf+Dy+PzkCmZbjXKNe1ZHch2H/rCK8WyKKnBiogJSh1TrRYlpJ1KEv6VMx9juCIUX4ioAqkuBV7yR4I99FDjwB5Ct1Hi3MyxnXkXvcnEag22x2V9dqHYmuWanxn8lYS72ljAxpCM="

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
for stockNumber in STOCK_CODE_LIST.keys():
    stockHeader.append(
        {
            "header": {
                "approval_key": i_approval_key,
                "custtype": "P",
                "tr_type": "1",
                "content-type": "utf-8"
            },
            "body": {
                "input": {
                    "tr_id": "H0STASP0",  # API명
                    "tr_key": stockNumber  # 종목번호
                }
            }
        }
    )
# Pandas DataFrame 이용

def pdbind(result):
    producer.send('korea_stock_hoka', json.dumps(result).encode('utf-8'))

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
            # xlsvalue(result)

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

ws = websocket.WebSocketApp("ws://ops.koreainvestment.com:21000",
                            on_open=on_open, on_message=on_message, on_error=on_error)

ws.run_forever()