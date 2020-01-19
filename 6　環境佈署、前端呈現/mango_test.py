from pymongo import MongoClient
from bson.objectid import ObjectId


# def mongoClient(coursor):
#connection
conn = MongoClient('mongodb://10.120.38.27:15000/')
db = conn.teach_data
collection = db.eyes

#test if connection success
collection.stats

coursor = collection.find_one({})
print(coursor)