from src.components import data_ingestion
from src.components import data_transformation
from src.components import model_training

if __name__ == "__main__":
    obj = data_ingestion.DataIngestion()
    train_path, test_path = obj.initiate_data_ingestion()
    data_transformation_obj = data_transformation.DataTransformation()
    train_array, test_array, preprocessor_filepath=data_transformation_obj.initiate_data_transformation(train_path, test_path)
    model_trainer_obj = model_training.ModelTrainer()
    r2_value=model_trainer_obj.initiate_model_training(train_array, test_array)
    print(f"R2_Square Value of Best Model: {r2_value}")

