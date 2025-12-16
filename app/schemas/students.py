from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.users import UserResponse


class StudentCreate(BaseModel):
    userId: str


class StudentUpdate(BaseModel):
    status: Optional[str] = None


class StudentResponse(BaseModel):
    id: str
    userId: str
    user: UserResponse  # NESTED USER
    enrolledCourses: List[str] = []
    completedCourses: List[str] = []
    status: str
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}
