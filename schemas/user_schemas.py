from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID
from consts import UserTypeEnum

# Base User Schema
class UserBase(BaseModel):
    username: str
    email: EmailStr

# Create User Schema
class UserCreate(UserBase):
    password: str
    role: Optional[UserTypeEnum] = UserTypeEnum.user

# Update User Schema
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserTypeEnum] = None

# User Response Schema
class UserResponse(UserBase):
    user_id: UUID
    role: UserTypeEnum
    created_at: datetime
    
    class Config:
        from_attributes = True

# Login Schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Token Data Schema
class TokenData(BaseModel):
    email: Optional[str] = None 