import pymongo
from pymongo import MongoClient
import configration
import modify_carts
import manage__users
from bson import ObjectId
import datetime
from geopy.geocoders import Nominatim
from time import sleep
from geopy.exc import GeocoderTimedOut
from pymongo import DESCENDING, GEO2D
import pdb

my_collection_carts=configration.getDBconnection("carts")
my_collection_user=configration.getDBconnection("users")

def show_total_options():
    """MY Statistic LIST"""
    print("=" * 40 +"\n" +"=" * 40 )
    print(show_total_options.__doc__)
    print("=" * 40 +"\n" +"=" * 40 )

    main_menu_list={"o":get_users_value,
                "r":get_total_revenu_by_year,
                "s":Enter_location_stats,
                "q":"Quite"
                }
    
    action=""
    while action !="q":
        for key, value in main_menu_list.items():
            # check if the value is a function
            if callable(value):
                print(f"{key}) {value.__doc__}()")
            else:
            # print the quit option in the desired syntax
                print(f"{key}) {value}")

        action=input("\nAction?")
        if action in main_menu_list:
            if  action!="q":
                 main_menu_list[action]()
            else:
                return   

def get_users_value():
    """Get the price for the carts this user has been paid"""
    total_sum=0
    user_id=input("\nEnter teh id of the user : ")
    try:
        user_id=ObjectId(user_id)
    except:
        print("=" * 40 +"\n" +"=" * 40 )
        print(f'{user_id} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string')
        return
    print("\n")

    result=my_collection_user.find_one({"_id":user_id})
    # result=list(result)
    if len(result)==0:
        print("=" * 40 +"\n" +"=" * 40 )
        print(f"\n\nThis user with this ID : {user_id} is not exiset !.")
    
    else:
            # print(carts_num)
            carts=result["users_carts"]
            #"loop in the list in the Document"
            for res in carts:
                res= ObjectId(res)
                # print(query)
                #cart=my_collection_carts.find_one({'_id':res})
                cart_price=modify_carts.calculate_cart_total_price(res)
                # print(cart)
                total_sum+=cart_price
                print(f"\nCart with ID {res} has price {cart_price}")
            
            print("=" * 40 +"\n" )
            print(f"\n\nTotal carts value for user {result['users_name']}, is {total_sum}")
            print("=" * 40 +"\n" )

def get_total_revenu_by_year():
    """Get total year sales from carts"""
    year=input("\nWhat year do you want to check the sales for :  ")
         # Find all paid carts in the specified year
     # Specify the date range to search for
    try:
        year=int(year)
    except:
        print("\nThis year is not in the right format 0000 four digits.. try again")

    start_date = datetime.datetime(year, 1, 1)
    end_date = datetime.datetime(year, 12, 31)

    # Find all paid carts between the specified dates
    query = {
        "cart_status": "paid",
        "cart_paid_date": {"$gte": start_date, "$lte": end_date}
    }
    # print(query)
    total_revenu=0
    paid_carts=my_collection_carts.find(query)
    paid_carts=list(paid_carts)
    if len(paid_carts)>0:
        for cart in paid_carts:
            print(f'\nCart with id {cart["_id"]} has price {cart["cart_total_price"]}')
            total_revenu+=cart["cart_total_price"]
        print("=" * 40 +"\n"  )   
        print(f"\nTotal revenue for {year} is {total_revenu} ")
        print("=" * 40 +"\n"  )   
    else:
        print("\n\nThere is no paid carts in this year...try with another year.")
    
def Enter_location_stats():
    """Enter a location and see stats"""
    # xloc=input("\n\nProvide the x coordinate : ")
    # yloc=input("\n\nProvide the y coordinate : ")
    city=input("\nProvide the city name : ")
    Distance=input("\n\nProvide the distance : ")
    xloc=0
    yloc=0
    my_collection_carts.create_index([("cart_location", "2dsphere")])
    geoLoc = Nominatim(user_agent="GetLoc")
    location = geoLoc.geocode(city)
    coordinates = [int(location.latitude), int(location.longitude)]
    sleep(1)
    # print(coordinates)
    # print(f'Carts near to location {xloc,yloc}:')

    # query = {"cart_location": {"$near": [int(xloc), int(yloc)]}}
    # results = my_collection_carts.find(query,{"cart_products":0})
    results=my_collection_carts.aggregate([
        {
           '$geoNear': {
            'near': { 'type': "Point", 'coordinates':coordinates },
            'distanceField': "dist.calculated",
            'maxDistance': int(Distance)*1000,
            'includeLocs': "dist.location",
            'spherical': True
            }
        }
        ])
    
    users=[]
    carts=[]
    users_info=[]
    total_near_price=0
    results=list(results)
    if len(results)>0:
        for result in results:
            print(result)
           # pdb.set_trace()
            if result["_id"] not in carts:
                carts.append(result["_id"])
            total_near_price+=result["cart_total_price"]
        # print(result)
        location=f'{result["cart_location"][0]},{result["cart_location"][1]}'
        geoLoc = Nominatim(user_agent="GetLoc")
        sleep(1)
        locname = geoLoc.reverse(location)
        print(f'Location:  {locname.address}:')
        query_user={"users_carts": {"$in": [result["_id"]]}}
        all_user_id=my_collection_user.find(query_user)
        for user_id in all_user_id:
            # print(user_id["_id"])
             if user_id["_id"] not in users:
                users.append(user_id["_id"])
    # print(users)
    users_count=len(users)
    carts_amount=len(carts)
    
    print("=" * 40 +"\n"  )   
    print(f" Total amount of users buying in these coordinates : {users_count}")
    print(f" Total amount of carts buying in these coordinates : {carts_amount}")
    print(f"\n Total carts value for the provided coordinates  is : {total_near_price} sek")
    print("=" * 40 +"\n"  ) 
    # print("=" * 40 +"\n"  ) 
    user_informations=input("\nDo you want information for these users Y/N ?")
    
    if user_informations.lower()=="y":
        for user_id in users:
            user_query={"_id":user_id}
            # user_info=my_collection_user.find_one(user_query)
            user_info=manage__users.show__users(UserID=user_id)
            users_info.append(user_info)
            
        print(users_info)
        print("=" * 40 +"\n"  ) 
    else:
            carts_status=input("\nDo you want to see carts by status in this area Y/N ?")
            if carts_status.lower()=="y":
                user_carts_status=input("\nWhich status is it (paid / pending / abandon ) ?")
                # print(carts)
                for cart in carts:
                    query_cart={"_id":cart, "cart_status":user_carts_status}
                    # print(query_cart)
                    res=my_collection_carts.find_one(query_cart)
                    if res !=None:
                        print(res)
                        print("\n\n")
                    else:
                        print("\n\n")
                print("=" * 40 +"\n"  ) 

    

    
