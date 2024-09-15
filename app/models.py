# app/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from .database import Base

class Questionnaire(Base):
    __tablename__ = "questionnaire_questionnaires"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)

class Question(Base):
    __tablename__ = "questionnaire_questions"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(JSONB, nullable=False)

class QuestionnaireJunction(Base):
    __tablename__ = "questionnaire_junction"

    id = Column(Integer, primary_key=True, index=True)
    questionnaire_id = Column(Integer, ForeignKey("questionnaire_questionnaires.id", ondelete="CASCADE"))
    question_id = Column(Integer, ForeignKey("questionnaire_questions.id", ondelete="CASCADE"))
    priority = Column(Integer, nullable=False)

class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    questionnaire_id = Column(Integer, ForeignKey("questionnaire_questionnaires.id", ondelete="CASCADE"))
    question_id = Column(Integer, ForeignKey("questionnaire_questions.id", ondelete="CASCADE"))
    answer_content = Column(Text, nullable=False)
