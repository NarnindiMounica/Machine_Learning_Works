import os,sys
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp

from networksecurity.exception_details.exception import CustomException
from networksecurity.logging_details.logger import logging


from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.artifact_entity import DataValidationArtifact, DataIngestionArtifact