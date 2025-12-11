from bson import ObjectId
from datetime import datetime
from app.db.database import db
from app.utils.security import hash_password, verify_password

def serialize_user(u):
    return {
        "id": str(u["_id"]),
        "fullName": u["fullName"],
        "email": u["email"],
        "profileImageURL": u.get("profileImageURL"),
        "contactNo": u.get("contactNo"),
        "country": u.get("country"),
        "role": u["role"],
        "status": u["status"],
        "tenant_id": str(u["tenant_id"]) if u.get("tenant_id") else None,
        "enrolledCourses": u.get("enrolledCourses", []),
        "completedCourses": u.get("completedCourses", []),
        "createdAt": u["createdAt"],
        "updatedAt": u["updatedAt"],
        "lastLogin": u.get("lastLogin")
    }

# async def get_user_by_email(email: str):
#     return await db.users.find_one({"email": email})

async def get_user_by_email(email: str):
    return await db.users.find_one({"email": email.lower()})


async def create_user(data: dict):
    data["password"] = hash_password(data["password"])
    data["createdAt"] = datetime.utcnow()
    data["updatedAt"] = datetime.utcnow()
    data["lastLogin"] = None
    result = await db.users.insert_one(data)
    new_user = await db.users.find_one({"_id": result.inserted_id})
    return serialize_user(new_user)

# async def verify_user(email: str, password: str):
#     u = await get_user_by_email(email)
#     if not u:
#         return None
#     if not verify_password(password, u["password"]):
#         return None
#     return serialize_user(u)


async def verify_user(email: str, password: str):
    u = await get_user_by_email(email)
    if not u:
        print("User not found:", email)
        return None
    if not verify_password(password, u["password"]):
        print("Password mismatch")
        return None
    return serialize_user(u)


async def update_last_login(user_id: str):
    await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"lastLogin": datetime.utcnow()}}
    )
