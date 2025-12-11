from fastapi import APIRouter, HTTPException
from app.schemas.users import UserCreate, UserLogin
from app.auth.auth_service import register_user, login_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup")
async def signup(payload: UserCreate):
    user = await register_user(payload.dict())
    return {"message": "User registered successfully", "user": user}

@router.post("/login")
async def login(payload: UserLogin):
    result = await login_user(payload.email, payload.password)
    return result
