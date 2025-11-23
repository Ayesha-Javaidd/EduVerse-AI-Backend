from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class AdminCreate(BaseModel):
    # tenant_id: str
    fullName: str
    orgName: str
    email: EmailStr
    password: str
    profileImageURL: Optional[str] = None
    contactNo: Optional[str] = None
    country: Optional[str] = None

class AdminResponse(BaseModel):
    id: str
    tenant_id: Optional[str] = None
    fullName: str
    orgName: str
    email: EmailStr
    profileImageURL: Optional[str] = None
    permissions: List[str] = []
    status: str
    contactNo: Optional[str] = None
    country: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime

    class Config:
        orm_mode = True
