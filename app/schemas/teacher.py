from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class TeacherCreate(BaseModel):
    # tenant_id: str
    name: str
    email: EmailStr
    status:  Optional[str] = None
    password: str
    profileImageURL: Optional[str] = None
    contactNo: Optional[str] = None
    country: Optional[str] = None


class TeacherResponse(BaseModel):
    id: str
    tenant_id: Optional[str] = None
    name: str
    email: EmailStr
    profileImageURL: Optional[str] = None
    assignedCourses: List[str] = []
    status: str
    contactNo: Optional[str] = None
    country: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime

    class Config:
        orm_mode = True
