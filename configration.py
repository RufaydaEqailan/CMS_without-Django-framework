import pymongo
from pymongo import MongoClient

def getDBconnection(collection_name):
    cluster=MongoClient("mongodb+srv://rufayda:Select123@clusterstor.pzj5idm.mongodb.net/?retryWrites=true&w=majority")
    db=cluster["Bo__training"]
    collection=db[f"{collection_name}"]
    return collection
    