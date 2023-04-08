import pymongo
from pymongo import MongoClient
import configration

my_collection=configration.getDBconnection("product")

def modify_master_category(prod_id):
    """modify_master_category"""
    result=my_collection.find({"_id":prod_id})

    if not result:
        print("=" * 40 +"\n" +"=" * 40 )
        print(f"This product with this ID : {prod_id} is not exiset !.")

    field_name=input('Enter the name of field you want to update?')
    field_value=input('Enter the new value of field you want to update?')
    
    if field_name and field_value:
       
            if field_name.lower()=="year" or field_name.lower()=="price":
                try:
                    field_value=int(field_value)                    
                except:
                    print("=" * 40 +"\n" +"=" * 40 )
                    print(f"this is value {field_value} is not number.")

            myquery = { "_id":prod_id }
            newvalues = { "$set": { field_name.lower(): field_value } }
            my_collection.update_one(myquery, newvalues)
    else:
        print("=" * 40 +"\n" +"=" * 40 )
        print("Enter the name of field or the value is empty !.")
        modify_master_category(prod_id)
    
def delete_sub_product(prod_id):
    """delete_sub_product"""
    choice1=input("Are you sure to delete the product? Y/N :")
    if choice1 =="Y":
        try:
            result=my_collection.find_one({"_id":prod_id})
            result=list(result)

            if len(result)>0:
                myquery = { "_id": prod_id }
                my_collection.find_one_and_delete(myquery)
                print(f"This product with this ID : {prod_id} is Deleted !.")  
                
        except:
            print("=" * 40 +"\n" +"=" * 40 )
            print(f"Your choice is begin redirected, Ther is no products with thid ID {prod_id}  !.")
    