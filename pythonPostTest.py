import requests
import json
data = {'inputText' : '장지웅은 바보인가 천재인가 그것이 문제인가? 답변을 달라'}

header = {'Content-Type' : 'application/json; charset=utf-8'}

res = requests.post('http://221.156.60.18:8010/summary', headers=header, data=json.dumps(data))

print(res.text)