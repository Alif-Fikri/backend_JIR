import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_AUTH_DB = os.getenv("MONGO_AUTH_DB")
MONGO_DATABASE = os.getenv("MONGO_DATABASE")

mongo_uri = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?authSource={MONGO_AUTH_DB}"
client = MongoClient(mongo_uri)

db = client[MONGO_DATABASE]
