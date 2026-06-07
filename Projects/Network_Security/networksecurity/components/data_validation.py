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
