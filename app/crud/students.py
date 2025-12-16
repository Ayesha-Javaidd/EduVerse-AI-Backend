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

    # Fetch the user document
    user = await db.users.find_one({"_id": ObjectId(user_id)})

    return serialize_student(student, user)


async def update_student_profile(user_id: str, updates: dict):
    student_fields = {}
    user_fields = {}

    # ---- student fields ----
    for field in ["status", "enrolledCourses", "completedCourses"]:
        if field in updates:
            student_fields[field] = updates[field]

    # ---- user fields ----
    for field in ["fullName", "profileImageURL", "contactNo", "country"]:
        if field in updates:
            user_fields[field] = updates[field]

    if student_fields:
        student_fields["updatedAt"] = datetime.utcnow()
        await db.students.update_one(
            {"userId": ObjectId(user_id)}, {"$set": student_fields}
        )

    if user_fields:
        user_fields["updatedAt"] = datetime.utcnow()
        await db.users.update_one({"_id": ObjectId(user_id)}, {"$set": user_fields})

    # ---- fetch updated documents ----
    student = await db.students.find_one({"userId": ObjectId(user_id)})
    user = await db.users.find_one({"_id": ObjectId(user_id)})

    if not student or not user:
        return None

    return serialize_student(student, user)
