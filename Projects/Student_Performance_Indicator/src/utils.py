import os, sys
import dill

import numpy as np
import pandas as pd

from src.exception import CustomException
from src.logger import logging

from sklearn.metrics import r2_score


def save_object(filepath, obj):

    try:

        file_dir = os.path.dirname(filepath)
        os.makedirs(file_dir, exist_ok=True)

        with open(filepath, 'wb') as file_obj:
            dill.dump(obj, file_obj )

    except Exception as e:
        raise CustomException(e, sys)  


    def evaluate_models(x_train, x_test, y_train, y_test, models):

        try:
            
            report = {}

            for i in range(len(models)):

                model = list(models.keys())[i]

                model.fit(x_train, y_train)
                logging.info("Model is trained on training data")

                y_train_pred = model.predict(x_train)
                y_test_pred = model.predict(x_test)

                logging.info("Model prediction is done on train and test inputs")

                train_model_score = r2_score(y_train, y_train_pred)
                test_model_score = r2_score(y_test, y_test_pred)

                report[model] = test_model_score

            logging.info("Evaluation is completed, report is prepared") 

            return report

        except Exception as e:
            raise CustomException(e, sys)          