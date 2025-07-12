### routes/answer_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.database_helper import get_db
from models import Answer

router = APIRouter()

@router.get("/")
def get_answers(db: Session = Depends(get_db)):
    return db.query(Answer).all()
