import os, sys
import pandas as pd
import numpy as np

from src.exception import CustomException
from src.logger import logging

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from dataclasses import dataclass

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    
    preprocessor_filepath : str = os.path.join("artifacts", "preprocessor.pkl")

class DataTransformation:

    def __init__(self):

        self.data_transformation_config = DataTransformationConfig() 

    def get_data_transformation_object(self):

        try:
            df = pd.read_csv("D:\\Machine_Learning_Works\\Projects\\Student_Performance_Indicator\\dataset\\stud.csv")

            target_column = "math_score"
            num_columns = [col for col in df.columns if (col != "math_score" and df[col].dtype != "str")]
            cat_columns = [col for col in df.columns if (col != "math_score" and df[col].dtype == "str")]

            logging.info("Separated numerical and categorical columns")

            num_pipeline = Pipeline(
                steps=[
                    ("Imputer", SimpleImputer(strategy="median")),
                    ("Standard_Scaler", StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ("Imputer", SimpleImputer(strategy="most_frequent")),
                    ("OneHot_Encoder", OneHotEncoder(drop="first"))
                ]
            )

            logging.info("Numerical and categorical pipelines are prepared")

            preprocessor = ColumnTransformer(
                [
                    ("numerical_pipeline", num_pipeline, num_columns),
                    ("categorical_pipeline", cat_pipeline, cat_columns)
                ]
            )

            logging.info("Preprocessor is ready to transform data")

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)   



    def initiate_data_transformation(self, train_path, test_path):

        try:
            train_dataframe = pd.read_csv(train_path)
            test_dataframe = pd.read_csv(test_path)

            logging.info("Reading train and test dataframes is completed")

            preprocessor_obj = self.get_data_transformation_object()

            target_col = 'math_score'

            x_train_df = train_dataframe.drop(target_col, axis=1)
            y_train = train_dataframe[target_col]
            x_test_df = test_dataframe.drop(target_col, axis=1)
            y_test = test_dataframe[target_col]

            x_train_preprocessed = preprocessor_obj.fit_transform(x_train_df)
            x_test_preprocessed = preprocessor_obj.transform(x_test_df)

            train_arr = np.c_[x_train_preprocessed, np.array(y_train)]
            test_arr = np.c_[x_test_preprocessed, np.array(y_test)]

            logging.info("Input features in train and test dataframes are preprocessed")

            logging.info("Saving preprocessing object")

            save_object(
                filepath = self.data_transformation_config.preprocessor_filepath,
                obj = preprocessor_obj
            )

            logging.info("Data Transformation is completed")

            return (train_arr,
                    test_arr, 
                    self.data_transformation_config.preprocessor_filepath)
        
        except Exception as e:
            raise CustomException(e, sys)
