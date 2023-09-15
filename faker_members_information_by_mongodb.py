from faker import Faker
import sys
import numpy as np
import pymongo
import json
import random
import csv
import pymysql
import datetime

data = ""
try:
    conn = pymysql.connect(
        user="say",
        passwd="qwer12#$",
        host="svc.sel5.cloudtype.app",
        port=31538,
        db="sayproject",
    )
    요일 = ["월", "화", "수", "목", "금", "토", "일"]
    with conn.cursor() as cur:
        query = "select no, name, weight, height, trainer from members"

        cur.execute(query)

        for no, name, weight, height, trainer in cur:
            print(no, name, weight, height, trainer)
            try:
                connectionString = "mongodb+srv://sentimentalhoon:L1XIq4QEJRuBXEmb@cluster0.q3lazme.mongodb.net/?retryWrites=true&w=majority&authMechanism=SCRAM-SHA-1"
                year = "2023"
                month = "09"
                dbName = year + month
                myclient = pymongo.MongoClient(connectionString)
                mydb = myclient["sayproject"]
                mycol = mydb[dbName]

                fake = Faker("ko-KR")

                with open(
                    "EXERCISE_INFO_202309151724.csv", newline="", encoding="EUC-KR"
                ) as excerciseFile:
                    with open(
                        "food_nutrients_202309151724.csv", newline="", encoding="EUC-KR"
                    ) as foodfile:
                        exercise = list(
                            csv.reader(
                                excerciseFile,
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
                        breakfast = []

                        lunch = []

                        dinner = []

                        otherfood = []

                        for i in range(5):
                            ranNum = random.randint(1, len(food) - 1)
                            breakfast.append(
                                {
                                    "code": food[ranNum][2],
                                    "foodname": food[ranNum][3],
                                    "gram": food[ranNum][7],
                                    "calorie": food[ranNum][11],
                                }
                            )
                            ranNum = random.randint(1, len(food) - 1)
                            lunch.append(
                                {
                                    "code": food[ranNum][2],
                                    "foodname": food[ranNum][3],
                                    "gram": food[ranNum][7],
                                    "calorie": food[ranNum][11],
                                }
                            )
                            ranNum = random.randint(1, len(food) - 1)
                            dinner.append(
                                {
                                    "code": food[ranNum][2],
                                    "foodname": food[ranNum][3],
                                    "gram": food[ranNum][7],
                                    "calorie": food[ranNum][11],
                                }
                            )
                            ranNum = random.randint(1, len(food) - 1)
                            otherfood.append(
                                {
                                    "code": food[ranNum][2],
                                    "foodname": food[ranNum][3],
                                    "gram": food[ranNum][7],
                                    "calorie": food[ranNum][11],
                                }
                            )

                        status = ["weight", "height"]

                        all = []

                        defalutWeight = weight
                        for j in range(1, 32):
                            nowWeight = weight
                            if datetime.datetime.today().day < j:
                                break
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

                            ranN = random.randint(0, 100) * 0.0001
                            print(
                                "!!-------",
                                ranN,
                                (nowWeight * ranN),
                                weight,
                                defalutWeight,
                            )

                            if random.randint(0, 2) % 2 == 0:
                                weight = defalutWeight - (nowWeight * ranN)
                                print("plus", nowWeight)
                            else:
                                weight = defalutWeight + (nowWeight * ranN)
                                print("minus", nowWeight)

                            print(
                                "!!-------",
                                ranN,
                                (nowWeight * ranN),
                                weight,
                                defalutWeight,
                            )
                            myexercise = []
                            for i in range(4):
                                ranNum = random.randint(1, len(exercise) - 1)
                                met = exercise[ranNum][2]
                                timeMinute = random.randint(10, 120)

                                몫 = 0
                                남은시간 = 0

                                if timeMinute >= 60:
                                    몫 = int(timeMinute / 60)
                                    남은시간 = (timeMinute - (60 * 몫)) / 60
                                else:
                                    남은시간 = timeMinute / 60

                                cal = float(float(met) * int(weight) * float(남은시간 + 몫))
                                myexercise.append(
                                    {
                                        "exerciseid": exercise[ranNum][0],
                                        "kind": exercise[ranNum][1],
                                        "met": met,
                                        "time_minute": timeMinute,
                                        "calorie": cal,
                                    }
                                )

                            # myexercise["sum_calorie"] = random.randint(100, 200)

                            myDailyAllInfo["exercise"] = myexercise

                            myStatus["weight"] = weight
                            myStatus["height"] = height
                            myDailyAllInfo["status"] = myStatus

                            myDailyAllInfo["day"] = dbName + format(j, "02")

                            day1 = datetime.date(
                                int(year), int(month), int(format(j, "02"))
                            )
                            myDailyAllInfo["dayOfTheWeek"] = 요일[day1.weekday()]
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
