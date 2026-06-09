import os, sys

from networksecurity.exception_details.exception import CustomException
from networksecurity.logging_details.logger import logging

from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ClassificationMetricArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import save_object, save_numpy_array_data, load_numpy_array_data
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score


class ModelTrainer:
    def __init__(self, model_trainer_config:ModelTrainerConfig, data_transformation_artifact:DataTransformationArtifact):
        self.model_trainer_config = model_trainer_config
        self.data_transformation_artifact = data_transformation_artifact

    def train_model(self, x_train, y_train):
        try:
            
        except Exception as e:
            raise CustomException(e, sys)    

    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_path = self.data_transformation_artifact.transformed_train_filepath
            test_path = self.data_transformation_artifact.transformed_test_filepath

            train_array = load_numpy_array_data(filepath=train_path)
            test_array = load_numpy_array_data(filepath=test_path)

            x_train = train_array[:, :-1]
            x_test = test_array[:, :-1]
            y_train = train_array[:, -1]
            y_test = test_array[:, -1]
            
            model = self.train_model(x_train, y_train)
            model_trainer_artifact = ModelTrainerArtifact(trained_model_filepath=, train_metrics_artifact=, test_metrics_artifact=)
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e, sys)

