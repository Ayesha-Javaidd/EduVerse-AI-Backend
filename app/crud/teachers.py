from app.db.database import db
from bson import ObjectId
from datetime import datetime

def serialize_teacher(t):
    return {
        "id": str(t["_id"]),
        "userId": str(t["userId"]),
        "assignedCourses": [str(c) for c in t.get("assignedCourses", [])],
        "qualifications": t.get("qualifications", []),
        "subjects": t.get("subjects", []),
        "status": t.get("status", "active"),
        "createdAt": t.get("createdAt"),
        "updatedAt": t.get("updatedAt"),
    }


async def get_teacher_by_user(user_id: str):
    t = await db.teachers.find_one({"userId": ObjectId(user_id)})
    return serialize_teacher(t) if t else None


async def update_teacher_profile(user_id: str, updates: dict):
    updates["updatedAt"] = datetime.utcnow()
    await db.teachers.update_one(
        {"userId": ObjectId(user_id)},
        {"$set": updates}
    )
    t = await db.teachers.find_one({"userId": ObjectId(user_id)})
    return serialize_teacher(t)
