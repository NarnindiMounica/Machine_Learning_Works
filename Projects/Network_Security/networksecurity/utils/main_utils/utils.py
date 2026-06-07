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
    
