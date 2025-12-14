from pydantic import BaseModel
from datetime import datetime


class SuperAdminCreate(BaseModel):
    userId: str


class SuperAdminResponse(BaseModel):
    id: str
    userId: str
    createdAt: datetime

    model_config = {
        "from_attributes": True
    }
