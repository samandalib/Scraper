# -*- coding: utf-8 -*-
"""
Created on Mon May 27 17:33:01 2019

@author: Hesam
"""

import pymongo
import os
import json

state = input('Enter the name of STATE(capitalized): ')
city = input('Enter the name of CITY(capitalized+single spcaced btw words): ')


l = os.listdir()

def connect_to_db():
    client =  pymongo.MongoClient("mongodb+srv://hesamandalib:hesam14239@restaurant-7f8ln.mongodb.net/test?retryWrites=true")

    db = client.get_database("test")
    restaurants_records = db.restaurants
    users_records = db.users

    print('test restaurants collection with count_documents: ', restaurants_records.count_documents({}))
    print('test users collection with count_documents: ',users_records.count_documents({}))

    
    return (restaurants_records, users_records)

def make_users_list(state,city):#call the function and provide name of the state and city capitalized using space if needed; e.g. California, Los Angeles
    #print(restaurants)
    try:
        os.chdir(f"C:\\Users\\Hesam\\Scraper\\countries\\usa\\states\\{state}\\{city}")##CHECK THE DIRECTORY BEFORE EXECUTING FILE
        file_names = os.listdir()
#        print(file_names)
    except:
        print('the state/city name is not according to rules')
        
    users = []
    
    db = connect_to_db()
    restaurants_records = db[0]
    users_records = db[1]
    
    restaurants = list(restaurants_records.find())
    ids = [restaurant['id'] for restaurant in restaurants]

    
    for name in file_names:
        try:
            with open(f"{name}") as f:
                data=f.read()
                data = json.loads(data)

            try:
                #first: make a username and password for each restaurant 
                user = {}
                username = make_username(data)
                #second: check if the restaurant does exists in the data base           
                if data["id"] not in ids:#if it does not, then register the restaurant to the database and make a record for its user in users collection
                    user = {"_id": data["id"], "username": username, "password":username[-7:]}
                    users.append(user)
#                    print(user)
                    data['owner']=username#update the restaurant object with owner field added
                    
                    restaurants_records.insert_one(data)#insert the restaurant record in its collection in db
                    print('restuarant added to db')
    #                users_records.insert_one(user)#insert the user record in users collection in db
    #                print('user added to db')
#                    print("data uploaded on db")
                else:
                    print(f"data with id:{data['id']} already exists on db, so aborted duplication")
            except:
                print("There is an error in database handling, check the database entries to be sure it is alright")

        except:
            print('Error in openning files from folder')
    return users
 
make_users_list(state,city)
users = make_users_list('California','San Diego')
#print(users)


def users_json(users,state,city):
#    print('users_json: ', users)
#    users = str(users)
    users_JSON = json.dumps(users, indent=4, sort_keys=True)

#    return users
    file_name = f'{city}All.json'
    try:
        existing_files = os.listdir()
        if file_name not in existing_files:
            with open (file_name, "w") as file:
                file.write(users_JSON)
            print('File did not exist, so separate file created for users')
            
        else:
            os.remove(f"C:\\Users\\Hesam\\Scraper\\countries\\usa\\states\\{state}\\{city}\\{file_name}")
            with open (file_name, "w") as file:
                file.write(users_JSON)
            print('File alrady existed so it was removed and a separate file created for users')
            
            
#        print(users)
    #    users_records.insert_many(users, ordered=False)#THERE IS AN ERROR IN INSERTING USER DATA TO THE DATABASE!!!!!!
        print(f'user file created successfully with name {file_name}')
    except:
        print('error in inserting users list to db')
    return file_name

#######FUNCTION CALL#########
users_json(users,state, city)
#############################

city_users_file = users_json(users,state,city)

def users_insert(city_users_file):
    with open(city_users_file) as f:
        users_data = f.read()
        users_data = json.loads(users_data)
    print(users_data)
    db = connect_to_db()
    users_records = db[1]
    print('Users records existing in db: ',users_records.count_documents({}))
#    for user in users_data:
#    print("USER DOCUMENT IS : ", user)
    try:    
        users_records.insert_many(users_data, ordered = False)
        return ('user document succesfully inserted to the data base')
    except:
        print('THERE IS AN ERROR IN INSERTING USER DATA TO DB')
        raise
users_insert(city_users_file)

def make_username(restaurant):
    try:
        first_part = restaurant['name'][0:4].replace(" ","x")
#        print("username first part")
        second_part = restaurant['city'].split()
#        print("username second part")
        city_abb = ""
        if len(second_part)>1:
            for part in second_part:
                city_abb += part[0]
            second_part = city_abb
        else:
            second_part=restaurant['city'][0]
            
        third_part = restaurant['zip']
        username = first_part+"-"+second_part+third_part
#        print(username)
        return username
    except:
        print("error in making USERNAME")