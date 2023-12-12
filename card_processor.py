import requests
from pydantic import BaseModel
from fastapi import FastAPI, Request
import uvicorn

response = requests.get('http://121.179.83.68:8881/stock_api')

status_code = response.status_code

responseJson = None

if (status_code >= 300):
    print(f'status_code => {status_code}')
else:
    import json
    responseJson = response.json()
    print(f'status_code => {status_code}')

app = FastAPI()

class Item(BaseModel):
    company: str
    initial: list
    current_trade: list

def makeData(company: str, initial: list, current_trade: list):
    stockData = {}
    stockData[company] = {}
    try:
        responseJsonCompanyInfo = responseJson[company]
        responseInitial = responseJsonCompanyInfo['initial']
        responseCurrentTrade = responseJsonCompanyInfo['current_trade']

        initialData = {}
        if (len(responseInitial) > 0):
            for key, value in responseInitial.items():
                if key in initial:                                      
                    initialData.update({key : value }) 

        stockData[company]['initial'] = initialData

        currentTradeData = {}
        if (len(responseCurrentTrade) > 0):
            for key, value in responseCurrentTrade.items():
                if key in current_trade:     
                    currentTradeData.update({key : value })

        stockData[company]['current_trade'] = currentTradeData
    except Exception as e:
        stockData = { "status" : "error" }
        print(f'::::::: makeData Error => {e}')        
    finally:
        return stockData

@app.post('/')
def example(item: Item):
    if responseJson is not None:
        company = item.company
        initial = item.initial
        current_trade = item.current_trade
        returnData = {}
        if company != '0':
            if company in responseJson:
                returnData.update(makeData(company, initial, current_trade))  
            else:
                returnData = { "status" : "company is not found"}
        else:            
            for companyCode in responseJson:
                returnData.update(makeData(companyCode, initial, current_trade))
                
        return returnData
    else:
        return { "status" : "none" }  

if __name__ == "__main__":
    # TODO 로컬 배포
    #uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
    # TODO 실서버 배포
    uvicorn.run(app, host="0.0.0.0", port=9100)