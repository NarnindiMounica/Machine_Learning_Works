import os,sys
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp

from networksecurity.exception_details.exception import CustomException
from networksecurity.logging_details.logger import logging

from networksecurity.utils.main_utils.utils import read_yaml_file


from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.artifact_entity import DataValidationArtifact, DataIngestionArtifact

from networksecurity.constant.training_pipeline import SCHEMA_FILEPATH

class DataValidation:
    def __init__(self, data_ingestion_artifacts:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        
        try:
            self.data_ingestion_artifacts=data_ingestion_artifacts
            self.data_validation_config=data_validation_config
            self._schema_config=read_yaml_file(filepath=SCHEMA_FILEPATH)
        except Exception as e:
            raise CustomException(e, sys)  
        

    @staticmethod
    def read_data(filepath:str)->pd.DataFrame:
        try:
            return pd.DataFrame(filepath)
        except Exception as e:
            raise CustomException(e, sys)  

    def validate_number_of_columns(self, dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self._schema_config['columns'])
            logging.info(f"Required number of columns : {number_of_columns}")
            logging.info(f"DataFrame has columns : {len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                return True
            else:
                return False

        except Exception as e:
            raise CustomException(e, sys)    
        
    def validate_number_of_num_columns(self, dataframe:pd.DataFrame)->bool:
        try:
            number_of_num_columns = len(self._schema_config['numerical columns'])
            logging.info(f"Number of numerical columns: {number_of_num_columns}")
            number_of_num_columns_in_dataframe = len([column for column in dataframe.columns if dataframe[column].dtype!="str"])

            if number_of_num_columns==number_of_num_columns_in_dataframe:
                return True
            else:
                return False
        except Exception as e:
            raise CustomException(e, sys)    


    def initiate_data_valiation(self)->DataValidationArtifact:
        try:
            train_filepath = self.data_ingestion_artifacts.train_filepath
            test_filepath = self.data_ingestion_artifacts.test_filepath

            #read the data from train and test filepaths

            train_dataframe = DataValidation.read_data(filepath=train_filepath)
            test_dataframe = DataValidation.read_data(filepath=test_filepath)

            train_status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not train_status:
                error_message=f"Train dataframe does not contain all columns.\n"

            test_status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not test_status:
                error_message=f"Test dataframe does not contain all columns.\n"        

        except Exception as e:
            raise CustomException(e, sys)    
      
