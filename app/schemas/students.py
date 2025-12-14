from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class StudentCreate(BaseModel):
    userId: str


class StudentUpdate(BaseModel):
    status: Optional[str] = None


class StudentResponse(BaseModel):
    id: str
    userId: str
    enrolledCourses: List[str] = []
    completedCourses: List[str] = []
    status: str
    createdAt: datetime
    updatedAt: datetime

    model_config = {
        "from_attributes": True
    }
