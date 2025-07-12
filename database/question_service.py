from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete
from models import Question, User
from utils.exception_handler import raise_exception
from schemas.question_schemas import QuestionCreate, QuestionUpdate
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class QuestionService:
    """Service class for question-related database operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_question_by_id(self, question_id: UUID) -> Optional[Question]:
        """Get question by ID"""
        result = await self.db.execute(select(Question).filter(Question.question_id == question_id))
        return result.scalar_one_or_none()

    async def get_all_questions(self, skip: int = 0, limit: int = 100) -> List[Question]:
        """Get all questions with pagination"""
        result = await self.db.execute(
            select(Question).order_by(Question.created_at.desc()).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def get_questions_by_user(self, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Question]:
        """Get questions by user ID"""
        result = await self.db.execute(
            select(Question)
            .filter(Question.user_id == user_id)
            .order_by(Question.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def create_question(self, question_data: QuestionCreate, user_id: UUID) -> Question:
        """Create a new question"""
        new_question = Question(
            user_id=user_id,
            title=question_data.title,
            description=question_data.description
        )
        
        self.db.add(new_question)
        await self.db.commit()
        await self.db.refresh(new_question)
        return new_question

    async def update_question(self, question_id: UUID, question_data: QuestionUpdate, user_id: UUID) -> Optional[Question]:
        """Update question (only by the author)"""
        question = await self.get_question_by_id(question_id)
        raise_exception(question is None, "Question not found")
        raise_exception(question.user_id != user_id, "You can only update your own questions")
        
        # Update fields
        update_data = {}
        if question_data.title is not None:
            update_data["title"] = question_data.title
        if question_data.description is not None:
            update_data["description"] = question_data.description
        
        if update_data:
            update_data["updated_at"] = datetime.utcnow()
            await self.db.execute(
                update(Question).where(Question.question_id == question_id).values(**update_data)
            )
            await self.db.commit()
            await self.db.refresh(question)
        
        return question

    async def delete_question(self, question_id: UUID, user_id: UUID) -> bool:
        """Delete a question (only by the author)"""
        question = await self.get_question_by_id(question_id)
        raise_exception(question is None, "Question not found")
        raise_exception(question.user_id != user_id, "You can only delete your own questions")
        
        await self.db.execute(delete(Question).where(Question.question_id == question_id))
        await self.db.commit()
        return True

    async def get_question_with_author(self, question_id: UUID) -> Optional[dict]:
        """Get question with author information"""
        result = await self.db.execute(
            select(Question, User.username)
            .join(User, Question.user_id == User.user_id)
            .filter(Question.question_id == question_id)
        )
        row = result.first()
        if row:
            question, author_username = row
            return {
                "question": question,
                "author_username": author_username
            }
        return None

    async def search_questions(self, search_term: str, skip: int = 0, limit: int = 100) -> List[Question]:
        """Search questions by title or description"""
        result = await self.db.execute(
            select(Question)
            .filter(
                (Question.title.ilike(f"%{search_term}%")) |
                (Question.description.ilike(f"%{search_term}%"))
            )
            .order_by(Question.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all() 