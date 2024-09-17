# app/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Text,Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from .database import Base


class Question(Base):
    __tablename__ = "questionnaire_questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(JSONB, nullable=False)

class QuestionnaireJunction(Base):
    __tablename__ = "questionnaire_junction"

    id = Column(Integer, primary_key=True, index=True)
    questionnaire_id = Column(Integer, ForeignKey("questionnaire_questionnaires.id", ondelete="CASCADE"))
    question_id = Column(Integer, ForeignKey("questionnaire_questions.id", ondelete="CASCADE"))
    priority = Column(Integer, nullable=False)

    question = relationship("Question")  # Link to the Question model


class Answer(Base):
    __tablename__ = 'answer'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    question_id = Column(Integer, ForeignKey('questionnaire_questions.id'))
    answer = Column(Text, nullable=False)

    question = relationship("Question")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    pword = Column(String)
    is_admin = Column(Boolean)

class Questionnaire(Base):
    __tablename__ = "questionnaire_questionnaires"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
