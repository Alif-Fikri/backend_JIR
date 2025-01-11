from pymongo import MongoClient

# Koneksi MongoDB
client = MongoClient("mongodb://localhost:27017/") 
db = client["smartcity"] 
