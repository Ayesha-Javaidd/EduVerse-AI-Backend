from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from pydantic import ConfigDict

# ---------- Base ----------

class UserBase(BaseModel):
    fullName: str
    email: EmailStr
    role: str                     # student | teacher | admin | super_admin
    status: str = "active"
    profileImageURL: Optional[str] = None
    contactNo: Optional[str] = None
    country: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# ---------- Requests ----------

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    tenantId: Optional[str] = None

    model_config = ConfigDict(validate_assignment=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., max_length=72)

    model_config = ConfigDict(validate_assignment=True)


# ---------- Responses ----------

class UserResponse(UserBase):
    id: str
    tenantId: Optional[str]
    createdAt: datetime
    updatedAt: datetime
    lastLogin: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
