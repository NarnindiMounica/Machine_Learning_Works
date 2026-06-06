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

''' Data Ingestion related constants starts with DATA_INGESTION var name'''

DATA_INGESTION_COLLECTION_NAME:str = "NetworkData"
DATA_INGESTION_DATABASE_NAME:str = "MounicaAI"
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_NAME:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.2


