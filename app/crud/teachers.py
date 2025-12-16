


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


from bson import ObjectId
from datetime import datetime
from app.db.database import db
from app.crud.users import serialize_user


def serialize_teacher(t, user=None):

    return {
        "id": str(t["_id"]),
        "userId": str(t["userId"]),
        "user": serialize_user(user) if user else None,  # attach user if available
        "assignedCourses": [str(c) for c in t.get("assignedCourses", [])],
        "qualifications": t.get("qualifications", []),
        "subjects": t.get("subjects", []),
        "status": t.get("status", "active"),
        "createdAt": t.get("createdAt"),
        "updatedAt": t.get("updatedAt"),
    }


async def create_teacher(user_id: str, tenant_id: str | None = None):
   
    data = {
        "userId": ObjectId(user_id),
        "courses": [],
        "status": "active",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    }
    if tenant_id:
        data["tenantId"] = ObjectId(tenant_id)

    result = await db.teachers.insert_one(data)
    teacher = await db.teachers.find_one({"_id": result.inserted_id})

    # Attach user details if user exists
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    return serialize_teacher(teacher, user)


async def get_teacher_by_user(user_id: str):
    """
    Fetch teacher by user_id along with user details.
    """
    teacher = await db.teachers.find_one({"userId": ObjectId(user_id)})
    if not teacher:
        return None

    user = await db.users.find_one({"_id": ObjectId(user_id)})
    return serialize_teacher(teacher, user)


async def update_teacher_profile(user_id: str, updates: dict):
    """
    Update teacher profile and corresponding user fields.
    """
    teacher_fields = {}
    user_fields = {}

    # ---- teacher fields ----
    for field in ["status", "courses"]:
        if field in updates:
            teacher_fields[field] = updates[field]

    # ---- user fields ----
    for field in ["fullName", "profileImageURL", "contactNo", "country"]:
        if field in updates:
            user_fields[field] = updates[field]

    if teacher_fields:
        teacher_fields["updatedAt"] = datetime.utcnow()
        await db.teachers.update_one(
            {"userId": ObjectId(user_id)}, {"$set": teacher_fields}
        )

    if user_fields:
        user_fields["updatedAt"] = datetime.utcnow()
        await db.users.update_one({"_id": ObjectId(user_id)}, {"$set": user_fields})

    # ---- fetch updated documents ----
    teacher = await db.teachers.find_one({"userId": ObjectId(user_id)})
    user = await db.users.find_one({"_id": ObjectId(user_id)})

    if not teacher or not user:
        return None

    return serialize_teacher(teacher, user)
