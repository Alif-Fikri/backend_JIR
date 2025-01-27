from database import db
from bson import ObjectId

users_collection = db["users"]

def get_user_by_email(email: str):
    user = users_collection.find_one({"email": email})
    if user:
        user["id"] = str(user["_id"])
        del user["_id"], user["hashed_password"]
    return user

def delete_user_by_email(email: str):
    result = users_collection.delete_one({"email": email})
    return result.deleted_count > 0

def update_user_password(email: str, new_password: str):
    result = users_collection.update_one(
        {"email": email},
        {"$set": {"hashed_password": new_password}}
    )
    return result.modified_count > 0