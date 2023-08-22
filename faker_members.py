from faker import Faker
import sys
import numpy as np
import pymysql
try:
    conn = pymysql.connect(
        user="root", passwd="Tkfkdgo12#$", host="localhost", port=3306, db="miniproject"
    )

    fake = Faker("ko-KR")
    
    cur = conn.cursor()

    for i in range(100000):
        # 이름
        name = fake.name()
        # 나이 (random 사용)
        age = fake.pyint(min_value=20, max_value=70)
        # 성별
        gender = np.random.choice(["M", "F"], p=[0.5, 0.5])
        # 사진
        photo_path = fake.image_url()
        # 키 (random 사용)
        height = fake.pyint(min_value=150, max_value=200)
        # 몸무게 (random 사용)
        weight = fake.pyint(min_value=40, max_value=120)
        # 트레이너
        trainer = 1001
        # 등록일
        regist_day = fake.date_this_year()
        # 주소
        address = fake.address()
        # 직업
        job = fake.job()
        # 연락처
        phone_number = fake.phone_number()
        # 이메일
        email = fake.email()
        # 신용카드 정보
        credit_card = fake.credit_card_full()
        insert_query = f"INSERT INTO miniproject.members(name, age, gender, height, weight, trainer, photopath, job, address, regist_day, phone_number, email, credit_card) VALUES('{name}', {age}, '{gender}', {height}, {weight},{trainer}, '{photo_path}', '{job}', '{address}', '{regist_day}', '{phone_number}', '{email}', '{credit_card}')"
        
        cur.execute(insert_query)
        
       
    conn.commit()   
    conn.close()
    
except pymysql.Error as e:
    print(f"Error {e}")
    sys.exit(1)


