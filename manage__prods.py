import pymongo
from pymongo import MongoClient
import configuration
import pprint
import modify_prods
from bson import ObjectId


my_collection=configuration.getDBconnection("product")

class Product():
    def __init__(self,gender,masterCategory,subCategory,articleType,baseColour,season,year,usage,productDisplayName,price ):
        self.qualites={"gender":gender,"masterCategory":masterCategory,"subCategory":subCategory,"articleType":articleType,"baseColour":baseColour,
                       "season":season,"year":year,"usage":usage,"productDisplayName":productDisplayName,"price":price}
        #self.qualites={"gender":gender[0],"masterCategory":masterCategory[0],"subCategory":subCategory[0],"articleType":articleType[0],"baseColour":baseColour[0],
        #               "season":season[0],"year":year[0],"usage":usage[0],"productDisplayName":productDisplayName[0],"price":price[0]}

def add_product():
    """Add a anew product"""
    gender=input("\n What is the gender?")
    masterCategory=input("\n What is the masterCategory?")
    subCategory=input("\n What is the subCategory?")
    articleType=input("\n What is the articleType?")
    baseColour=input("\n What is the baseColour?")
    season=input("\n What is the season?")
    year=input("\n What is the year?")
    usage=input("\n What is the usage?")
    productDisplayName=input("\n What is the productDisplayName?")
    price=input("\n What is the price?")

    product=Product(gender,masterCategory,subCategory,articleType,baseColour,season,year,usage,productDisplayName,price )
    newProduct=product.qualites
    # print(newProduct)
    my_collection.insert_one(newProduct)
    
def show_categories_product():
    """Show the different products catergories"""
    products=my_collection.find({})
    master__catergories=[]
    sub_categories=[]
    # master_cate=my_collection.distinct('masterCategory')

    for entry in products:
        if not entry["masterCategory"] in master__catergories:
            master__catergories.append(entry["masterCategory"])
        if not entry["subCategory"] in sub_categories:
            sub_categories.append(entry["subCategory"])

    print(f"Master categories are:\n {master__catergories}")
    print("=" * 40 +"\n" +"=" * 40 )
    print(f"Sub  categories are:\n {sub_categories}")
    print("=" * 40 +"\n" +"=" * 40 )

def modify_product():
    """Modify selected product"""
    product_id=input("Enter the id of product:")
    try :
        product_id=ObjectId(product_id)
    except:
        print("=" * 40 +"\n" +"=" * 40 )
        print(f'{product_id} is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string')
        return
    print("\n\n")
    sub_menu={
                "d":modify_prods.modify_master_category,
                "e":modify_prods.delete_sub_product,
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
        # if callable(value):
        if  next_action!="q":
            sub_menu[next_action](ObjectId(product_id))
        else:
            return

def Set_an_extra_category_value():
    """Set an extra category + value for all products in a category"""
    category_name=input("\n Which category products do you want to modify (Year)? : ")
    value_name=input("\n Which maximum value do  the products have in the category ? :")

    myquery = { category_name:{ "$lte":int(value_name)  } }
    newvalues = { "$set": { "old_products": "True" } }
    my_collection.update_many(myquery, newvalues)
 
def search_parameter_value_product():
    """search parameter value product """
    parameter=input("\n What is the Field you want to filter?")
    value=input("\n What is the value you want to find?")

    products=my_collection.find({f"{parameter}":f"{value}"},{"_id":0,"gender":1,"masterCategory":1,"subCategory":1,"articleType":1,"baseColour":1}).limit(5)

    for entry in products:
        print(f"your choice is {parameter}=>{entry} ")
        print(f"The Search Result is {entry[parameter]}. ")
    print("=" * 40 +"\n" +"=" * 40 )

def delete_product():
    """Clear products list"""
    message_user="Are you want to clear all the products?(yes\no)"
    if message_user=="yes":
        my_collection.drop()

def show__products():
    """MY PRODUCTS LIST"""
    print("=" * 40 +"\n" +"=" * 40 )
    print(show__products.__doc__)
    print("=" * 40 +"\n" +"=" * 40 )

    collection__doc=my_collection.find({}).limit(10)
    
    for prod in collection__doc:
        print(prod)


    main_menu_list={"a":add_product,
                "m":modify_product,
                "s":show_categories_product,
                "c":delete_product,
                "mc":Set_an_extra_category_value,
                "v":search_parameter_value_product,
                "q":"Quite"
                }
    
    action=""
    while action !="q":
        if prod:
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

            
    