from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List

class UserBase(BaseModel):
    fullName: str
    email: EmailStr
    profileImageURL: Optional[str] = None
    contactNo: Optional[str] = None
    country: Optional[str] = None
    role: str
    status: str = "active"


class UserCreate(UserBase):
    password: str
    tenant_id: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., max_length=72)



class UserResponse(UserBase):
    id: str
    tenant_id: Optional[str]
    enrolledCourses: List[str] = []
    completedCourses: List[str] = []
    createdAt: datetime
    updatedAt: datetime
    lastLogin: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }
