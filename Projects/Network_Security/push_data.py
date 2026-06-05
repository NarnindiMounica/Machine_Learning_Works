import os, sys,json, certifi
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import pymongo

from networksecurity.exception_details.exception import CustomException
from networksecurity.logging_details.logger import logging

load_dotenv()
ca=certifi.where()

mongodb_url = os.getenv("MONGODB_URL")

class NetworkDataExtract:
    def __init__(self, filepath):
        self.filepath = filepath
        self.collection = "NetworkData"
        self.Database = "MounicaAI"
        
    def csv_to_json_converter(self):
        try:
            data = pd.read_csv(self.filepath)
            data.reset_index(drop=True, inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise CustomException(e, sys)
        
    def insert_data_mongodb(self, records):
        try:
            self.mongo_client = pymongo.MongoClient(mongodb_url)
            self.Database = self.mongo_client[self.Database]
            self.collection = self.Database[self.collection]
            self.collection.insert_many(records)
            return len(records)
        except Exception as e:
            raise CustomException(e, sys)
        

if __name__=="__main__":

    network_data_extract_obj = NetworkDataExtract(filepath="network_data\\phisingData.csv")
    records=network_data_extract_obj.csv_to_json_converter()
    print(records)
    print(network_data_extract_obj.insert_data_mongodb(records=records))
    




        