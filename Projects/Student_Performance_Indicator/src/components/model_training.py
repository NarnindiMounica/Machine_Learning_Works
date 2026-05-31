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
            
            params = {"Linear Regression": {},
                      "Ridge": {"alpha": [0.1, 0.01, 0.001, 1], "solver": [ 'sag', 'saga', 'lbfgs', 'auto']},
                      "Lasso": {"alpha": [0.1, 0.01, 0.001, 1]},
                      "Support Vector Regressor": {"kernel": ['linear,' 'poly', 'rbf', 'sigmoid'], "C": [1.0, 0.1, 10, 0.01]},
                      "KNN": {"n_neighbors": [5, 4, 6, 7, 3]},
                      "Decision Tree": {"criterion": ['squared_error', 'poisson'], "max_features":['auto', 'sqrt', 'log2'], "max_depth": [4,5,6]},
                      "Random Forest": {"n_estimators": [100, 150, 200], "criterion": ['squared_error', 'poisson'], "max_depth": [4,5,6]},
                      "Adaptive Boosting": {"n_estimators": [50, 70, 90], "loss":['linear', 'square']},
                      "XG Boosting": {}
                      }
            
            

            model_report = evaluate_models(x_train=x_train, x_test=x_test, y_train=y_train, y_test=y_test, models=models, params=params)
        
            #to get best modelname and modelscore from report
            best_model_score = max(model_report.values()) 

            rev_report = {v:k for k, v in model_report.items()}

            best_model_name = rev_report.get(max(rev_report))

            best_model_obj = models[best_model_name]

            if best_model_score <=0.6:
                raise CustomException("No best model found")
            
            logging.info("Best model with max score is found")

            save_object(filepath=self.model_trainer_config.trained_model_filepath,
                        obj=best_model_obj)
            
            predicted = best_model_obj.predict(x_test)

            r2_square = r2_score(y_test, predicted)

            return r2_square

        except Exception as e:
            raise CustomException(e, sys)
