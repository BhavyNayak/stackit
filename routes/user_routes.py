from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from utils.database_helper import get_async_db
from utils.auth_helper import get_current_active_user, create_access_token
from database.users import UserService
from models import User
from schemas.user_schemas import UserCreate, UserUpdate, UserResponse, UserLogin, Token
from schemas.response_schemas import create_response

router = APIRouter()

@router.post("/register", response_model=dict)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """Register a new user"""
    user_service = UserService(db)
    user = await user_service.create_user(user_data)
    
    return create_response(
        status=201,
        message="User registered successfully",
        data=UserResponse.from_orm(user)
    )

@router.post("/login", response_model=dict)
async def login_user(
    user_credentials: UserLogin,
    db: AsyncSession = Depends(get_async_db)
):
    """Login user and return JWT token"""
    user_service = UserService(db)
    user = await user_service.authenticate_user(
        user_credentials.email, 
        user_credentials.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(data={"sub": user.email})
    
    return create_response(
        message="Login successful",
        data=Token(access_token=access_token, token_type="bearer")
    )

@router.get("/me", response_model=dict)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user information"""
    return create_response(
        data=UserResponse.from_orm(current_user)
    )

@router.get("/", response_model=dict)
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all users (admin only)"""
    user_service = UserService(db)
    users = await user_service.get_all_users(skip=skip, limit=limit)
    
    return create_response(
        data=[UserResponse.from_orm(user) for user in users]
    )

@router.get("/{user_id}", response_model=dict)
async def get_user_by_id(
    user_id: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get user by ID"""
    user_service = UserService(db)
    user = await user_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return create_response(
        data=UserResponse.from_orm(user)
    )

@router.put("/{user_id}", response_model=dict)
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update user (only own profile or admin)"""
    # Check if user is updating their own profile or is admin
    if current_user.user_id != user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own profile"
        )
    
    user_service = UserService(db)
    user = await user_service.update_user(user_id, user_data)
    
    return create_response(
        message="User updated successfully",
        data=UserResponse.from_orm(user)
    )

@router.delete("/{user_id}", response_model=dict)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete user (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete users"
        )
    
    user_service = UserService(db)
    await user_service.delete_user(user_id)
    
    return create_response(
        message="User deleted successfully"
    )
