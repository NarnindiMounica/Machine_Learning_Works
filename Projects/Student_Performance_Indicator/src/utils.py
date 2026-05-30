import os, sys
import dill

import numpy as np
import pandas as pd

from src.exception import CustomException


def save_object(filepath, obj):

    try:

        file_dir = os.path.dirname(filepath)
        os.makedirs(file_dir, exist_ok=True)

        with open(filepath, 'wb') as file_obj:
            dill.dump(obj, file_obj )

    except Exception as e:
        raise CustomException(e, sys)        