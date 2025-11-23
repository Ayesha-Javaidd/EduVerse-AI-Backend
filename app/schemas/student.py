from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class Student(BaseModel):
    tenant_id : str
    name : str
    email : EmailStr
    password : str
    profileImage : Optional[str] = None
    contactNo : Optional[str] = None
    country : Optional[str] = None

class Student(BaseModel):
    id: str
    tenant_id: str
    name: str
    email: EmailStr
    profileImageURL: Optional[str] = None
    enrolledCourses: List[str] = []
    complatedCourses: List[str] = []
    contactNo: Optional[str] = None
    country: Optional[str] = None
    status: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime

    class Config:
        orm_mode = True