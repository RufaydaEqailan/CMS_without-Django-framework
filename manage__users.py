import pymongo
from pymongo import MongoClient
import configuration
import pprint
import modify_users
from bson import ObjectId
import datetime
import re
import getpass

my_collection=configuration.getDBconnection("users")

class Users():
    def __init__(self,users_name,users_email,users_password,users_status,users_online,users_carts,users_payment_methods,users_regiterd_at,users_credit_card ):
        self.qualites={"users_name":users_name,"users_email":users_email,"users_password":users_password,"users_status":users_status,"users_online":users_online,"users_carts":users_carts,
                       "users_payment_methods":users_payment_methods,"users_regiterd_at":users_regiterd_at,"users_credit_card":users_credit_card}
        
def show__users(**kwargs):
    """MY Users LIST"""
    print("=" * 40 +"\n" +"=" * 40 )
    print(show__users.__doc__)
    print("=" * 40 +"\n" +"=" * 40 )

    
    # if queryType=='general':
    #     collection__doc=my_collection.find({}).limit(10)
    #     for user in collection__doc:
    #         print(user)
    # elif queryType==UserID:
    #     query={'_id':ObjectId(UserID)}
    #     print(query)
        # user=my_collection.find_one({'_id':ObjectId(UserID)})
        # return user
# **kwargs
    for arg in kwargs.keys():
            if kwargs[arg] == "general":
                users = my_collection.find({}).limit(10)
                for user in users:
                    print(user)
            elif arg == "UserID":
                user = my_collection.find_one({"_id":kwargs[arg] })
                return (user)
# calling
# manage_users.show_users(UserID='AAA', queryType='general', status='active')

    main_menu_list={"a":add_user,
                    "m":modify_user,
                    "s":show_categories_user,
                    "c":delete_user,
                    "mc":Set_old_users,
                    "v":search_parameter_value_user,
                    "q":"Quite"
                }
    
    action=""
    while action !="q":
        if user:
            print("=" * 40 +"\n" +"=" * 40 )

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
            
def add_user():
    """Add a anew user"""
    users_online = ""

    field_value=[]
    number_of_products=input("\n Enter the number of products you want to add (MAX 3nr,) : ")
    for i in range(int(number_of_products)):
        product=input(f"\n Enter ID for product nr{i+1} : ")
        field_value.append(product)
    print(f"The list of products in user cart is: {field_value} .")
    users_carts=field_value

    users_name=input("\nName of the user?:")

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
    users_payment_methods=field_value

    users_regiterd_at=datetime.datetime.now()
    #"validation email goes here"
    email_pattern="([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
    field_value=input('\nEnter the new value of Email field in the right format test@test.com : ')
    if  re.search(email_pattern, field_value)==None:
        print("\nNot valid email formate , must be like this formate: name.surname@gmail.com")
        
    users_email=field_value

    users_password= getpass.getpass("\Enter  Password ---- password should be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one digit, and one special character?:")
    while True:
        # define the regular expression for password validation
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        if re.match(pattern, users_password):
            print("Valid password")
            break
        else:
            print("Invalid password")

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
    users_credit_card=field_value

    users_status="active"

    user=Users(users_name,users_email,users_password,users_status,users_online,users_carts,users_payment_methods,users_regiterd_at,users_credit_card)
    newUser=user.qualites

    result = my_collection.insert_one(newUser)
    if result.acknowledged:
                print('\n' + '=' * 40 + '\n')
                print(f'\nUser {users_name} is added succesfully ...')
                print("=" * 40 +"\n" +"=" * 40 )
                print(show__users.__doc__)
                print("=" * 40 +"\n" +"=" * 40 )
                collection__doc=my_collection.find({}).limit(10)             
                for user in collection__doc:
                    print("\n")
                    print(user)

def modify_user():
    """Modify selected user"""
    user_id=input("\nEnter teh id of the user : ")
    try:
        user_id=ObjectId(user_id)
    except:
        print("=" * 40 +"\n" +"=" * 40 )
        print(f'{user_id} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string')
        return
    print("\n")
    result=my_collection.find({"_id":user_id})
    result=list(result)
    if len(result)==0:
        print("=" * 40 +"\n" +"=" * 40 )
        print(f"This user with this ID : {user_id} is not exiset !.")
    else:
        sub_menu={
                    "d":modify_users.modify_master_category,
                    "e":modify_users.delete_sub_user,
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
                sub_menu[next_action](ObjectId(user_id))
            else:
                return

def show_categories_user():
    """Show the different user payment methods"""
    all_users=my_collection.find({})
    # paymentmethods=[]

    for entry in all_users:
        # if not entry["users_payment_methods"] in paymentmethods:
            # paymentmethods.append(entry["users_payment_methods"])
        
        print(entry["users_name"] + "  has this payment method list :   ")
        print(entry["users_payment_methods"])
        print("=" * 40 +"\n" +"=" * 40 )

def delete_user():
    """Clear users list"""
    if (input("\nAre you want to clear all the users?(yes\no)")=='Yes'):
        my_collection.drop()
    print("\Database is empty NOW...")

def Set_old_users():
    """Set an status 'terminated' for all users accounts where Online < some value"""
    online_value=input("\n Enter online date for all the users which their status must be terminated before.  \n Enter the Date in right format , the spirate List is: YYYY,NN,DD , YYYY MM DD or YYYY-MM-DD : " )
    if len(online_value)==10:
        try:
            year=online_value[:4]
            month=online_value[5:7]
            day=online_value[8:]
            online_value=datetime.datetime(int(year), int(month), int(day))

            myquery = { "users_online":{ "$lt":online_value  } }
            newvalues = { "$set": { "users_status": "terminated" } }
            result=my_collection.update_many(myquery, newvalues)
            
            if result.matched_count>0:
                print(f"\nThe new status :terminated for all users who has online date less than  : {online_value}  are updated successfully")
            else:
                print("\nThere is something wrong  happend... Try again later")
        except:
            print("\nThe date format is wrong YYYY,NN,DD , YYYY MM DD or YYYY-MM-DD . ")

    else:
        print("\n th date you enter is (Less\More) 10 Digit ..  ")
            
def search_parameter_value_user():
    """search parameter value user """
    parameter=input("\n What is the Field you want to search about it: users_email, users_status, users_name,users_online,users_payment_methods, users_regiterd_at , users_credit_card   ?")

    if parameter.lower()=="email":
        #Make validation for email 
        email_pattern="([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        parameter_value=input("Enter the email in the right  format :   ")
        
        if re.search(email_pattern, parameter_value)==None:
            print("Not valid email formate , must be like this formate: name.surname@gmail.com")
            return

        results=my_collection.find({"users_email " : parameter_value})
        results=list(results)

        if len(results)>0:
            for user in results:
                print("\n")
                print(user)
                print("\n")
            print("=" * 40 +"\n" +"=" * 40 )   
        else:
            print(f"This product with this Email : {parameter_value} is not exiset !.")
            print("=" * 40 +"\n" +"=" * 40 )


    elif parameter.lower()=="paymentmethod":
        #Make validation for payment method
        available_methods=["VISA","PayPal","Master"]
        alternative_methods=input("Enter the number of methods you want to add (MAX 3nr,) : ")
        for i in range(int(alternative_methods)):
            paymentmethod=input(f"Give paymentmetod nr{i+1} : ")
            if paymentmethod in available_methods:
                print(f"\nCustomer using {paymentmethod} ")
                
                query = {"users_payment_methods": {"$in": [paymentmethod]}}
                entries=my_collection.find(query)
                for entry in entries:
                    print(entry)
            else:
                print(f"The paymentmethod {paymentmethod} is not in the available method list")


    elif parameter.lower()=="users_online" or parameter.lower()=="users_regiterd_at":
        customer_date=input("\n Enter the Date in right format , the spirate Lis is: Year,Month,Day , Year Month Day or Year-Month-Day : ")
        year=customer_date[:4]
        month=customer_date[5:7]
        day=customer_date[8:]
        new_customer_date=datetime.datetime(int(year), int(month), int(day))
        results=my_collection.find({parameter:new_customer_date})
        results=list(results)
        for res in results:
            print(res)
        print("=" * 40 +"\n" +"=" * 40 )
    else:
        parameter_value=input("Enter the value of the field which you want to search about it : ")
        results=my_collection.find({parameter:parameter_value})
        results=list(results)
        for res in results:
            print(res)
        print("=" * 40 +"\n" +"=" * 40 )


