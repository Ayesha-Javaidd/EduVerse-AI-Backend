from datetime import datetime
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.crud import admins, students, teachers, users
from app.schemas.users import UserCreate
from app.auth.auth_service import register_user, login_user
from app.db.database import db

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup")
async def signup(payload: UserCreate):

    # Admin MUST have tenant
    if payload.role == "admin" and not payload.tenantId:
        raise HTTPException(
            status_code=400, detail="tenantId is required for admin accounts"
        )

    # Prevent public creation of super_admin
    if payload.role == "super_admin":
        raise HTTPException(
            status_code=403, detail="Super admin cannot be created via signup"
        )

    user = await users.create_user(payload.dict())

    if payload.role == "student":
        await students.create_student(user["id"])

    elif payload.role == "teacher":
        await teachers.create_teacher(user["id"])

    elif payload.role == "admin":
        await admins.create_admin(user["id"])

    return {"message": "User registered successfully", "user": user}


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):

    result = await login_user(form_data.username, form_data.password)

    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": result["access_token"],
        "token_type": "bearer",
        "user": result["user"],
    }
