import os,sys
import numpy as np
import pandas as pd
import pymongo
from typing import List

from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGODB_URL=os.getenv("MONGODB_URL")

from networksecurity.exception_details.exception import CustomException
from networksecurity.logging_details.logger import logging

#Data ingestion config

from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e, sys)
        
    def export_collection_as_dataframe(self):
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name

            self.client_name = pymongo.MongoClient(MONGODB_URL)
            collection = self.client_name[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.to_list():
                df.drop("_id", axis=1, inplace=True)
            df.replace({"na":np.nan})  

            return df  

        except Exception as e:
            raise CustomException(e, sys)
        

    def export_data_into_feature_store(self, dataframe:pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_filepath
            #creating folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, header=True, index=False)
            return dataframe
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def split_data_as_train_test(self, dataframe):
        try:
            train_df, test_df = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Applied train and test split on dataframes")

            logging.info("Exited split_data_as_train_test method of DataIngestion class")

            dir_path = os.path.dirname(self.data_ingestion_config.training_filepath)
            os.makedirs(dir_path, exist_ok=True)

            logging.info("Exporting train and test file path")
            train_df.to_csv(self.data_ingestion_config.training_filepath, index=False, header=True)
            test_df.to_csv(self.data_ingestion_config.testing_filepath, index=False, header=True)

        except Exception as e:
            raise CustomException(e, sys)


    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_collection_as_dataframe()
            dataframe=self.export_data_into_feature_store()
            self.split_data_as_train_test(dataframe=dataframe)
        except Exception as e:
            raise CustomException(e, sys)

