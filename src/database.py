from pymongo import MongoClient
import os

def connect_to_mongo():
    """
    Establece y retorna una conexión a MongoDB.
    
    Returns:
        MongoClient: Cliente de MongoDB configurado con la URI del entorno.
        
    Raises:
        Exception: Si no se puede establecer la conexión a MongoDB.
    """
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    return client