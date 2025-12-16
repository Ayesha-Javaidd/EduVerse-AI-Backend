from bson import ObjectId
from datetime import datetime
from app.db.database import db
from app.crud.users import serialize_user


def serialize_superadmin(user_doc):
    return {
        "id": str(user_doc["_id"]),
        "userId": str(user_doc["_id"]),
        "user": serialize_user(user_doc),  # attach user details
        "createdAt": user_doc["createdAt"],
        "updatedAt": user_doc["updatedAt"],
    }


async def get_superadmin_by_user(user_id: str):
    user = await db.users.find_one({"_id": ObjectId(user_id), "role": "super_admin"})
    if not user:
        return None
    return serialize_superadmin(user)


async def update_superadmin(user_id: str, updates: dict):

    user_fields = {}
    for field in ["fullName", "profileImageURL", "contactNo", "country", "status"]:
        if field in updates:
            user_fields[field] = updates[field]

    if user_fields:
        user_fields["updatedAt"] = datetime.utcnow()
        await db.users.update_one(
            {"_id": ObjectId(user_id), "role": "super_admin"}, {"$set": user_fields}
        )

    user = await db.users.find_one({"_id": ObjectId(user_id), "role": "super_admin"})
    if not user:
        return None
    return serialize_superadmin(user)
