from faker import Faker
import requests
import time

fake = Faker("ko-KR")

for i in range(999):
    # 이름
    name = fake.name()
    # 나이 (random 사용)
    age = fake.pyint(min_value=20, max_value=70)
    password = fake.name()
    # 직업
    job = fake.job()
    # 이메일
    email = fake.email() + str(i)

    address = fake.address()

    ip = fake.ipv4_private()

    phone_number = fake.phone_number()

    user_agent = fake.user_agent()

    jsonData ={
                      "account": email,
                      "password": "admin",
                      "age": age,
                      "name": name,
                      "job" : job,
                      "address" : address,
                      "ip" : ip,
                      "phoneNumber" : phone_number,
                      "userAgent" : user_agent
                  }
    
    print(jsonData)
    returnData = requests.post(url="http://127.0.0.1:8989/sign-up",
                  json= jsonData,
                  headers={"Content-Type": "application/json; charset=utf-8"})
    print(returnData.status_code)
    time.sleep(0.01)