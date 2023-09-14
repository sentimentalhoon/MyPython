from faker import Faker
import sys
import numpy as np
import pymongo
import json
import random
import csv
import pymysql

data = ""
try:
    conn = pymysql.connect(
        user="say",
        passwd="qwer12#$",
        host="svc.sel5.cloudtype.app",
        port=31538,
        db="sayproject",
    )
    with conn.cursor() as cur:
        query = "select no, name, weight, height, trainer from members"

        cur.execute(query)

        for no, name, weight, height, trainer in cur:
            print(no, name, weight, height, trainer)
            try:
                connectionString = "mongodb+srv://sentimentalhoon:L1XIq4QEJRuBXEmb@cluster0.q3lazme.mongodb.net/?retryWrites=true&w=majority&authMechanism=SCRAM-SHA-1"

                myclient = pymongo.MongoClient(connectionString)
                mydb = myclient["sayproject"]
                mycol = mydb["202309"]

                fake = Faker("ko-KR")

                with open(
                    "한국건강증진개발원_보건소 모바일 헬스케어 운동_20220921.csv", newline=""
                ) as csvfile:
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

                        ranNum = no

                        # 이름
                        name = name
                        # 트레이너
                        trainerNo = trainer

                        mydict = {"_id": ranNum, "name": name, "trainer": trainerNo}
                        breakfast = [
                            {
                                "code": "D000006",
                                "foodname": "꿩불고기",
                                "gram": 300,
                                "calorie": 500,
                            },
                            {
                                "code": "D000016",
                                "foodname": "불고기",
                                "gram": 300,
                                "calorie": 500,
                            },
                            {
                                "code": "D010234",
                                "foodname": "갈릭버터쉬림프(치즈크러스트)L",
                                "gram": 300,
                                "calorie": 500,
                            },
                            {
                                "code": "D010293",
                                "foodname": "돼지고기",
                                "gram": 300,
                                "calorie": 500,
                            },
                        ]
                        lunch = [
                            {
                                "code": "D010307",
                                "foodname": "꿩불고기",
                                "gram": 300,
                                "calorie": 500,
                            },
                            {
                                "code": "D010313",
                                "foodname": "불고기",
                                "gram": 300,
                                "calorie": 500,
                            },
                            {
                                "code": "D010361",
                                "foodname": "갈릭버터쉬림프(치즈크러스트)L",
                                "gram": 300,
                                "calorie": 500,
                            },
                            {
                                "code": "D010390",
                                "foodname": "돼지고기",
                                "gram": 300,
                                "calorie": 500,
                            },
                        ]
                        dinner = [
                            {
                                "code": "D010430",
                                "foodname": "꿩불고기",
                                "gram": 300,
                                "calorie": 500,
                            },
                            {
                                "code": "D010443",
                                "foodname": "불고기",
                                "gram": 300,
                                "calorie": 500,
                            },
                            {
                                "code": "D010433",
                                "foodname": "갈릭버터쉬림프(치즈크러스트)L",
                                "gram": 300,
                                "calorie": 500,
                            },
                            {
                                "code": "D010486",
                                "foodname": "돼지고기",
                                "gram": 300,
                                "calorie": 500,
                            },
                        ]
                        otherfood = [
                            {
                                "code": "D010529",
                                "foodname": "꿩불고기",
                                "gram": 300,
                                "calorie": 500,
                            },
                            {
                                "code": "D010539",
                                "foodname": "불고기",
                                "gram": 300,
                                "calorie": 500,
                            },
                            {
                                "code": "D010562",
                                "foodname": "갈릭버터쉬림프(치즈크러스트)L",
                                "gram": 300,
                                "calorie": 500,
                            },
                            {
                                "code": "D010582",
                                "foodname": "돼지고기",
                                "gram": 300,
                                "calorie": 500,
                            },
                        ]

                        status = ["weight", "height"]

                        all = []
                        for j in range(1, 32):
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
                            mydiet["otherfood"] = otherfood
                            # 총정보에 식단 정보 입력
                            myDailyAllInfo["diet"] = mydiet

                            myexercise = [
                                {
                                    "exerciseid": 1237,
                                    "kind": "사이드 밴드",
                                    "time_minute": 10,
                                    "calorie": 150,
                                },
                                {
                                    "exerciseid": 1240,
                                    "kind": "(윈드)서핑",
                                    "time_minute": 10,
                                    "calorie": 150,
                                },
                                {
                                    "exerciseid": 1264,
                                    "kind": "레그 컬",
                                    "time_minute": 10,
                                    "calorie": 150,
                                },
                                {
                                    "exerciseid": 1265,
                                    "kind": "루마니안 데드리프트",
                                    "time_minute": 10,
                                    "calorie": 150,
                                },
                            ]
                            # myexercise["sum_calorie"] = random.randint(100, 200)

                            myDailyAllInfo["exercise"] = myexercise
                            myStatus["weight"] = weight
                            myStatus["height"] = height
                            myDailyAllInfo["status"] = myStatus

                            myDailyAllInfo["day"] = "202308" + format(j, "02")
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

        conn.commit()
        conn.close()
except pymysql.Error as e:
    print(f"Error {e}")
    sys.exit(1)
