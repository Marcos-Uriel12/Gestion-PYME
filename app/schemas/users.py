from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class tokenResponse(BaseModel):
    access_token: str
    token_type: str

class tokenData(BaseModel):
    email: Optional[str] = None