from pymongo import MongoClient

# Koneksi MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Pastikan URL sesuai dengan pengaturan MongoDB Anda
db = client["smartcity"]  # Nama database yang Anda buat di MongoDB Compass
