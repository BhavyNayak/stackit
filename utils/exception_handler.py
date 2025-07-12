from fastapi import HTTPException, status

def raise_exception(condition: bool, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
    """
    Raises HTTPException if condition is True.

    Args:
        condition (bool): If True, raise the exception.
        message (str): Message to return in the exception.
        status_code (int): HTTP status code (default 400).
    """
    if condition:
        raise HTTPException(
            status_code=status_code,
            detail=message
        )
