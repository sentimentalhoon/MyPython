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

        conn.commit()
        conn.close()
except pymysql.Error as e:
    print(f"Error {e}")
    sys.exit(1)
