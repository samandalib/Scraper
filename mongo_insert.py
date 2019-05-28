# -*- coding: utf-8 -*-
"""
Created on Mon May 27 17:33:01 2019

@author: Hesam
"""

import pymongo
import os
import json


l = os.listdir()

client =  pymongo.MongoClient("mongodb+srv://hesamandalib:hesam14239@restaurant-7f8ln.mongodb.net/test?retryWrites=true")

db = client.get_database("test")
records = db.restaurants

print(records.count_documents({}))

os.chdir("C:\\Users\\Hesam\\Desktop\\menu_parser\\countries\\usa\\states\\California\\Los Angeles")
file_names = os.listdir()
print(file_names)

for name in file_names:
    with open(f"{name}") as f:
        data=f.read()
        data = json.loads(data)
        records.insert_one(data)
        print("data uploaded on db")
    