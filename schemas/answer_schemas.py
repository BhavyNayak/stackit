from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

# Base Answer Schema
class AnswerBase(BaseModel):
    content: str

# Create Answer Schema
class AnswerCreate(AnswerBase):
    question_id: UUID

# Update Answer Schema
class AnswerUpdate(BaseModel):
    content: Optional[str] = None
    is_accepted: Optional[bool] = None

# Answer Response Schema
class AnswerResponse(AnswerBase):
    answer_id: UUID
    question_id: UUID
    user_id: UUID
    is_accepted: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Answer with Author Schema
class AnswerWithAuthor(AnswerResponse):
    author_username: str 