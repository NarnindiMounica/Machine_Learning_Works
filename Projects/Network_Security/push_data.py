import os, sys,json, certifi
from dotenv import load_dotenv
import pandas as pd
import numpy as np


load_dotenv()
ca=certifi.where()

mongodb_url = os.getenv("MONGODB_URL")