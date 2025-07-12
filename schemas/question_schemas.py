from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID

# Base Question Schema
class QuestionBase(BaseModel):
    title: str
    description: str

# Create Question Schema
class QuestionCreate(QuestionBase):
    pass

# Update Question Schema
class QuestionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

# Question Response Schema
class QuestionResponse(QuestionBase):
    question_id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Question with Author Schema
class QuestionWithAuthor(QuestionResponse):
    author_username: str 