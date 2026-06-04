import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

mongodb_url = os.getenv("MONGODB_URL")


print(mongodb_url)
