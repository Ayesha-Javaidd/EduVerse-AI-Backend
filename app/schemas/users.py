from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


# ---------- Base ----------

class UserBase(BaseModel):
    fullName: str
    email: EmailStr
    role: str                     # student | teacher | admin | super_admin
    status: str = "active"
    profileImageURL: Optional[str] = None
    contactNo: Optional[str] = None
    country: Optional[str] = None


# ---------- Requests ----------

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    tenantId: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., max_length=72)


# ---------- Responses ----------

class UserResponse(UserBase):
    id: str
    tenantId: Optional[str]
    createdAt: datetime
    updatedAt: datetime
    lastLogin: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }
