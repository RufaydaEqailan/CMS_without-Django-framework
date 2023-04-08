import pymongo
from pymongo import MongoClient
import configration
import re
import datetime
from bson import ObjectId


my_collection=configration.getDBconnection("carts")
my_collection_products=configration.getDBconnection("product")

def modify_master_category(cart_id):
    """Modify selected cart based on : Price , Discount"""
    field_name=input('\n Enter the name of field you want to modify:  cart_total_price , cart_discount ?')
    try:
        if field_name.lower()=="cart_total_price":
            field_value=input("\nEnter the total price you want to modify , numerical numbers :  ")
            try:
                field_value=int(field_value)
            except:
                print("The total price value not acceptable format")
                raise ValueError
            
            myquery = { "_id":cart_id }
            newvalues = { "$set": { field_name.lower(): field_value } }
            result=my_collection.update_one(myquery, newvalues)
            if result.matched_count>0:
                print(f"\nThe new total price {field_value} for the  cart with ID {cart_id} is updated successfully\n\n")
            else:
                print("\nThere is something wrong  happend... Try again later")
        
        elif field_name.lower()=="cart_discount":
            field_value=input("\nEnter the Discount avlue you want to modify , must be Numerical data :  ")
            try:
                field_value=int(field_value)
            except:
                print("\nThe Discount value not acceptable format\n")
                raise ValueError
            price_discount=result["cart_total_price"]-(result["cart_total_price"]*(field_value/100))
            myquery={"_id":cart_id}
            newvalues = { "$set": {  "cart_discount":field_value, "price_discount":price_discount}}
            result=my_collection.update_many(myquery, newvalues)
            if result.matched_count>0:
                print(f"\nThe new Discount  for the cart ID : {cart_id}  is updated successfully\n\n") 
            else:
                print("\nThere is something wrong  happend... Try again later\n\n")
    except ValueError:
        print("\nThere is something wrong. Try again!\n")

def delete_sub_cart(cart_id):
    """delete_sub_cart"""
    choice1=input("Are you sure to delete the cart ? Y/N :")
    if choice1 =="Y":
        try:
            result=my_collection.find({"_id":cart_id})
            result=list(result)   
        except:
            print("=" * 40 +"\n" +"=" * 40 )
            print(f"\nYour choice is begin redirected, Ther is no carts  with thid ID {cart_id}  !.\n")
        
        if len(result)>0:
                if result[0]["cart_status"]!="paid":
                    myquery = { "_id": cart_id }
                    # my_collection.find_one_and_delete(myquery)
                    newvalues={"$set": {"cart_abandoned_date":datetime.datetime.now(),"cart_status":"abandon","cart_paid_date":""}}
                    result=my_collection.update_one(myquery,newvalues)
                    if result.matched_count>0:
                        print(f"\n\nThe cart which has ID {cart_id} is abandoned successfully\n\n")
                    else:
                        print("\n\nThere is something wrong  happend... Try again later\n\n")
                elif result[0]["cart_status"]!="abandon":
                    myquery = { "_id": cart_id }
                    # my_collection.find_one_and_delete(myquery)
                    newvalues={"$set": {"cart_status":"abandon","cart_paid_date":""}}
                    result=my_collection.update_one(myquery,newvalues)
                    if result.matched_count>0:
                        print(f"\n\nThe cart which has ID {cart_id} is abandoned successfully\n\n")
                    else:
                        print("\n\nThere is something wrong  happend... Try again later\n\n")        
                else:
                    myquery = { "_id": cart_id }
                    my_collection.find_one_and_delete(myquery)
                    print(f"This cart with this ID : {cart_id}  ... is Deleted sucessfully!.")  

def calculate_cart_total_price(id):
    """Get Total price for the cart"""
    total_price=0
    cart_id=id
    try:
        cart_id=ObjectId(cart_id)
    except:
       print("=" * 40 +"\n" +"=" * 40 )
       print(f'{cart_id} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string')
       return
       print("\n")
    query={"_id":cart_id}   
    carts=my_collection.find_one(query)
    if len(carts)==0:
        print("=" * 40 +"\n" +"=" * 40 )
        print(f"\n\nThis cart with this ID : {cart_id} is not exiset !.")
    else:
        products=carts["cart_products"] 
        for product in products:
            product=ObjectId(product)
            prod_query={"_id":product}
            prod=my_collection_products.find_one(prod_query)

            if len(prod)==0:
                continue
            else:
                total_price+=prod["price"]
        query_update={"$set":{"cart_total_price":total_price}}
        update_cart=my_collection.update_one(query,query_update)
        if update_cart.matched_count>0:
            return total_price
        else:
            print("\n\nTher is problem in update the total price for the cart")

def get_near_location():
    """GET THE NEAR LOCATIONS"""
    