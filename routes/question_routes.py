

### routes/question_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.database_helper import get_db
from models import Question

router = APIRouter()

@router.get("/")
def get_questions(db: Session = Depends(get_db)):
    return db.query(Question).all()
