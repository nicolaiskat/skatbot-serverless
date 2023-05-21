import logging
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
import os

def get_database():
    uri = os.environ['MONGO_URI']
    client = MongoClient(uri)
    return client[os.environ['CSGOSTATS_DATABASE']]
  
if __name__ == "__main__":   
   dbname = get_database()