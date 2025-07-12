from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from utils.database_helper import get_async_db
from utils.auth_helper import get_current_active_user
from database.answer_service import AnswerService
from models import User
from schemas.answer_schemas import AnswerCreate, AnswerUpdate, AnswerResponse, AnswerWithAuthor
from schemas.response_schemas import create_response

router = APIRouter()

@router.post("/", response_model=dict)
async def create_answer(
    answer_data: AnswerCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new answer"""
    answer_service = AnswerService(db)
    answer = await answer_service.create_answer(answer_data, current_user.user_id)
    
    return create_response(
        status=201,
        message="Answer created successfully",
        data=AnswerResponse.from_orm(answer)
    )

@router.get("/question/{question_id}", response_model=dict)
async def get_answers_by_question(
    question_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_async_db)
):
    """Get all answers for a specific question"""
    answer_service = AnswerService(db)
    answers = await answer_service.get_answers_by_question(question_id, skip=skip, limit=limit)
    
    return create_response(
        data=[AnswerResponse.from_orm(answer) for answer in answers]
    )

@router.get("/my-answers", response_model=dict)
async def get_my_answers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get current user's answers"""
    answer_service = AnswerService(db)
    answers = await answer_service.get_answers_by_user(
        current_user.user_id, skip=skip, limit=limit
    )
    
    return create_response(
        data=[AnswerResponse.from_orm(answer) for answer in answers]
    )

@router.get("/{answer_id}", response_model=dict)
async def get_answer_by_id(
    answer_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """Get answer by ID with author information"""
    answer_service = AnswerService(db)
    answer_with_author = await answer_service.get_answer_with_author(answer_id)
    
    if not answer_with_author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found"
        )
    
    # Create response with author information
    answer_data = AnswerResponse.from_orm(answer_with_author["answer"])
    response_data = AnswerWithAuthor(
        **answer_data.dict(),
        author_username=answer_with_author["author_username"]
    )
    
    return create_response(
        data=response_data
    )

@router.put("/{answer_id}", response_model=dict)
async def update_answer(
    answer_id: UUID,
    answer_data: AnswerUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update answer (only by the author)"""
    answer_service = AnswerService(db)
    answer = await answer_service.update_answer(
        answer_id, answer_data, current_user.user_id
    )
    
    return create_response(
        message="Answer updated successfully",
        data=AnswerResponse.from_orm(answer)
    )

@router.delete("/{answer_id}", response_model=dict)
async def delete_answer(
    answer_id: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete answer (only by the author)"""
    answer_service = AnswerService(db)
    await answer_service.delete_answer(answer_id, current_user.user_id)
    
    return create_response(
        message="Answer deleted successfully"
    )

@router.post("/{answer_id}/accept", response_model=dict)
async def accept_answer(
    answer_id: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user)
):
    """Mark an answer as accepted (only by question author)"""
    answer_service = AnswerService(db)
    answer = await answer_service.mark_answer_as_accepted(answer_id, current_user.user_id)
    
    return create_response(
        message="Answer marked as accepted successfully",
        data=AnswerResponse.from_orm(answer)
    )

@router.get("/user/{user_id}", response_model=dict)
async def get_answers_by_user_id(
    user_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_async_db)
):
    """Get answers by user ID"""
    answer_service = AnswerService(db)
    answers = await answer_service.get_answers_by_user(user_id, skip=skip, limit=limit)
    
    return create_response(
        data=[AnswerResponse.from_orm(answer) for answer in answers]
    )

@router.get("/question/{question_id}/accepted", response_model=dict)
async def get_accepted_answer_for_question(
    question_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """Get the accepted answer for a question"""
    answer_service = AnswerService(db)
    answer = await answer_service.get_accepted_answer_for_question(question_id)
    
    if not answer:
        return create_response(
            message="No accepted answer found for this question",
            data=None
        )
    
    return create_response(
        data=AnswerResponse.from_orm(answer)
    )
