import os, sys
from networksecurity.exception_details.exception import CustomException
from networksecurity.logging_details.logger import logging

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.constant import training_pipeline
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig, DataTransformationConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation


if __name__=="__main__":
    dataingestionobj= DataIngestion(data_ingestion_config=DataIngestionConfig(training_pipeline_config=TrainingPipelineConfig))
    logging.info("Initiate data ingestion")
    data_ingestion_artifacts=dataingestionobj.initiate_data_ingestion()
    logging.info("completion of data ingestion")
    logging.info("Initiate data validation")
    datavalidationobj=DataValidation(data_ingestion_artifacts=data_ingestion_artifacts, data_validation_config=DataValidationConfig(training_pipeline_config=TrainingPipelineConfig))
    data_validation_artifacts=datavalidationobj.initiate_data_validation()
    logging.info("completion of data validation")
    logging.info("Initiate data transformation")
    datatransformationobj=DataTransformation(data_validation_artifact=data_validation_artifacts, data_transformation_config=DataTransformationConfig(training_pipeline_config=TrainingPipelineConfig))
    print(datatransformationobj.initiate_data_transformation())