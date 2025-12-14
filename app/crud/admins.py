from bson import ObjectId
from datetime import datetime
from app.db.database import db

def serialize_admin(a):
    return {
        "id": str(a["_id"]),
        "userId": str(a["userId"]),
        "profileImageURL": a.get("profileImageURL"),
        "status": a.get("status", "active"),
        "createdAt": a.get("createdAt"),
        "updatedAt": a.get("updatedAt"),
    }


async def get_admin_by_user(user_id: str):
    a = await db.admins.find_one({"userId": ObjectId(user_id)})
    return serialize_admin(a) if a else None


async def update_admin_profile(user_id: str, updates: dict):
    updates["updatedAt"] = datetime.utcnow()
    await db.admins.update_one(
        {"userId": ObjectId(user_id)},
        {"$set": updates}
    )
    a = await db.admins.find_one({"userId": ObjectId(user_id)})
    return serialize_admin(a)
