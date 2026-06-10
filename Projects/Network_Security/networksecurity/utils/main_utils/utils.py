import os, sys, yaml, pickle, dill
import numpy as np
import pandas as pd

from networksecurity.exception_details.exception import CustomException
from networksecurity.logging_details.logger import logging

from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

def read_yaml_file(filepath:str)->dict:
    try:
        with open(filepath, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise CustomException(e,sys)
    

def write_yaml_file(filepath:str, content:object, replace:bool=False)->None:
    try:
        if replace:
            if os.path.exists(filepath):
                os.remove(filepath)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)        
        with open(filepath, 'w') as yaml_obj:
            yaml.safe_dump(content, yaml_obj)
    except Exception as e:
        raise CustomException(e, sys) 


def save_numpy_array_data(filepath:str, array:np.array):
    try:
        dir_name = os.path.dirname(filepath)
        os.makedirs(dir_name, exist_ok=True)
        with open(filepath, 'wb') as file_obj:
            np.save(file_obj, array)

    except Exception as e:
        raise CustomException(e, sys)


def save_object(filepath:str, obj:object):
    try:
        logging.info("Entered the save_object function from utils folder")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Exiting from save_object function from utils folder")    
    
    except Exception as e:
        raise CustomException(e, sys)
    
def load_object(filepath:str)->object:
    try:
        if not os.path.exists(filepath):
            raise Exception(f"The file {filepath} does not exist")
        with open (filepath, "rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)
    

def load_numpy_array_data(filepath:str)->np.array:
    try:
        if not os.path.exists(filepath):
            raise Exception(f"The file {filepath} does not exist")
        with open(filepath, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)


def evaluate_models(x_train, y_train, x_test, y_test, models, params):
    try:
        report = {}
        for i in range(len(list(models))):
            model_name = list(models.keys())[i]
            model = models[list(models.keys())[i]]
            param = params[list(params.keys())[i]]

            grid_cv = GridSearchCV(estimator=model, param_grid=param, cv=3)
            grid_cv.fit(x_train, y_train)

            model.set_params(**grid_cv.best_params_)
            model.fit(x_train, y_train)

            y_train_pred = model.predict(x_train)
            y_test_pred = model.predict(x_test)

            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            report[model_name]=test_model_score

            return report
        
    except Exception as e:
        raise CustomException(e, sys)        

    
