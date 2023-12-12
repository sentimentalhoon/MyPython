from faker import Faker
import sys
import numpy as np
import pymysql
from datetime import datetime, time
import uuid

try:
    conn = pymysql.connect(
        user="sam9mo",
        passwd="sam9mo!!",
        host="59.3.28.12",
        port=3306,
        db="sam9mo",
    )

    fake = Faker("ko-KR")
    try:
        cur = conn.cursor()

        for i in range(10):
            # 이름
            name = fake.name()
            # 나이 (random 사용)
            age = fake.pyint(min_value=20, max_value=70)
            password = fake.name()
            # 직업
            job = fake.job()
            # 이메일
            email = fake.email()
                        # UUID 생성
            my_uuid = uuid.uuid4()

            # UUID를 16바이트 바이너리로 변환
            my_uuid_bytes = my_uuid.bytes
            print(my_uuid_bytes)
            insert_query = f"INSERT INTO sam9mo.member(id, account, age, name, password) VALUES('{my_uuid_bytes}', '{email}', {age}, '{name}', '{password}')"
            print(insert_query)
            cur.execute(insert_query)

            time.sleep(0.5)
    finally:
        conn.commit()
        conn.close()

except pymysql.Error as e:
    print(f"Error {e}")
    sys.exit(1)
