import os, sys

from dataclasses import dataclass

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object, evaluate_models 

from sklearn.metrics import r2_score

from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from xgboost import XGBRegressor

@dataclass
class ModelTrainerConfig:

    trained_model_filepath :str = os.path.join("artifacts", "trained_model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_training(self, train_array, test_array):
        try:
            logging.info("Splitting train and test data into input features and targets ")
            x_train, x_test, y_train, y_test = train_array[:,:-1], test_array[:,:-1], train_array[:,-1], test_array[:,-1]


            models = {"Linear Regression": LinearRegression(),
                        "Ridge": Ridge(),
                        "Lasso": Lasso(),
                        "Support Vector Regressor": SVR(),
                        "KNN": KNeighborsRegressor(),
                        "Decision Tree": DecisionTreeRegressor(),
                        "Random Forest": RandomForestRegressor(),
                        "Adaptive Boosting": AdaBoostRegressor(),
                        "XG Boosting": XGBRegressor()}
            

            model_report:dict = evaluate_models(x_train=x_train, x_test=x_test, y_train=y_train, y_test=y_test, models=models)
        except Exception as e:
            raise CustomException(e, sys)
