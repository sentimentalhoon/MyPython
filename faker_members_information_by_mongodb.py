from faker import Faker
import sys
import numpy as np
import pymongo
import json

try:
    connectionString = "mongodb+srv://sentimentalhoon:U20WArnMN2o6I03J@cluster0.q3lazme.mongodb.net/?retryWrites=true&w=majority&authMechanism=SCRAM-SHA-1";
		
    myclient = pymongo.MongoClient(connectionString)
    mydb = myclient["sayproject"]
    mycol = mydb["202309"]

    fake = Faker("ko-KR")
    
    mylist = []
    for i in range(1):
        # 이름
        name = fake.name()
        # 트레이너
        trainer = 1001

        mydict = { 
                "name" : name,
                "trainer" : trainer
                  }
        x = mycol.insert_one(mydict)
        #mylist.append(mydict)

    #print(mylist)
    #x = mycol.insert_many(mylist)
    #print(x.inserted_ids)
except Exception as e:
    print(f"Error {e}")
    sys.exit(1)