from utils import raise_exception, is_otp_expire
from sqlalchemy.future import select
from models import User
from ..consts import UserTypeEnum
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID



class UserService:
    """Has methods for user related operations"""
    def __init__(self, db:AsyncSession):
        self.db = db

    async def get_user(
            self, 
            phone_number: int, 
            is_staff: bool = True, 
            is_active: bool = True,
            is_all:bool = False
            )-> User:
        """ 
        fetch user from database according to conditions
        
        Params:
        phone_number: 10 digit phone number
        is_staff: default True, get only staff data, if false then give only customer data
        is_active: default True, give only active members, if false give all data 
        is_all: `True`, to fetch all data 

        Return: user object
        """
        filter = [User.phone_number == phone_number]
        
        # check for staff or all types
        if is_staff and not is_all:
            filter.append(User.user_type != UserTypeEnum.CUSTOMER)
        elif not is_all:
            filter.append(User.user_type == UserTypeEnum.CUSTOMER)
        
        # check for active users
        if is_active:
            filter.append(User.is_active == True)

        result = await self.db.execute(select(User).filter(*filter))

        user = result.scalar_one_or_none()

        return user

   
    async def create_user(self, is_staff: bool,**kwargs)-> User:
        """
        create user in database with given parameters
        params:
        is_staff: True, add staff data. False, add customer data

        Return: new user object
        """
        if is_staff:
            new_user = User(
                name = kwargs.get('name'),
                phone_number = kwargs.get('phone_number'),
                email = kwargs.get('email'),
                user_type = kwargs.get('user_type'),
                tenant_id = kwargs.get('tenant_id'),
                restaurant_id = kwargs.get('restaurant_id'),
                is_active = False
            )
        else:
            new_user = User(
                phone_number = kwargs.get('phone_number'),
                name = kwargs.get('name'),
                is_active = False
            )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user


    async def delete_staff_by_restaurant(self, user_id: UUID)-> User:
        """
        This method delete the user (staff)

        params:
        user_id: UUID of the user

        Output: UUID of the deleted user
        """
        result = await self.db.execute(select(User).filter(User.user_id == user_id))
        user = result.scalar_one_or_none()
        user.restaurant_id = None
        user.tenant_id = None
        user.is_active = False
        self.db.add(user)
        await self.db.commit() 
        return user

    async def otp_verification(self, phone_number: int, otp: int)-> User:
        """
        verifies otp
        
        params:
        phone_number: 10 digit phone number
        otp: Six digit otp

        Return: user object
        """
        result = await self.db.execute(select(User).filter(User.otp==otp))
        user = result.scalar_one_or_none()
        raise_exception(not user or phone_number!=user.phone_number, 400, "Invalid OTP")
        raise_exception(is_otp_expire(user.otp_access_time), 400, "OTP is expired")
        return user
    
    
    async def fetch_role(self, user_id: UUID)-> str:
        """
        Fetch role or user_type of the user

        params:
        user_id : UUID of the user

        Output: role of user
        """
        result = await self.db.execute(select(User.user_type).filter(User.user_id==user_id))
        return result.scalar_one_or_none()