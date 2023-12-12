from faker import Faker
import sys
import numpy as np
import mysql.connector
from datetime import datetime, time
import uuid
import redis
import json
try:
    conn = mysql.connector.connect(
        user="sam9mo",
        passwd="sam9mo!!",
        host="59.3.28.12",
        port=3306,
        database="sam9mo",
    )
    rd = redis.StrictRedis(host='59.3.28.12', port=6379, db=0, password="sam9mo!!")

    with conn:
      with conn.cursor(dictionary=True) as cursor:
          cursor.execute("select * from kospi_code")
          result = cursor.fetchall()

          num_fields = len(cursor.description)
          field_names = [i[0] for i in cursor.description]
          
          for data in result:
            rd.set(data["abbreviation_Code"], json.dumps(data)) 

          cursor.execute("select * from kosdaq_code")
          result = cursor.fetchall()

          num_fields = len(cursor.description)
          field_names = [i[0] for i in cursor.description]
          
          for data in result:
            rd.set(data["abbreviation_Code"], json.dumps(data)) 

except Exception as e:
    print(f"Error {e}")
    sys.exit(1)
