from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    username:str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(BaseModel):
    id: str = Field(..., alias="_id")
    username: str
    email: str

    class Config:
        # Allow the use of the alias
        populate_by_name = True
        # Any extra fields (like password) will be ignored automatically
        extra = "ignore"

class UserLogin(UserBase):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None