from pydantic import BaseModel
from typing import List
from datetime import datetime


class AdminCreate(BaseModel):
    userId: str
    permissions: List[str] = []


class AdminUpdate(BaseModel):
    permissions: List[str]


class AdminResponse(BaseModel):
    id: str
    userId: str
    permissions: List[str]
    status: str
    createdAt: datetime

    model_config = {
        "from_attributes": True
    }
