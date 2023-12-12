from faker import Faker
import sys
import pymysql

try:
    conn = pymysql.connect(
        user="com",
        passwd="com01",
        host="localhost",
        port=3306,
        db="com",
    )

    fake = Faker("ko-KR")

    cur = conn.cursor()

    for i in range(20):
        insert_query = f"INSERT INTO com.tbl_board(title, writer, content) VALUES('{fake.sentence()}', '{fake.name()}', '{fake.text(4000)}')"

        cur.execute(insert_query)

    conn.commit()
    conn.close()


except pymysql.Error as e:
    print(f"Error {e}")
    sys.exit(1)
