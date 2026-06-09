import os, sys
import numpy as np
import pandas as pd

'''Defining common constant variables for training pipeline'''

TARGET_COLUMN="Result"
PIPELINE_NAME:str="NetworkSecurity"
ARTIFACT_DIR:str="Artifacts"
TRAIN_FILENAME:str="Traindata.csv"
TEST_FILENAME:str="Testdata.csv"
FILENAME:str="phisingData.csv"
SCHEMA_FILEPATH:str=os.path.join("data_schema", "schema.yml")
PREPROCESSING_OBJECT_FILENAME:str="preprocessor.pkl"


''' Data Ingestion related constants starts with DATA_INGESTION var name'''

DATA_INGESTION_COLLECTION_NAME:str = "NetworkData"
DATA_INGESTION_DATABASE_NAME:str = "MounicaAI"
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_NAME:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.2

''' Data Validation related constants starts with DATA_VALIDATION var name'''

DATA_VALIDATION_DIR_NAME:str = "data_validation"
DATA_VALIDATION_VALID_DIR:str = "validated"
DATA_VALIDATION_INVALID_DIR:str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILENAME:str = "report.yml"

''' Data Transformation related constants starts with DATA_TRANSFORMATION var name'''

DATA_TRANSFORMATION_DIR_NAME:str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str = "transformed_object" 

#knn imputer to replace nan values
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform"
}

''' Model trainer related constants starts with MODEL_TRAINER var name'''

MODEL_TRAINER_DIR_NAME:str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR:str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME:str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE:float = 0.6
MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD:float = 0.05



