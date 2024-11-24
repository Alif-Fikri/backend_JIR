from database import db
from bson import ObjectId

users_collection = db["users"]

def get_user_by_email(email: str):
    user = users_collection.find_one({"email": email})
    if user:
        user["id"] = str(user["_id"])
        del user["_id"], user["hashed_password"]
    return user
