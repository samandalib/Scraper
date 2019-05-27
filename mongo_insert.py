# -*- coding: utf-8 -*-
"""
Created on Mon May 27 17:33:01 2019

@author: Hesam
"""

import pymongo
import os
import json

myclient =  pymongo.MongoClient("mongodb+srv://hesamandalib:hesam14239@restaurant-7f8ln.mongodb.net/test?retryWrites=true")

mydb = myclient["Totell"]
mycol = mydb["restaurants"]
os.chdir("C:\\Users\\Hesam\\Desktop\\menu_parser\\countries\\usa\\states\\California\\Los Angeles")

with open("Papa Cristos.json") as f:
    mydata=f.read()

print(type(mydata))
    