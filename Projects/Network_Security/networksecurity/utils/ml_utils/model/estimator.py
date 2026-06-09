import os, sys

from networksecurity.exception_details.exception import CustomException
from networksecurity.logging_details.logger import logging

from networksecurity.constant.training_pipeline import MODEL_TRAINER_TRAINED_MODEL_DIR, MODEL_TRAINER_TRAINED_MODEL_NAME

class NetworkModel:
    def __init__(self, preprocessor, model):
        self.preprocessor = preprocessor
        self.model = model

    def predict(self, x):
        try:
            x_transformed = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transformed)
            return y_hat
        except Exception as e:
            raise CustomException(e, sys)    