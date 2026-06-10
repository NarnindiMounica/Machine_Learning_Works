import os, sys

from networksecurity.exception_details.exception import CustomException
from networksecurity.logging_details.logger import logging

from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ClassificationMetricArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import save_object, save_numpy_array_data, load_numpy_array_data, evaluate_models
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier

class ModelTrainer:
    def __init__(self, model_trainer_config:ModelTrainerConfig, data_transformation_artifact:DataTransformationArtifact):
        self.model_trainer_config = model_trainer_config
        self.data_transformation_artifact = data_transformation_artifact

    def train_model(self, x_train, y_train, x_test, y_test):
        try:
            models = {
                "Random_Forest":RandomForestClassifier(verbose=True),
                "KNN": KNeighborsClassifier(),
                "Decision_Tree":DecisionTreeClassifier(),
                "Logistic_Regression": LogisticRegression(verbose=True),
                "AdaBoost":AdaBoostClassifier(),
                "GradientBoost":GradientBoostingClassifier(verbose=True)
                }
            
            params = {
                "Random_Forest":{
                    "n_estimators":[8,16,32,64,128,156],
                    "criterion":['gini', 'entropy'],
                    "max_features":['sqrt', 'log2', None]
                },

                "Decision_Tree":{
                    "criterion":['gini', 'entropy'],
                    "splitter":['best', 'random'],
                    "max_features":['sqrt', 'log2']
                },
                "Logistic_Regression":{},
                "KNN":{"n_neighbors":[5,6,7,8]},
                "AdaBoost":{
                    "learning_rate":[.1, .01, .05, .001],
                    "n_estimators": [8,16,32,64,128,156],
                },
                "GradientBoost":{
                    "loss":['log_loss', 'exponential'],
                    "learning_rate":[.1, .01, .05, .001],
                    "subsample":[0.6, 0.7, 0.75, 0.8, 0.85, 0.9],
                    "n_estimators": [8,16,32,64,128,156],
                    "criterion":['squared_error', 'friedman_mse'],
                    "max_features":['auto', 'sqrt', 'log2']
                }
            }

            model_report:dict = evaluate_models(x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test, models=models, params=params)
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

