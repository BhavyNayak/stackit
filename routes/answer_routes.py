### routes/answer_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.database_helper import get_db
from models import Answer
from routes import answer_routes, question_routes, user_routes
router = APIRouter()
router.include_router(answer_routes.router)
router.include_router(question_routes.router)
router.include_router(user_routes.router)

@router.get("/")
def get_answers(db: Session = Depends(get_db)):
    return db.query(Answer).all()
