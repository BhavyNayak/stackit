from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete
from models import User
from consts import UserTypeEnum
from consts import UserTypeEnum as UserRole
from utils.auth_helper import get_password_hash, verify_password
from utils.exception_handler import raise_exception
from schemas.user_schemas import UserCreate, UserUpdate
from typing import List, Optional
from uuid import UUID

class UserService:
    """Service class for user-related database operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID"""
        result = await self.db.execute(select(User).filter(User.user_id == user_id))
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        result = await self.db.execute(select(User).filter(User.email == email))
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        result = await self.db.execute(select(User).filter(User.username == username))
        return result.scalar_one_or_none()

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        result = await self.db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()

    async def create_user(self, user_data: UserCreate) -> User:
        """Create a new user"""
        # Check if email already exists
        existing_user = await self.get_user_by_email(user_data.email)
        raise_exception(existing_user is not None, "Email already registered")
        
        # Check if username already exists
        existing_username = await self.get_user_by_username(user_data.username)
        raise_exception(existing_username is not None, "Username already taken")
        
        # Hash the password
        hashed_password = get_password_hash(user_data.password)
        
        # Create new user
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password=hashed_password,
            # role=user_data.role
            role= UserRole(user_data.role)
        )
        
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user

    async def update_user(self, user_id: UUID, user_data: UserUpdate) -> Optional[User]:
        """Update user information"""
        user = await self.get_user_by_id(user_id)
        raise_exception(user is None, "User not found")
        
        # Check if new email already exists (if email is being updated)
        if user_data.email and user_data.email != user.email:
            existing_user = await self.get_user_by_email(user_data.email)
            raise_exception(existing_user is not None, "Email already registered")
        
        # Check if new username already exists (if username is being updated)
        if user_data.username and user_data.username != user.username:
            existing_username = await self.get_user_by_username(user_data.username)
            raise_exception(existing_username is not None, "Username already taken")
        
        # Update fields
        update_data = {}
        if user_data.username is not None:
            update_data["username"] = user_data.username
        if user_data.email is not None:
            update_data["email"] = user_data.email
        if user_data.role is not None:
            update_data["role"] = user_data.role
        
        if update_data:
            await self.db.execute(
                update(User).where(User.user_id == user_id).values(**update_data)
            )
            await self.db.commit()
            await self.db.refresh(user)
        
        return user

    async def delete_user(self, user_id: UUID) -> bool:
        """Delete a user"""
        user = await self.get_user_by_id(user_id)
        raise_exception(user is None, "User not found")
        
        await self.db.execute(delete(User).where(User.user_id == user_id))
        await self.db.commit()
        return True

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = await self.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    async def get_users_by_role(self, role: UserTypeEnum, skip: int = 0, limit: int = 100) -> List[User]:
        """Get users by role"""
        result = await self.db.execute(
            select(User).filter(User.role == role).offset(skip).limit(limit)
        )
        return result.scalars().all()