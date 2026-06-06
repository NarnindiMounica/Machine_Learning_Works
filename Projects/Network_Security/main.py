import os, sys
from networksecurity.exception_details.exception import CustomException
from networksecurity.logging_details.logger import logging

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.constant import training_pipeline
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact


if __name__=="__main__":
    dataingestionobj= DataIngestion(data_ingestion_config=DataIngestionConfig(training_pipeline_config=TrainingPipelineConfig))
    print(dataingestionobj.initiate_data_ingestion())