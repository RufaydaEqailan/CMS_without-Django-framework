import pymongo
from pymongo import MongoClient
import configuration
import modify_carts
from bson import ObjectId
import datetime
from geopy.geocoders import Nominatim
from time import sleep

from pymongo import DESCENDING, GEO2D

my_collection=configuration.getDBconnection("carts")

def show__carts_operation():
    """ Main  Cart Operations"""
    main_menu_list={"m":modify_cart,
                "s":show_carts_by_status,
                "c":delete_cart,
                "o":Set_old_carts,
                "v":search_by_value_,
                "l":search_by_location,
                "q":"Quite"
                }
    print("\n\n"+show__carts_operation.__doc__)
    print("=" * 40 +"\n" +"=" * 40 )

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

def modify_cart():
    """Modify selected cart"""
    cart_id=input("\nEnter teh id of the cart : ")
    try:
        cart_id=ObjectId(cart_id)
    except:
        print("=" * 40 +"\n" +"=" * 40 )
        print(f'\n\n{cart_id} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string')
        return
    
    print("\n")
    result=my_collection.find({"_id":cart_id})
    result=list(result)
    if len(result)==0:
        print("=" * 40 +"\n" +"=" * 40 )
        print(f"This cart with this ID : {cart_id} is not exiset !.")
    else:
        sub_menu={
                    "e":modify_carts.modify_master_category,
                    "d":modify_carts.delete_sub_cart,
                    "q":"Back to Main"
                    }
        next_action=""
        for key, value in sub_menu.items():
            # check if the value is a function
            if callable(value):
                print(f"{key}) {value.__doc__}")
            else:
            # print the quit option in the desired syntax
                print(f"{key}) {value}")
                
        next_action=input("\nAction?")
        if next_action in sub_menu:
            if  next_action!="q":
                sub_menu[next_action](ObjectId(cart_id))
            else:
                return

def show_carts_by_status():
    """Search based on status "abandon" / "paid" / "pending" """
    cart_status=input("\n\nEnter the status of the carts you want to fetch, paid-pending-abandon : \n\n")
    cart_status_list=["paid", "pending", "abandon"]
    # make list. if in list make find
    if cart_status in cart_status_list:
        query={"cart_status":cart_status.lower()}
        result=my_collection.find(query, {"_id":1,"cart_status":1})
        result=list(result)  

        print(f"List of carts which status is {cart_status}")
        print("=" * 40 +"\n" +"=" * 40 )
    
        if len(result)>0:
            for entry in result:
                print(entry)
                print("=" * 40 +"\n"  )
        else:
                print(f"Their is No carts with {cart_status} status .!")
                print("=" * 40 +"\n" +"=" * 40 )
    else:
        print("\n This status is no in the list paid-abandon-pending.. Try again \n")

def delete_cart():
    """Delete all carts collection"""
    if (input("\nAre you want to clear all the carts?(yes \ no)")=='Yes'):
        my_collection.drop()
    print("\nDatabase is empty NOW...\n")

def Set_old_carts():
    """Set the carts with the right status : "abandoned" / "paid" based on date """
    print("\n Modify all carts which are pending (Not paid) to Abandon status, before specifec date. \n")
    pending_date_before=input("\n Enter the date which befor set all carts status.\n Enter the Date in right format , the spirate List is: YYYY,NN,DD , YYYY MM DD or YYYY-MM-DD : \n" )
    if len(pending_date_before)==10:
        try:
            year=pending_date_before[:4]
            month=pending_date_before[5:7]
            day=pending_date_before[8:]
            pending_date_before=datetime.datetime(int(year), int(month), int(day))

            myquery = { "cart_created_at":{ "$lt":pending_date_before  }, "cart_status":"pending" }
            newvalues = { "$set": { "cart_status": "abandon" , "cart_abandoned_date":datetime.datetime.now(),"cart_paid_date":""} }
            result=my_collection.update_many(myquery, newvalues)
            
            if result.matched_count>0:
                print(f"\nThe new status :abandon for all carts which have create date before than  : {pending_date_before}  are updated successfully\n\n")
            else:
                print("\nThere is something wrong  happend... Try again later\n")
        except:
            print("\nThe date format is wrong YYYY,NN,DD , YYYY MM DD or YYYY-MM-DD .\n ")

    else:
        print("\n th date you enter is (Less\More) 10 Digit ..  \n")
            
def search_by_value_():
    """Find carts based on Create at created date, price , payment method"""
    parameter=input("\n \nWhat is the Field you want to search about it: cart_created_at, cart_total_price, cart_payment_methods, cart_products   ?\n\n")
    if parameter.lower()=="cart_payment_methods":
        #"payment method code goes here"
        field_value=[]
        available_methods=["VISA","PayPal","Master"]
        alternative_methods=input("\n Enter the number of methods you want to add (MAX 3nr,) :\n ")
        for i in range(int(alternative_methods)):
            paymentmethod=input(f"Give paymentmetod nr{i+1} : ")
            if paymentmethod in available_methods:
                field_value.append(paymentmethod)      
            else:
                print(f"\nThe paymentmethod {paymentmethod} is not in the available method list\n")
        query = {"cart_payment_methods": {"$in": field_value}}
        query_value={"cart_payment_methods":1, "_id":1}

    
    elif parameter.lower()=="cart_products":
        field_value=[]
        alternative_products=input("\n Enter the number of products you want to search (MAX 3nr,) :\n ")
        for i in range(int(alternative_products)):
            prod_ID=input(f"Give ID of product  nr{i+1} : ")
            try:
                prod_ID=ObjectId(prod_ID)
            except:
                print("=" * 40 +"\n" +"=" * 40 )
                print(f'\n\n{prod_ID} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string')
                return
            field_value.append(prod_ID)         
        query = {"cart_products": {"$in": field_value}}
        query_value={ "_id":1}

    elif parameter.lower()=="cart_total_price":
        parameter_value=input("\n Enter the total price you want search about it , in numerical format:\n ")
        try:
             parameter_value=int(parameter_value)
        except:
            print("\nThe price you enter is not numerical data ... try again .\n")
        query={"cart_total_price": parameter_value}
        query_value={"cart_total_price":1, "_id":1,}
    # make for all dates
    elif parameter.lower()=="cart_created_at":
        create_date=input("\n Enter the created date for the carts you want .  \n Enter the Date in right format , the spirate List is: YYYY,NN,DD , YYYY MM DD or YYYY-MM-DD : \n" )
        if len(create_date)==10:
            try:
                year=create_date[:4]
                month=create_date[5:7]
                day=create_date[8:]
                create_date=datetime.datetime(int(year), int(month), int(day))
            except:
                print("\nThe date format is wrong YYYY,NN,DD , YYYY MM DD or YYYY-MM-DD . \n")
        else:
            print("\n th date you enter is (Less\More) 10 Digit .. \n ")
        query = { "cart_created_at":create_date   }
        query_value={"cart_created_at":1, "_id":1,}

    entries=my_collection.find(query, query_value)
    entries=list(entries)

    print(f"List of carts with field is {parameter}")
    print("=" * 40 +"\n" +"=" * 40 )
    if len(entries) > 0:
             for entry in entries:
                 print(entry)
                 print("\n")
    else:
         print(f"\nThere is no catrs for this field : {parameter}... \n\n")
            
    # if date   kl:15.20 2023 03 09
                
def search_by_location():
    """Find carts based on Location"""   
    xloc=input("\n\n Provide the x coordinate : ")
    yloc=input("\n\n Provide the y coordinate : ")

    my_collection.create_index([("cart_location", pymongo.GEO2D)])
    location=f"{xloc},{yloc}"
    geoLoc = Nominatim(user_agent="GetLoc")
    sleep(1)
    locname = geoLoc.reverse(location)
    print(f'Carts near to location {locname.address}:')

    query = {"cart_location": {"$near": [int(xloc), int(yloc)]}}
    results = my_collection.find(query,{"cart_products":0})

    for result in results:
        print(result)
        print("\n")
        location=f'{result["cart_location"][0]},{result["cart_location"][1]}'
        geoLoc = Nominatim(user_agent="GetLoc")
        sleep(1)
        locname = geoLoc.reverse(location)
        print(f'Location:  {locname.address}:')
        print("\n\n")

            
