from pymongo import MongoClient
import os

def connect_to_mongo():
    print(os.getenv('MONGO_URI'))
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    return client