# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas

def get_questionnaire(db: Session, questionnaire_id: int):
    return db.query(models.Questionnaire).filter(models.Questionnaire.id == questionnaire_id).first()

def create_answer(db: Session, answer: schemas.AnswerCreate):
    db_answer = models.Answer(**answer.dict())
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer

def get_answers_for_user(db: Session, user_id: int):
    return db.query(models.Answer).filter(models.Answer.user_id == user_id).all()
