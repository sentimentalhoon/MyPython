'''코스닥주식종목코드(kosdaq_code.mst) 정제 파이썬 파일'''

import pandas as pd
import urllib.request
import ssl
import zipfile
import os
from sqlalchemy import create_engine

from dotenv import load_dotenv
import os

loadEvn = load_dotenv()

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')

MYSQL_HOST = os.environ.get('MYSQL_HOST')
MYSQL_PORT = os.environ.get('MYSQL_PORT')
MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE')

base_dir = os.getcwd()

def kosdaq_master_download(base_dir, verbose=False):

    cwd = os.getcwd()
    if (verbose): print(f"current directory is {cwd}")
    ssl._create_default_https_context = ssl._create_unverified_context
    
    urllib.request.urlretrieve("https://new.real.download.dws.co.kr/common/master/kosdaq_code.mst.zip",
                               base_dir + "\\kosdaq_code.zip")

    os.chdir(base_dir)
    if (verbose): print(f"change directory to {base_dir}")
    kosdaq_zip = zipfile.ZipFile('kosdaq_code.zip')
    kosdaq_zip.extractall()
    
    kosdaq_zip.close()

    if os.path.exists("kosdaq_code.zip"):
        os.remove("kosdaq_code.zip")

def get_kosdaq_master_dataframe(base_dir):
    file_name = base_dir + "\\kosdaq_code.mst"
    tmp_fil1 = base_dir + "\\kosdaq_code_part1.tmp"
    tmp_fil2 = base_dir + "\\kosdaq_code_part2.tmp"

    wf1 = open(tmp_fil1, mode="w")
    wf2 = open(tmp_fil2, mode="w")

    with open(file_name, mode="r", encoding="cp949") as f:
        for row in f:
            rf1 = row[0:len(row) - 222]
            rf1_1 = rf1[0:9].rstrip()
            rf1_2 = rf1[9:21].rstrip()
            rf1_3 = rf1[21:].strip()
            wf1.write(rf1_1 + ',' + rf1_2 + ',' + rf1_3 + '\n')
            rf2 = row[-222:]
            wf2.write(rf2)

    wf1.close()
    wf2.close()

    part1_columns = ['abbreviationCode', 'standardCode', 'koreanName']
    df1 = pd.read_csv(tmp_fil1, header=None, names=part1_columns, encoding='cp949')

    field_specs = [2, 1,
                   4, 4, 4, 1, 1,
                   1, 1, 1, 1, 1,
                   1, 1, 1, 1, 1,
                   1, 1, 1, 1, 1,
                   1, 1, 1, 1, 9,
                   5, 5, 1, 1, 1,
                   2, 1, 1, 1, 2,
                   2, 2, 3, 1, 3,
                   12, 12, 8, 15, 21,
                   2, 7, 1, 1, 1,
                   1, 9, 9, 9, 5,
                   9, 8, 9, 3, 1,
                   1, 1
                   ]

    # part2_columns = ['증권그룹구분코드','시가총액 규모 구분 코드 유가',
    #                  '지수업종 대분류 코드','지수 업종 중분류 코드','지수업종 소분류 코드','벤처기업 여부',
    #                  '저유동성종목 여부','KRX 종목 여부','ETP 상품구분코드','KRX100 종목 여부',
    #                  'KRX 자동차 여부','KRX 반도체 여부','KRX 바이오 여부','KRX 은행 여부','기업인수목적회사여부',
    #                  'KRX 에너지 화학 여부','KRX 철강 여부','단기과열종목구분코드','KRX 미디어 통신 여부',
    #                  'KRX 건설 여부','(코스닥)투자주의환기종목여부','KRX 증권 구분','KRX 선박 구분',
    #                  'KRX섹터지수 보험여부','KRX섹터지수 운송여부','KOSDAQ150지수여부 (Y,N)','주식 기준가',
    #                  '정규 시장 매매 수량 단위','시간외 시장 매매 수량 단위','거래정지 여부','정리매매 여부',
    #                  '관리 종목 여부','시장 경고 구분 코드','시장 경고위험 예고 여부','불성실 공시 여부',
    #                  '우회 상장 여부','락구분 코드','액면가 변경 구분 코드','증자 구분 코드','증거금 비율',
    #                  '신용주문 가능 여부','신용기간','전일 거래량','주식 액면가','주식 상장 일자','상장 주수(천)',
    #                  '자본금','결산 월','공모 가격','우선주 구분 코드','공매도과열종목여부','이상급등종목여부',
    #                  'KRX300 종목 여부','매출액','영업이익','경상이익','단기순이익','ROE(자기자본이익률)',
    #                  '기준년월','전일기준 시가총액 (억)','그룹사 코드','회사신용한도초과여부','담보대출가능여부','대주가능여부'
    #                  ]
    part2_columns = [
        'SecurityGroupCode', 'MarketCapSizeCodeListed', 'IndexIndustryMajorCode', 'IndexIndustryMediumCode', 'IndexIndustryMinorCode', 'VentureCompanyYN', 'LowLiquidityStockYN', 'KRXStockYN', 'ETPProductCode', 'KRX100StockYN', 'KRXAutomobileYN', 'KRXSemiconductorYN', 'KRXBioYN', 'KRXBankYN', 'CompanyTakeoverPurposeYN', 'KRXEnergyChemicalYN', 'KRXSteelYN', 'ShortTermOverheatedStockCode', 'KRXMediaCommunicationYN', 'KRXConstructionYN', 'KOSDAQInvestmentWarningRevocationYN', 'KRXSecuritiesDivision', 'KRXShipDivision', 'KRXSectorIndexInsuranceYN', 'KRXSectorIndexTransportationYN', 'KOSDAQ150IndexYN', 'StockBasePrice', 'RegularMarketTradingUnit', 'AfterHoursMarketTradingUnit', 'TradingSuspensionYN', 'CleanupTradingYN', 'ManagementStockYN', 'MarketWarningCode', 'MarketWarningRiskNoticeYN', 'InsincereDisclosureYN', 'CircumventionListingYN', 'LockCode', 'FaceValueChangeCode', 'CapitalIncreaseCode', 'MarginRate', 'CreditOrderPossibleYN', 'CreditPeriod', 'PrevDayTradingVolume', 'StockFaceValue', 'StockListingDate', 'ListedSharesThousand', 'Capital', 'SettlementMonth', 'PublicOfferingPrice', 'PreferredStockCode', 'ShortSellingOverheatedStockYN', 'AbnormalRiseStockYN', 'KRX300StockYN', 'Sales', 'OperatingProfit', 'CurrentProfit', 'ShortTermNetProfit', 'ROE', 'BaseYearMonth', 'PrevDayBaseMarketCapBillion', 'GroupCompanyCode', 'CompanyCreditLimitExceededYN', 'CollateralLoanPossibleYN', 'MajorShareholderPossibleYN'
                     ]
    df2 = pd.read_fwf(tmp_fil2, widths=field_specs, names=part2_columns)

    df = pd.merge(df1, df2, how='outer', left_index=True, right_index=True)

    # clean temporary file and dataframe
    del (df1)
    del (df2)
    os.remove(file_name)
    os.remove(tmp_fil1)
    os.remove(tmp_fil2)

    print("get_kosdaq_master_dataframe Done")

    return df

def saveMysql(df):
    from urllib.parse import quote

    SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{MYSQL_USER}:{quote(MYSQL_PASSWORD)}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8'

    engine = create_engine(url=SQLALCHEMY_DATABASE_URL)

    conn = engine.connect()
    try:
        df.to_sql(name='kosdaqCode', con=engine, if_exists='replace',index=False)
        print('save KosDaq Mysql Complete')
    except Exception as e:
        print(f' save Mysql except => {e}')
    finally:
        conn.close()

def saveRedis(df):
    import redis
    redisClient  = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=0)
    try:
        # Set
        redisClient.set(name='kosdaqCode', value=df.to_json())
        print('save Kosdaq Redis Complete')
    except Exception as e:
        print(f' saveRedis except => {e}')
    finally:
        redisClient.close()

kosdaq_master_download(base_dir)
df = get_kosdaq_master_dataframe(base_dir)
saveMysql(df)
saveRedis(df)