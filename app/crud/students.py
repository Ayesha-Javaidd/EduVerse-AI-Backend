from bson import ObjectId
from datetime import datetime
from app.db.database import db
from app.crud.users import serialize_user


def serialize_student(s, user):
    return {
        "id": str(s["_id"]),
        "userId": str(s["userId"]),
        "user": serialize_user(user),  #  attach user
        "enrolledCourses": s.get("enrolledCourses", []),
        "completedCourses": s.get("completedCourses", []),
        "status": s.get("status"),
        "createdAt": s.get("createdAt"),
        "updatedAt": s.get("updatedAt"),
    }


async def get_student_by_user(user_id: str):
    student = await db.students.find_one({"userId": ObjectId(user_id)})
    if not student:
        return None

    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return None

    return serialize_student(student, user)


async def create_student(user_id: str):
    data = {
        "userId": ObjectId(user_id),
        "enrolledCourses": [],
        "completedCourses": [],
        "status": "active",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    }
    result = await db.students.insert_one(data)
    student = await db.students.find_one({"_id": result.inserted_id})
    return serialize_student(student)



async def update_student_profile(user_id: str, updates: dict):
    updates["updatedAt"] = datetime.utcnow()
    await db.students.update_one({"userId": ObjectId(user_id)}, {"$set": updates})
    s = await db.students.find_one({"userId": ObjectId(user_id)})
    return serialize_student(s)
