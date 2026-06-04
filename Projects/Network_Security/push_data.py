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

    def csv_to_json_converter(self):
        try:
            data = pd.read_csv(self.filepath)
            data.reset_index(drop=True, inplace=True)
            records=list(json.loads((data.T.to_json()).values()))
            return records
        except Exception as e:
            raise CustomException(e, sys)
        
    def insert_data_mongodb(self, )    

        