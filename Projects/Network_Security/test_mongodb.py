import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

mongodb_url = os.getenv("MONGODB_URL")

# Create a new client and connect to the server
client = MongoClient(mongodb_url)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
