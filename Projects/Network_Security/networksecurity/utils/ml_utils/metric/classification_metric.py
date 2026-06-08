import os, sys

from networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from networksecurity.exception_details.exception import CustomException
from networksecurity.logging_details.logger import logging

from sklearn.metrics import f1_score, precision_score, recall_score

def get_classification_score(y_true, y_pred)->ClassificationMetricArtifact:

    try:
        f1_value = f1_score(y_true, y_pred)
        precision_value = precision_score(y_true, y_pred)
        recall_value = recall_score(y_true, y_pred)
        classification_metric_artifact = ClassificationMetricArtifact(f1_score=f1_value, precision_score=precision_value, recall_score=recall_value)
        return classification_metric_artifact
    except Exception as e:
        raise CustomException(e, sys)