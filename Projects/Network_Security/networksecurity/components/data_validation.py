import os,sys
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp

from networksecurity.exception_details.exception import CustomException
from networksecurity.logging_details.logger import logging

from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file


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

    #let's check data drift
    def detect_dataset_drift(self, base_df, current_df, threshold=0.05) ->bool:
        try:
            status=True
            report = {}
            for column in base_df.columns:
                df1 = base_df[column]
                df2 = current_df[column]
                is_same_dist = ks_2samp(df1, df2)
                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else: 
                    is_found = True
                    status = False
            report.update({column: {
                "p_value": float(is_same_dist.pvalue),
                "drift_status": is_found
            }})  
            drift_report_filepath = self.data_validation_config.drift_report_filepath

            #create directory

            dir_name = os.path.dirname(drift_report_filepath)
            os.makedirs(dir_name, exist_ok=True)

            return report
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
                error_message="Train dataframe does not contain all columns.\n"

            test_status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not test_status:
                error_message="Test dataframe does not contain all columns.\n" 

            train_numerical_status = self.validate_number_of_num_columns(dataframe=train_dataframe)
            if not train_numerical_status:
                numerical_error_message="Train dataframe does not contain all numerical columns.\n"  

            test_numerical_status = self.validate_number_of_num_columns(dataframe=test_dataframe)
            if not test_numerical_status:
                numerical_error_message="Test dataframe does not contain all numerical columns.\n"              

        except Exception as e:
            raise CustomException(e, sys)    
      
