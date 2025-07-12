from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from utils.database_helper import get_async_db
from utils.auth_helper import get_current_active_user
from database.question_service import QuestionService
from models import User
from schemas.question_schemas import QuestionCreate, QuestionUpdate, QuestionResponse, QuestionWithAuthor
from schemas.response_schemas import create_response

router = APIRouter()

@router.post("/")
async def create_question(
    question_data: QuestionCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new question"""
    question_service = QuestionService(db)
    question = await question_service.create_question(question_data, current_user.user_id)
    
    return create_response(
        status=201,
        message="Question created successfully",
        data=QuestionResponse.from_orm(question)
    )

@router.get("/")
async def get_all_questions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None, description="Search term for questions"),
    db: AsyncSession = Depends(get_async_db)
):
    """Get all questions with optional search"""
    question_service = QuestionService(db)
    
    if search:
        questions = await question_service.search_questions(search, skip=skip, limit=limit)
    else:
        questions = await question_service.get_all_questions(skip=skip, limit=limit)
    
    return create_response(
        data=[QuestionResponse.from_orm(question) for question in questions]
    )

@router.get("/my-questions")
async def get_my_questions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get current user's questions"""
    question_service = QuestionService(db)
    questions = await question_service.get_questions_by_user(
        current_user.user_id, skip=skip, limit=limit
    )
    
    return create_response(
        data=[QuestionResponse.from_orm(question) for question in questions]
    )

@router.get("/{question_id}")
async def get_question_by_id(
    question_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    """Get question by ID with author information"""
    question_service = QuestionService(db)
    question_with_author = await question_service.get_question_with_author(question_id)
    
    if not question_with_author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    # Create response with author information
    question_data = QuestionResponse.from_orm(question_with_author["question"])
    response_data = QuestionWithAuthor(
        **question_data.dict(),
        author_username=question_with_author["author_username"]
    )
    
    return create_response(
        data=response_data
    )

@router.put("/{question_id}")
async def update_question(
    question_id: UUID,
    question_data: QuestionUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update question (only by the author)"""
    question_service = QuestionService(db)
    question = await question_service.update_question(
        question_id, question_data, current_user.user_id
    )
    
    return create_response(
        message="Question updated successfully",
        data=QuestionResponse.from_orm(question)
    )

@router.delete("/{question_id}")
async def delete_question(
    question_id: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete question (only by the author)"""
    question_service = QuestionService(db)
    await question_service.delete_question(question_id, current_user.user_id)
    
    return create_response(
        message="Question deleted successfully"
    )

@router.get("/user/{user_id}")
async def get_questions_by_user_id(
    user_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_async_db)
):
    """Get questions by user ID"""
    question_service = QuestionService(db)
    questions = await question_service.get_questions_by_user(user_id, skip=skip, limit=limit)
    
    return create_response(
        data=[QuestionResponse.from_orm(question) for question in questions]
    )
