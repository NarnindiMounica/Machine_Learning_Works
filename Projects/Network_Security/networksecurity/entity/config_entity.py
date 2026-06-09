from datetime import datetime
import os,sys

from networksecurity.constant import training_pipeline

print(training_pipeline.PIPELINE_NAME)
print(training_pipeline.ARTIFACT_DIR)

class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now()):
        timestamp = timestamp.strftime("%Y-%m-%D %H-%M-%S")
        self.pipelinename = training_pipeline.PIPELINE_NAME
        self.artifactname = training_pipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifactname, timestamp)
        self.timestamp:str = timestamp


class DataIngestionConfig:
    def __init__(self, training_pipeline_config):
        self.training_pipeline_config=TrainingPipelineConfig()
        self.data_ingestion_dir:str=os.path.join(self.training_pipeline_config.artifact_dir, training_pipeline.DATA_INGESTION_DIR_NAME)
        self.feature_store_filepath:str=os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_FEATURE_STORE_NAME) 
        self.training_filepath:str=os.path.join(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TRAIN_FILENAME)
        self.testing_filepath:str=os.path.join(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TEST_FILENAME)
        self.train_test_split_ratio:float=training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name:str=training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name:str=training_pipeline.DATA_INGESTION_DATABASE_NAME  

class DataValidationConfig:
    def __init__(self, training_pipeline_config):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.data_validation_dir:str=os.path.join(self.training_pipeline_config.artifact_dir, training_pipeline.DATA_VALIDATION_DIR_NAME)
        self.valid_data_dir:str=os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_VALID_DIR) 
        self.invalid_data_dir:str=os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_INVALID_DIR) 
        self.valid_train_filepath:str=os.path.join(self.valid_data_dir, training_pipeline.TRAIN_FILENAME)
        self.valid_test_filepath:str=os.path.join(self.valid_data_dir, training_pipeline.TEST_FILENAME)
        self.invalid_train_filepath:str=os.path.join(self.invalid_data_dir, training_pipeline.TRAIN_FILENAME)
        self.invalid_test_filepath:str=os.path.join(self.invalid_data_dir, training_pipeline.TEST_FILENAME)
        self.drift_report_filepath:str=os.path.join(self.data_validation_dir, 
                                               training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
                                               training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILENAME)

class DataTransformationConfig:
    def __init__(self, training_pipeline_config):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.data_transformation_dir:str = os.path.join(self.training_pipeline_config.artifact_dir, training_pipeline.DATA_TRANSFORMATION_DIR_NAME)
        self.transformed_train_filepath:str = os.path.join(self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                           training_pipeline.TRAIN_FILENAME.replace(".csv", ".npy"))
        self.transformed_test_filepath:str = os.path.join(self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                           training_pipeline.TEST_FILENAME.replace(".csv", ".npy"))
        self.transformed_object_filepath:str = os.path.join(self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR, training_pipeline.PREPROCESSING_OBJECT_FILENAME)


class ModelTrainerConfig:
    def __init__(self, training_pipeline_config):
        self.training_pipeline_config=TrainingPipelineConfig()
        self.model_trainer_dir_name = os.path.join(self.training_pipeline_config.artifact_dir, training_pipeline.MODEL_TRAINER_DIR_NAME)
        self.trained_model_filepath = os.path.join(self.model_trainer_dir_name, training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR,
                                                   training_pipeline.S)
        self.expected_accuracy = training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        self.overfitting_underfitting_threshold = training_pipeline.MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD

