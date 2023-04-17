import pymongo
from pymongo import MongoClient
import configuration
import pprint

printer=pprint.PrettyPrinter()

def find_10_Men_product(): 
    product_collection=configuration.getDBconnection("product")
    products=product_collection.find({"gender" : "Men"}).limit(10)
    
    for prod in products:
         printer.pprint(prod)
        #print("yes")   


def find_10_vinter_women_product():
    product_collection=configuration.getDBconnection("product")
    products=product_collection.find({"gender" : "Women", "season" : "Winter"}).limit(10)

    for prod in products:
        printer.pprint(prod)

def find_10_orderby_year():
    product_collection=configuration.getDBconnection("product")
    products=product_collection.find().limit(10).sort("year")

    for prod in products:
        printer.pprint(prod)

def find_10_index_subcategori():
    product_collection=configuration.getDBconnection("product")
    product_collection.create_index("subCategory")
    products=product_collection.find({"subCategory" : "Topwear"}).limit(10)

    for prod in products:
        printer.pprint(prod)

def find_10_link_http():
    product_collection=configuration.getDBconnection("product")
    products=product_collection.find({}).limit(10)

    for prod in products:
        link=prod["Link"]
        index=link.index(":")
        Link_part1=link[:index]
        Link_part2=link[index:]
        Link_part1="https"
        new_link=Link_part1+Link_part2
        product_collection.update_one({"_id":prod["_id"]},{"$set":{"Link":new_link}})
            
# def collection__cheap__prods():
#     product_collection=configration.getDBconnection("product")
#     products=product_collection.find({"price":{"$gte" : 50}}).limit(10)

#     cheap__prods=product_collection.insert_many(products)
# collection__cheap__prods()