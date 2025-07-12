from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete
from models import Answer, User, Question
from utils.exception_handler import raise_exception
from schemas.answer_schemas import AnswerCreate, AnswerUpdate
from typing import List, Optional
from uuid import UUID

class AnswerService:
    """Service class for answer-related database operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_answer_by_id(self, answer_id: UUID) -> Optional[Answer]:
        """Get answer by ID"""
        result = await self.db.execute(select(Answer).filter(Answer.answer_id == answer_id))
        return result.scalar_one_or_none()

    async def get_answers_by_question(self, question_id: UUID, skip: int = 0, limit: int = 100) -> List[Answer]:
        """Get all answers for a specific question"""
        result = await self.db.execute(
            select(Answer)
            .filter(Answer.question_id == question_id)
            .order_by(Answer.created_at.asc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_answers_by_user(self, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Answer]:
        """Get all answers by a specific user"""
        result = await self.db.execute(
            select(Answer)
            .filter(Answer.user_id == user_id)
            .order_by(Answer.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def create_answer(self, answer_data: AnswerCreate, user_id: UUID) -> Answer:
        """Create a new answer"""
        # Check if question exists
        question_result = await self.db.execute(
            select(Question).filter(Question.question_id == answer_data.question_id)
        )
        question = question_result.scalar_one_or_none()
        raise_exception(question is None, "Question not found")
        
        new_answer = Answer(
            question_id=answer_data.question_id,
            user_id=user_id,
            content=answer_data.content
        )
        
        self.db.add(new_answer)
        await self.db.commit()
        await self.db.refresh(new_answer)
        return new_answer

    async def update_answer(self, answer_id: UUID, answer_data: AnswerUpdate, user_id: UUID) -> Optional[Answer]:
        """Update answer (only by the author)"""
        answer = await self.get_answer_by_id(answer_id)
        raise_exception(answer is None, "Answer not found")
        raise_exception(answer.user_id != user_id, "You can only update your own answers")
        
        # Update fields
        update_data = {}
        if answer_data.content is not None:
            update_data["content"] = answer_data.content
        if answer_data.is_accepted is not None:
            # Only question author can mark answer as accepted
            question_result = await self.db.execute(
                select(Question).filter(Question.question_id == answer.question_id)
            )
            question = question_result.scalar_one_or_none()
            raise_exception(
                question.user_id != user_id and answer_data.is_accepted,
                "Only question author can mark answers as accepted"
            )
            update_data["is_accepted"] = answer_data.is_accepted
        
        if update_data:
            await self.db.execute(
                update(Answer).where(Answer.answer_id == answer_id).values(**update_data)
            )
            await self.db.commit()
            await self.db.refresh(answer)
        
        return answer

    async def delete_answer(self, answer_id: UUID, user_id: UUID) -> bool:
        """Delete an answer (only by the author)"""
        answer = await self.get_answer_by_id(answer_id)
        raise_exception(answer is None, "Answer not found")
        raise_exception(answer.user_id != user_id, "You can only delete your own answers")
        
        await self.db.execute(delete(Answer).where(Answer.answer_id == answer_id))
        await self.db.commit()
        return True

    async def get_answer_with_author(self, answer_id: UUID) -> Optional[dict]:
        """Get answer with author information"""
        result = await self.db.execute(
            select(Answer, User.username)
            .join(User, Answer.user_id == User.user_id)
            .filter(Answer.answer_id == answer_id)
        )
        row = result.first()
        if row:
            answer, author_username = row
            return {
                "answer": answer,
                "author_username": author_username
            }
        return None

    async def get_accepted_answer_for_question(self, question_id: UUID) -> Optional[Answer]:
        """Get the accepted answer for a question"""
        result = await self.db.execute(
            select(Answer).filter(
                Answer.question_id == question_id,
                Answer.is_accepted == True
            )
        )
        return result.scalar_one_or_none()

    async def mark_answer_as_accepted(self, answer_id: UUID, user_id: UUID) -> Optional[Answer]:
        """Mark an answer as accepted (only by question author)"""
        answer = await self.get_answer_by_id(answer_id)
        raise_exception(answer is None, "Answer not found")
        
        # Check if user is the question author
        question_result = await self.db.execute(
            select(Question).filter(Question.question_id == answer.question_id)
        )
        question = question_result.scalar_one_or_none()
        raise_exception(question.user_id != user_id, "Only question author can mark answers as accepted")
        
        # Unmark any previously accepted answers for this question
        await self.db.execute(
            update(Answer)
            .where(Answer.question_id == answer.question_id)
            .values(is_accepted=False)
        )
        
        # Mark this answer as accepted
        await self.db.execute(
            update(Answer)
            .where(Answer.answer_id == answer_id)
            .values(is_accepted=True)
        )
        
        await self.db.commit()
        await self.db.refresh(answer)
        return answer 