from faker import Faker
import sys
import numpy as np
import pymongo
import json
import random
import csv

try:
    connectionString = "mongodb+srv://sentimentalhoon:L1XIq4QEJRuBXEmb@cluster0.q3lazme.mongodb.net/?retryWrites=true&w=majority&authMechanism=SCRAM-SHA-1"

    myclient = pymongo.MongoClient(connectionString)
    mydb = myclient["sayproject"]
    mycol = mydb["202308"]

    fake = Faker("ko-KR")

    with open("한국건강증진개발원_보건소 모바일 헬스케어 운동_20220921.csv", newline="") as csvfile:
        with open("food.csv", newline="") as foodfile:
            exercise = list(
                csv.reader(
                    csvfile,
                    delimiter=",",
                    doublequote=True,
                    lineterminator="\r\n",
                    quotechar='"',
                    skipinitialspace=True,
                )
            )
            food = list(
                csv.reader(
                    foodfile,
                    delimiter=",",
                    doublequote=True,
                    lineterminator="\r\n",
                    quotechar='"',
                    skipinitialspace=True,
                )
            )

            for i in range(1):
                ranNum = random.randint(100000, 199999)

                # 이름
                name = fake.name()
                # 트레이너
                trainer = 1001

                mydict = {"_id": ranNum, "name": name, "trainer": trainer}
                breakfast = [
                    {"foodname": "개고기", "gram": 300, "calorie": 500},
                    {"foodname": "개고기", "gram": 300, "calorie": 500},
                    {"foodname": "개고기", "gram": 300, "calorie": 500},
                    {"foodname": "개고기", "gram": 300, "calorie": 500},
                ]
                lunch = [
                    {"foodname": "개고기", "gram": 300, "calorie": 500},
                    {"foodname": "개고기", "gram": 300, "calorie": 500},
                    {"foodname": "개고기", "gram": 300, "calorie": 500},
                    {"foodname": "개고기", "gram": 300, "calorie": 500},
                ]
                dinner = [
                    {"foodname": "개고기", "gram": 300, "calorie": 500},
                    {"foodname": "개고기", "gram": 300, "calorie": 500},
                    {"foodname": "개고기", "gram": 300, "calorie": 500},
                    {"foodname": "개고기", "gram": 300, "calorie": 500},
                ]
                nightmeal = [
                    {"foodname": "개고기", "gram": 300, "calorie": 500},
                    {"foodname": "개고기", "gram": 300, "calorie": 500},
                    {"foodname": "개고기", "gram": 300, "calorie": 500},
                    {"foodname": "개고기", "gram": 300, "calorie": 500},
                ]

                status = ["weight", "height"]

                all = []
                for j in range(1, 5):
                    
                    # 오늘 총 정보
                    myDailyAllInfo = {}
                    # 오늘 식단
                    mydiet = {}
                    # 오늘 운동
                    myexercise = {}
                    # 오늘 상태
                    myStatus = {}
                    # 오늘 총 먹은 칼로리 표기
                    mydiet["sum_calorie"] = random.randint(2000, 2500)
                    # 식단 정보 : 아침, 점심, 저녁, 야식
                    mydiet["breakfast"] = breakfast
                    mydiet["lunch"] = lunch
                    mydiet["dinner"] = dinner
                    mydiet["nightmeal"] = nightmeal
                    # 총정보에 식단 정보 입력
                    myDailyAllInfo["diet"] = mydiet                    
                    
                    myexercise = [
                        { "kind" : "달리기", "time_minute" : 10, "calorie" : 150 },
                                  { "kind" : "숨쉬기", "time_minute" : 10, "calorie" : 150 },
                                  { "kind" : "눕기", "time_minute" : 10, "calorie" : 150 },
                                  { "kind" : "일어나기", "time_minute" : 10, "calorie" : 150 }
                                  ]
                    # myexercise["sum_calorie"] = random.randint(100, 200)

                    myDailyAllInfo["exercise"] = myexercise
                    myStatus["wegith"] = 85
                    myStatus["height"] = 180
                    myDailyAllInfo["status"] = myStatus

                    myDailyAllInfo["dailyInfo"] = "202308" + format(j, "02")
                    all.append(myDailyAllInfo)
                    
                mydict["dailyInfo"] = all
                x = mycol.insert_one(mydict)

                print(x.inserted_id)
        # mylist.append(mydict)

    # print(mylist)
    # x = mycol.insert_many(mylist)
    # print(x.inserted_ids)
except Exception as e:
    print(f"Error {e}")
    sys.exit(1)
