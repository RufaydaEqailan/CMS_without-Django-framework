import pymongo
from pymongo import MongoClient
import configuration
import re
import datetime

my_collection=configuration.getDBconnection("users")

def modify_master_category(user_id):
    """modify_master_category"""
    try:
        field_name=input('\n Enter the name of field you want to update?')
        if field_name.lower()!="users_payment_methods":
            if field_name.lower()=="users_email":
                #"validation email goes here"
                email_pattern="([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
                field_value=input('\nEnter the new value of Email field in the right format test@test.com : ')
                if  re.search(email_pattern, field_value)==None:
                    print("\nNot valid email formate , must be like this formate: name.surname@gmail.com")
                    raise ValueError

            elif field_name.lower()=="users_credit_card":
                 #"validation users_credit_card goes here"
                field_value=input('\nEnter the new value of Cridet card  field in the right format 16 Digits : ')
                
                if  len(field_value)==16:
                    #print(len(field_value)) 
                    part_one=field_value[0:4]
                    part_two=field_value[4:8]
                    part_three=field_value[8:12]
                    part_four=field_value[12:16]
                    field_value=part_one+" "+part_two+" "+part_three+" "+part_four
                else:
                    print("\nThe cridet card is wrong (Less\More) 16 Digit ..  ")
                
            elif field_name.lower()=="users_online" or field_name.lower()=="users_regiterd_at":
                #"validation users_online and users_regiterd_at Dates goes here"
                field_value=input("\n Enter the Date in right format , the spirate List is: YYYY,NN,DD , YYYY MM DD or YYYY-MM-DD : ")
                if len(field_value)==10:
                    year=field_value[:4]
                    month=field_value[5:7]
                    day=field_value[8:]
                    field_value=datetime.datetime(int(year), int(month), int(day))
                else:
                    print("\nThe date format is wrong YYYY,NN,DD , YYYY MM DD or YYYY-MM-DD , (Less\More) 10 Digit ..  ")
                    raise ValueError
                
            elif field_name.lower()=="users_payment_methods":
                #"payment method code goes here"
                field_value=[]
                available_methods=["VISA","PayPal","Master"]
                alternative_methods=input("\n Enter the number of methods you want to add (MAX 3nr,) : ")
                for i in range(int(alternative_methods)):
                    paymentmethod=input(f"\nFrom this list [VISA,PayPal,Master] Enter paymentmetod nr{i+1} : ")
                    if paymentmethod in available_methods:
                        field_value.append(paymentmethod)
                    else:
                        print(f"The paymentmethod {paymentmethod} is not in the available payment method list [VISA,PayPal,Master] .")
            else:#Question to Gustavo about if elif else =>else didn't work out of elif?
                field_value=input('\nEnter the new value of  field you want to update : ')
        new_field_value=field_value
        if field_name and new_field_value:
            #"update code goes here if both values are not empty"
            myquery = { "_id":user_id }
            newvalues = { "$set": { field_name.lower(): new_field_value } }
            result=my_collection.update_one(myquery, newvalues)
            
            if result.matched_count>0:
                print(f"\nThe new value : {new_field_value } for a filed : {field_name} is updated successfully")
            else:
                print("\nThere is something wrong  happend... Try again later")
            
        else:
            print("\n Please check field name or field value is not empty.")
            raise ValueError
        
    except ValueError:
        print("\nThere is something wrong. Try again!")


def delete_sub_user(user_id):
    """delete_sub_user"""
    choice1=input("Are you sure to delete the user ? Y/N :")
    if choice1 =="Y":
        try:
            result=my_collection.find_one({"_id":user_id})
            result=list(result)

            if len(result)>0:
                myquery = { "_id": user_id }
                my_collection.find_one_and_delete(myquery)
                print(f"This user with this ID : {user_id}  ... is Deleted !.")  
                
        except:
            print("=" * 40 +"\n" +"=" * 40 )
            print(f"Your choice is begin redirected, Ther is no users  with thid ID {user_id}  !.")
    