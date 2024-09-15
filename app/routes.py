# app/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas, models
from .database import get_db

router = APIRouter()

@router.get("/questionnaires/{questionnaire_id}")
def get_questionnaire(questionnaire_id: int, db: Session = Depends(get_db)):
    db_questionnaire = crud.get_questionnaire(db, questionnaire_id=questionnaire_id)
    if db_questionnaire is None:
        raise HTTPException(status_code=404, detail="Questionnaire not found")
    return db_questionnaire

@router.post("/answers/")
def create_answer(answer: schemas.AnswerCreate, db: Session = Depends(get_db)):
    return crud.create_answer(db=db, answer=answer)

@router.get("/users/{user_id}/answers")
def get_answers_for_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_answers_for_user(db=db, user_id=user_id)
