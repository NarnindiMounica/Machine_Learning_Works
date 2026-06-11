import os, sys, mlflow

from networksecurity.exception_details.exception import CustomException
from networksecurity.logging_details.logger import logging

from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ClassificationMetricArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import save_object, load_object, save_numpy_array_data, load_numpy_array_data, evaluate_models
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier

import dagshub
dagshub.init(repo_owner='NarnindiMounica', repo_name='Machine_Learning_Works', mlflow=True)

class ModelTrainer:
    def __init__(self, model_trainer_config:ModelTrainerConfig, data_transformation_artifact:DataTransformationArtifact):
        self.model_trainer_config = model_trainer_config
        self.data_transformation_artifact = data_transformation_artifact

    def track_mlflow(self, best_model, classification_metrics:ClassificationMetricArtifact):
        try:
            with mlflow.start_run():
                f1_score=classification_metrics.f1_score
                precision_score=classification_metrics.precision_score
                recall_score=classification_metrics.recall_score

                mlflow.log_metric("f1_score", f1_score)
                mlflow.log_metric("precision_score", precision_score)
                mlflow.log_metric("recall_score", recall_score)

                mlflow.sklearn.log_model(best_model, "model")

        except Exception as e:
            raise CustomException(e, sys)

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

            #to get best model score from dict
            best_model_score = max(sorted(model_report.values()))
            #to get best model name
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            #to get best model
            best_model = models[best_model_name]
            y_train_pred = best_model.predict(x_train)
            y_test_pred = best_model.predict(x_test)

            classification_train_metric=get_classification_score(y_true=y_train, y_pred=y_train_pred)
            classification_test_metric=get_classification_score(y_true=y_test, y_pred=y_test_pred)

            #tracking the mlflow
            self.track_mlflow(best_model, classification_train_metric)
            self.track_mlflow(best_model, classification_test_metric)

            preprocessor = load_object(filepath=self.data_transformation_artifact.transformed_object_filepath)

            model_filepath = os.path.dirname(self.model_trainer_config.trained_model_filepath)

            NetworkModel(preprocessor=preprocessor, model=best_model)
            save_object(filepath=model_filepath, obj=NetworkModel)

            #model pusher implementation
            logging.info("saving objects in final_model folder")
            save_object(filepath="final_model/model.pkl", obj=best_model)
            save_object(filepath="final_model/preprocessor.pkl", obj=preprocessor)

            

            model_trainer_artifact = ModelTrainerArtifact(trained_model_filepath=model_filepath, train_metrics_artifact=classification_train_metric, test_metrics_artifact=classification_test_metric)
        
            return model_trainer_artifact
        
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
            
            model_trainer_artifact = self.train_model(x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test)
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e, sys)

