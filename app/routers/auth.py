from datetime import datetime
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.crud import students, users
from app.schemas.users import UserCreate
from app.auth.auth_service import register_user, login_user
from app.db.database import db

router = APIRouter(prefix="/auth", tags=["Authentication"])


# # Signup endpoint (JSON)
# @router.post("/signup")
# async def signup(payload: UserCreate):
#     # user = await register_user(payload.dict())
#     # if payload.role == "student":
#     #     await db.students.insert_one(
#     #         {
#     #             "userId": ObjectId(user["_id"]),
#     #             "enrolledCourses": [],
#     #             "completedCourses": [],
#     #             "status": "active",
#     #             "createdAt": datetime.utcnow(),
#     #             "updatedAt": datetime.utcnow(),
#     #         }
#     #     )
#     # return {"message": "User registered successfully", "user": user}

#     user_data = payload.dict()
#     user = await db.users.insert_one(user_data)

#     if payload.role == "student":
#         await db.students.insert_one(
#             {
#                 "userId": user.inserted_id,
#                 "enrolledCourses": [],
#                 "completedCourses": [],
#                 "status": "active",
#                 "createdAt": datetime.utcnow(),
#                 "updatedAt": datetime.utcnow(),
#             }
#         )

#     user_data["_id"] = user.inserted_id
#     return {"message": "User registered successfully", "user": user_data}


@router.post("/signup")
async def signup(payload: UserCreate):
    user = await users.create_user(payload.dict())

    # Create student profile if role is student
    if payload.role == "student":
        await students.create_student(user["id"])

    return {"message": "User registered successfully", "user": user}


# OAuth2 login endpoint (form-data)
@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # form_data.username is your email
    result = await login_user(form_data.username, form_data.password)

    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": result["access_token"],
        "token_type": "bearer",
        "user": result["user"],
    }
