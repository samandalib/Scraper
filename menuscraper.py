# -*- coding: utf-8 -*-
"""
Created on Sat May 25 14:31:37 2019

@author: Hesam
"""
import os
import json

"""**************************************************"""
""" RUN THIS FUNCTION FOR SCRAPING BASED ON CITY NAME """
"""**************************************************"""
def scrape_city(city,state): #enter abbreviation for the state argument, such as "ca" for "california"
    city = city.lower().replace(" ", "-")
    state = state.lower()
    url = f"https://www.allmenus.com/{state}/{city}/-/?filters=filter_online"
#    print(url)
    restaurants_list = get_restaurants(url)
    populate_menus(restaurants_list)
    return print(f"all resturants in {city} are now saved in the the directory with name {city}")
######################### END OF SECTION #####################################################################################
    

"""***********************************************************"""    
""" RUN THIS FUNCTION FO SCRAPING THE WHOLE DATA FROM THE SITE """
"""***********************************************************"""
def scrape_site():
    for url in urls:
        restaurants_list = get_restaurants(url)
        populate_menus(restaurants_list)
    
################################################ END OF SECTION ###############################################################

"""
    Openning a file containing state names and their abbreviations
"""
os.chdir("C:\\Users\\Hesam\\Desktop\\menu_parser\\countries\\usa")
with open("us_states.json") as f:
    g_states = f.read()
    g_states= json.loads(g_states)
#MAKING A FOLDER FOR EACH STATE
os.chdir("C:\\Users\\Hesam\\Desktop\\menu_parser\\countries\\usa\\states")#############CHECK DIRECTORIES FOR CHANGE
state_short = []
for state in g_states:
    name = state['name'].strip()
    if not os.path.exists(name):
        os.makedirs(name)
    state_short.append(state['abbreviation'].lower().strip())#to be used in making urls
####################### END OF SECTION ##############################  
#
#    
#  
    
"""
    Openning a file containing state names and their cities
"""
os.chdir("C:\\Users\\Hesam\\Desktop\\menu_parser\\countries\\usa")#############CHECK DIRECTORIES FOR CHANGE
with open("us_cities.json") as c:
    state_cities = c.read()
    state_cities = json.loads(state_cities)
##MAKING A FOLDER FOR EACH CITY IN ITS STATE FOLDER   
for state in state_cities:
    os.chdir(f"C:\\Users\\Hesam\\Desktop\\menu_parser\\countries\\usa\\states\\{state}")#############CHECK DIRECTORIES FOR CHANGE
    for city in state_cities[state]:
        if not os.path.exists(city):
            os.makedirs(city)
################################# END OF SECTION ##############################################
#
#            
#
#
#            
#            
"""
    Making URLs list for all cities in the US based on allmenus.com format
"""
def url_maker():
    urls=[]
    url_base = "https://www.allmenus.com/"
    urls = []
    for s in g_states:
        for ss in state_cities:
            if s['name'] == ss:
                for cty in state_cities[ss]:
                    url = url_base + s['abbreviation'].lower()+"/"+cty.replace(" ", "-").lower()+"/-/?filters=filter_online"
                    urls.append(url)
    return urls

urls = url_maker()  ##FUNCTION CALL##
#
#
################################## END OF SECTION #############################################
#
#
#

    
    
    
url="https://www.allmenus.com/ca/los-angeles/-/?filters=filter_online"

"""
    STEP1:
    Get list of restaurants from the URL
"""
def get_restaurants(url):
    import requests
    from bs4 import BeautifulSoup
    
    result = []

    
    restaurants_list = []
    response=requests.get(url)
    
    if response.status_code ==200:
        print("Response from URL with status code 200")
    else:
        print("No Response from all-restaurants URL")

    #parsing the URL
    result_page = BeautifulSoup(response.content,'lxml')
    
    div_tag= result_page.find_all('div', class_="s-row")
    
    #Getting each restaurnat's information
    for restaurant in div_tag:
        try:
            rest_props=[]
            rest_address=[]
            
            rest_head =  restaurant.find('h4', {'class':'name'})
            rest_id = rest_head.find('a').get('data-masterlist-id')
            rest_props.append(rest_id)
            
            rest_name = rest_head.get_text()
            rest_props.append(rest_name)
            
            rest_type=restaurant.find('p', {'class': 'cousine-list'}).get_text()
            rest_props.append(rest_type)
            
            address_finder = restaurant.find_all('p',{'class':'address'})
            rest_address = [address_finder[0].get_text(),address_finder[1].get_text()]
            rest_props.append(rest_address)
            
            restaurants_list.append(rest_props)
            print("restaurant basic document is created")
    
        except:
            print('an error in getting restuarant information')
    
    #creating a dictionary for each restaurant to populate furthur data in it
    for item in  restaurants_list:
        entity = {}
        _id = item[0]
        name = item[1]
        _type = item[2]
        address = item[3][0]
        location = item[3][1][:-7].split(",")
        city = location[0]
        rest_state = location[1].strip()
        state_abb = ""
        for state in g_states:
            if state['abbreviation'].strip() == rest_state:
                rest_state = state['name'].strip()
                
                state_abb = state['abbreviation'].strip()
#        print(rest_state)
        _zip = item[3][1][-5:]
        
        entity['id']= _id
        entity['name']= name
        entity['type']= _type
        entity['address']= address
        entity['state']=rest_state
        entity['city']= city.strip()
        entity['zip']= _zip
        entity['currency']='USD'
        entity['menu_url']="https://www.allmenus.com/"+state_abb.lower()+"/"+city.replace(" ", "-").lower()+"/"+_id+"-"+name.replace(" ","-").lower()+"/"+"menu/"
        result.append(entity)
        
    return result #returning a list of dictionaries that each represent a restaurant
  

"""
    STEP2:
    Now we can start parsing each restaurant's page and populate its menu info into the restaurants dictionary
"""

def populate_menus(restaurants_list):
    import requests
    from bs4 import BeautifulSoup
    
    #parsing menu page of each resturant
    for restaurant in restaurants_list:
        response=requests.get(restaurant['menu_url'])
         
        if response.status_code == 200:
            print("menu_url page obtained")
        else:
            print("No Response from restaurant URL")
        
        result_page = BeautifulSoup(response.content,'lxml') 
        
        rest_website = result_page.find('a', class_="menu-link").get('href')
        
        #making the menu section of the restaurnat document in database
        #search for categories in each menu
        menu_category= result_page.find_all('li', class_="menu-category")
        categories = []
        
        for category in menu_category:
             try:
                 category_content = {}
                 
                 #finding the name of category
                 categ_name = category.find('div', {'class':'h4 category-name menu-section-title'}).get_text()
                 category_content['category']=categ_name
                 
                 #finding items in each category
                 categ_items = category.find_all('ul', {'class':'menu-items-list unordered-list'})
                 
                 #making a list for each item in the menu consists of title, price, ingredients
                 items_list = []
                 
                 for item in categ_items:
                     try:
                         menu_item = {}
                         
                         item_title = item.find('span', {'class': 'item-title'}).get_text()
                         menu_item['title']= item_title
                     
                         item_price = item.find('span', {'class': 'item-price'}).get_text().strip()
                         item_price= item_price.replace("$","")
                         item_price = float(item_price)
                         menu_item['price'] = item_price
                     
                         item_desc = item.find('p', {'class': 'description'}).get_text()
                         menu_item['description']= item_desc
                         
                         item_ingredients = get_ingredients(item_desc)
                         menu_item['ingredients'] = item_ingredients
                         

                         items_list.append(menu_item)
                         
                     except:
                         print("error in getting items")
                     
                     
                     
                 category_content['items']=items_list
                 categories.append(category_content)
                 print("menu items successfully populated")
                     
             except:
                 print('an error in category organizer')
         
             
        restaurant['menu'] = categories
        restaurant['website']=rest_website
        #saving the result in a JSON File
        name = restaurant["name"]
        state = restaurant["state"]
        city = restaurant["city"]
        save_as_JSON(restaurant, state, city, name)
        print("restaurant json file created")
        
        
    return restaurants_list

########################################### END OF SECTION ########################################################
"""
     HELPING FUNCTION FOR populate_menus()
     it is used for saving result of each restaurant in its correct directory
"""
def save_as_JSON(restaurant,state, city,name):
    import json
    rest_JSON = json.dumps(restaurant, indent=4, sort_keys=True)
    os.chdir(f"C:\\Users\\Hesam\\Desktop\\menu_parser\\countries\\usa\\states\\{state}\\{city}")#############CHECK DIRECTORIES FOR CHANGE
    with open(f"{name}.json","w") as f:
        f.write(rest_JSON)
    return "THE JSON FILE IS SUCCESSFULLY CREATED FOR THIS RESTAURANT"

#
#
#
#
#
#
""" 
    HELPING FUNCTION FOR populate_menus() 
    extractying ingredients from description text
    based on master list of ingredients in db
"""
def get_ingredients(description):
    import re
    ingredients = []
    desc_clone = description
    
    #making a filter_list from exctracting files in database of ingredients
    filter_list = extracting_data(files)
    
    #check to see if there is any match for each item in filter_list in the description of the food
    for item in filter_list:
        try:
            item = item.strip().lower()
            pattern = re.compile(re.escape(item)+r"s?", re.I)
            matches = pattern.findall(desc_clone)
            for match in matches:
                if match not in ingredients:
                    ingredients.append(item)
                else:
                    continue
        except:
            continue

    #removing possible duplicates
    ingredients = list(dict.fromkeys(ingredients))
    
    #defining patterns for possible mistakes in the result of searching through description text
    regex_filters = [r"[0-9*]",r"[,!@#$%^&*+]", r"\s", r"^red$", r"^yellow$", r"^black$",  r"^green$" , r"'", r"^and$", r"^or$", r"^is$", r"^are$", r"^with$", r"^will$", r"^have$", r"^has$", r"^had$", r"^been$", r"^do$", r"^does$", r"^did$", "^done$"]
    
    for regex in regex_filters:
        try:
            pattern = re.compile(regex)
            for ing in ingredients:
                ing = ing.strip()
                if pattern.search(ing):
                    ingredients.remove(ing)
                elif len(ing)<2:
                    ingredients.remove(ing)

        except:
            print('error in regex pattern')
            
    #returning the ingredients extracted from description of the food
    return ingredients
    

"""
    HELPING FUNCTION FOR get_ingredients() 
    making a master list for possible ingredients 
    from existing databases on the net
"""

files = ["ingredients.csv"]
def extracting_data(files):
    import pandas as pd
    import os
    import re
    
    ingredients_master_list=[]
    
    #function for reading csv file 
    def data_import(file_name):
        
        os.chdir("C:\\Users\\Hesam\\Desktop\\menu_parser")#change the directory if the address is different
        data = pd.read_csv(file_name)
        return data
    print("OK-1")
    #reading each csv file from list of files
    for file in files:
        try:
            data = data_import(file)
            ingredients = pd.unique(data.name)
            ing_list = list(ingredients)
            ingredients_master_list += ing_list
        except:
            print("error in handling file")
    print("OK-2")
    #removing possible duplications in the list
    ingredients_master_list = list(dict.fromkeys(ingredients_master_list))
    
    #splitting the single line alias items to separate items and removing the original one
    for item in ingredients_master_list:
        if len(str(item))<2:
            ingredients_master_list.remove(item)
        try:
            temp = item.split(" or ")
            for i in temp:
                ingredients_master_list.append(i)
            ingredients_master_list.remove(item)
        except:
            continue
    print("OK-3") 
    #searching for and removing explainations in paranthesis and expressions after comma in each item
    for item in ingredients_master_list:
        pattern1 = re.compile(r"\s?\(.*\)\s?")
        pattern2 = re.compile(r",\s.*")
        try:
            if pattern1.search(item):
                replace = re.sub(pattern1,"", item)
                ingredients_master_list.append(replace)
                ingredients_master_list.remove(item)
            elif pattern2.search(item):
                replace = re.sub(pattern2,"", item)
                ingredients_master_list.append(replace)
                ingredients_master_list.remove(item)
            elif pattern1.search(item) and pattern2.search(item):
                replace = re.sub(pattern1,"", item)
                replace = re.sub(pattern2,"", replace)
                ingredients_master_list.append(replace)
                ingredients_master_list.remove(item)
        except:
            continue
    print("OK-4")
    #Removing possible duplicates from the master_list
    ingredients_master_list = list(dict.fromkeys(ingredients_master_list))
    
    return ingredients_master_list
    
        
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        