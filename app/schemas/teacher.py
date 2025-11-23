from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


class TeacherCreate(BaseModel):
    tenant_id: str
    name: str
    email: EmailStr
    password: str
    profileImageURL: Optional[str] = None
    contactNo: Optional[str] = None
    country: Optional[str] = None

class Teacher(BaseModel):
    id: str
    tenant_id: str
    name: str
    email: EmailStr
    profileImageURL: Optional[str] = None
    assignedCourses: List[str] = []
    status: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        orm_mode = True