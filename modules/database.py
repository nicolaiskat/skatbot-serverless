import logging
from pymongo import MongoClient
import os

def get_database():
    logging.info('Get dabase')
    uri = os.environ['MONGO_URI']
    client = MongoClient(uri)
    return client[os.environ['CSGOSTATS_DATABASE']]
  
if __name__ == "__main__":   
   dbname = get_database()