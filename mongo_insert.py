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
restaurants_records = db.restaurants
users_records = db.users

print(restaurants_records.count_documents({}))
print(users_records.count_documents({}))

restaurants = list(restaurants_records.find())
ids = [restaurant['id'] for restaurant in restaurants]

#print(restaurants)
os.chdir("C:\\Users\\Hesam\\Desktop\\menu_parser\\countries\\usa\\states\\California\\Los Angeles")
file_names = os.listdir()
print(file_names)
users = []
for name in file_names:
    with open(f"{name}") as f:
        data=f.read()
        data = json.loads(data)
        try:
            #first: make a username and password for each restaurant 
            user = {}
            if '_id' in user:
                del user['_id']
            print(user)
            username = make_username(data)
            #second: check if the restaurant does exists in the data base           
            if data["id"] not in ids:#if it does not, then register the restaurant to the database and make a record for its user in users collection
                user = {"id": data["id"], "username": username, "password":username}
                users.append(user)
                data['owner']=username#update the restaurant object with owner field added
                restaurants_records.insert_one(data)#insert the restaurant record in its collection in db
                print('restuarant added to db')
                print(user)
#                users_records.insert_one(user)#insert the user record in users collection in db
#                print('user added to db')
                print("data uploaded on db")
            else:
                print(f"data with id:{data['id']} already exists on db, so aborted duplication")
        except:
            print("There is an error in database handling, check the database entries to be sure it is alright")

#inserting users to db
try:
    print(users)
    users_records.insert_many(users)#THERE IS AN ERROR IN INSERTING USER DATA TO THE DATABASE!!!!!!
    print('user data inserted successfully')
except:
    print('error in inserting users list to db')
    
def make_username(restaurant):
    first_part = restaurant['name'][0:4].replace(" ","x")
    second_part = restaurant['city'].split()
    city_abb = ""
    for part in second_part:
        city_abb += part[0]
    second_part = city_abb
    third_part = restaurant['zip']
    username = first_part+"-"+second_part+third_part
    print(username)
    return username