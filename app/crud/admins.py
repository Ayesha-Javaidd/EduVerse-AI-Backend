from bson import ObjectId
from datetime import datetime
from app.db.database import db
from app.crud.users import serialize_user


def serialize_admin(a, u):
    return {
        "id": str(a["_id"]),
        "userId": str(a["userId"]),
        "permissions": a.get("permissions", []),
        "status": a.get("status"),
        "createdAt": a.get("createdAt"),
        "updatedAt": a.get("updatedAt"),
        "user": serialize_user(u),
    }


async def get_admin_by_user(user_id: str):
    admin = await db.admins.find_one({"userId": ObjectId(user_id)})
    if not admin:
        return None

    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return None

    return serialize_admin(admin, user)


async def update_admin_profile(user_id: str, updates: dict):
    admin_fields = {}
    user_fields = {}

    # ---- admin fields ----
    for field in ["permissions", "status"]:
        if field in updates:
            admin_fields[field] = updates[field]

    # ---- user fields ----
    for field in ["fullName", "profileImageURL", "contactNo", "country"]:
        if field in updates:
            user_fields[field] = updates[field]

    if admin_fields:
        admin_fields["updatedAt"] = datetime.utcnow()
        await db.admins.update_one(
            {"userId": ObjectId(user_id)}, {"$set": admin_fields}
        )

    if user_fields:
        user_fields["updatedAt"] = datetime.utcnow()
        await db.users.update_one({"_id": ObjectId(user_id)}, {"$set": user_fields})

    return await get_admin_by_user(user_id)
