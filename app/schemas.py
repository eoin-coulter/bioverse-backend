# app/schemas.py
from pydantic import BaseModel

class AnswerBase(BaseModel):
    user_id: int
    questionnaire_id: int
    question_id: int
    answer_content: str

class AnswerCreate(AnswerBase):
    pass

class Answer(AnswerBase):
    id: int

    class Config:
        orm_mode = True
