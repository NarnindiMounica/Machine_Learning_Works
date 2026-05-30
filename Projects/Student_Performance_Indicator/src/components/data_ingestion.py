import os, sys
import pandas as pd

from src.exception import CustomException
from src.logger import logging

from dataclasses import dataclass

from sklearn.model_selection import train_test_split

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join("artifacts", "train_data.csv")
    test_data_path: str = os.path.join("artifacts", "test_data.csv")
    raw_data_path: str = os.path.join("artifacts", "raw_data.csv")

class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):

        try:
            logging.info("Data ingestion has started")

            dataframe = pd.read_csv("D:\\Machine_Learning_Works\\Projects\\Student_Performance_Indicator\\dataset\\stud.csv")

            logging.info("Read the dataset as dataframe")

            os.makedirs(os.path.dirname(self.data_ingestion_config.raw_data_path), exist_ok=True)
            dataframe.to_csv(self.data_ingestion_config.raw_data_path)

            logging.info("Raw data is moved to raw_data.csv file")

            #train and test data
            train_dataframe, test_dataframe = train_test_split(dataframe, test_size=0.2, random_state=42)

            train_dataframe.to_csv(self.data_ingestion_config.train_data_path)
            test_dataframe.to_csv(self.data_ingestion_config.test_data_path)

            logging.info("Train and Test data is moved to train_data.csv and test_data.csv files")

            logging.info("Data ingestion is completed")

            return (self.data_ingestion_config.train_data_path,
                    self.data_ingestion_config.test_data_path)
        
        except Exception as e:
            raise CustomException(e, sys)
        

     
