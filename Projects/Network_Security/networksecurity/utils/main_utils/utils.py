import os, sys, yaml, pickle, dill
import numpy as np
import pandas as pd

from networksecurity.exception_details.exception import CustomException
from networksecurity.logging_details.logger import logging

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
    
