from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class TeacherCreate(BaseModel):
    userId: str
    qualifications: List[str] = []
    subjects: List[str] = []


class TeacherUpdate(BaseModel):
    qualifications: Optional[List[str]] = None
    subjects: Optional[List[str]] = None
    status: Optional[str] = None


class TeacherResponse(BaseModel):
    id: str
    userId: str
    assignedCourses: List[str] = []
    qualifications: List[str]
    subjects: List[str]
    status: str
    createdAt: datetime
    updatedAt: datetime

    model_config = {
        "from_attributes": True
    }
