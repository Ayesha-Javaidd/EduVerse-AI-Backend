from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class SuperAdmin(BaseModel):
    id: str
    name: str
    email: EmailStr
    profileImageURL: Optional[str] = None
    platformPermissions: List[str] = []
    createdAt: datetime
    updatedAt: datetime

    class Config:
        orm_mode = True