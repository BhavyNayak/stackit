### models.py
from sqlalchemy import Column, String, DateTime, Enum, Boolean, Text, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from utils.database_helper import Base
from consts import UserTypeEnum as UserRole

class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.user)
    created_at = Column(DateTime, default=datetime.utcnow)

    questions = relationship("Question", back_populates="author")
    answers = relationship("Answer", back_populates="author")

class Question(Base):
    __tablename__ = "questions"

    question_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)

    author = relationship("User", back_populates="questions")
    answers = relationship("Answer", back_populates="question")

class Answer(Base):
    __tablename__ = "answers"

    answer_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.question_id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    is_accepted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    question = relationship("Question", back_populates="answers")
    author = relationship("User", back_populates="answers")

