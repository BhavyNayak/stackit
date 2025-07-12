from pydantic import BaseModel
from typing import Optional, Any, Generic, TypeVar

T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    status: int
    message: str
    data: Optional[T] = None

def create_response(status: int = 200, message: str = "Operation successfully done", data: Any = None):
    """Helper function to create consistent API responses"""
    return APIResponse(status=status, message=message, data=data) 