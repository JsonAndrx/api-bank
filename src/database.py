from pymongo import MongoClient
import os

def connect_to_mongo():
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    return client