import os, sys
import numpy as np
import pandas as pd

from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.exception_details.exception import CustomException
from networksecurity.logging_details.logger import logging

from networksecurity.constant import training_pipeline

from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact

from networksecurity.components.data_validation import DataValidation

from networksecurity.utils.main_utils.utils import save_numpy_array_data, save_object

class DataTransformation:
    def __init__(self, data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        self.data_validation_artifact = data_validation_artifact
        self.data_transformation_config = data_transformation_config

    def get_data_transformer_object(self) -> Pipeline:
        try:
            imputer = KNNImputer(**training_pipeline.DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"Initialized knnimputer with params: {training_pipeline.DATA_TRANSFORMATION_IMPUTER_PARAMS}")

            processor: Pipeline = Pipeline([
                ("Knn_Imputer", imputer)
            ])

            return processor
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info("Initiating data transformation")
            train_df = DataValidation.read_data(filepath=self.data_validation_artifact.valid_train_filepath)
            test_df = DataValidation.read_data(filepath=self.data_validation_artifact.valid_test_filepath)

            #training dataframe
            input_feature_train_df = train_df.drop(training_pipeline.TARGET_COLUMN, axis=1)
            target_feature_train_df = train_df[training_pipeline.TARGET_COLUMN].replace(-1, 0)

            #testing dataframe
            input_feature_test_df = test_df.drop(training_pipeline.TARGET_COLUMN, axis=1)
            target_feature_test_df = test_df[training_pipeline.TARGET_COLUMN].replace(-1, 0)

            preprocessor = self.get_data_transformer_object()

            input_feature_train_df = preprocessor.fit_transform(input_feature_train_df)
            input_feature_test_df = preprocessor.transform(input_feature_test_df)

            train_array = np.c_[input_feature_train_df, np.array(target_feature_train_df)]
            test_array = np.c_[input_feature_test_df, np.array(target_feature_test_df)]

            #saving transformed arrays in filepath

            save_numpy_array_data(filepath= self.data_transformation_config.transformed_train_filepath, array=train_array)
            save_numpy_array_data(filepath= self.data_transformation_config.transformed_test_filepath, array=test_array)

            #saving processor_object

            save_object(filepath=self.data_transformation_config.transformed_object_filepath, object=preprocessor)

            #preparing artifact

            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_filepath=self.data_transformation_config.transformed_object_filepath,
                transformed_train_filepath=self.data_transformation_config.transformed_train_filepath,
                transformed_test_filepath=self.data_transformation_config.transformed_test_filepath
            )
            return data_transformation_artifact

        except Exception as e:
            raise CustomException(e, sys)    