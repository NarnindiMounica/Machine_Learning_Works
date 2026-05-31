from src.components import data_ingestion
from src.components import data_transformation


if __name__ == "__main__":
    obj = data_ingestion.DataIngestion()
    train_path, test_path = obj.initiate_data_ingestion()
    data_transformation_obj = data_transformation.DataTransformation()
    data_transformation_obj.initiate_data_transformation(train_path, test_path)

    
