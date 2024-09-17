# app/schemas.py
from pydantic import BaseModel
from typing import Union, List, Optional

class Answer(BaseModel):
    question_id: int
    answer: Union[str, List[str]]  

class AnswerRes(BaseModel):
    user_id: int
    questionnaire_id: int
    answers: List[Answer] 

class AnswerCreate(BaseModel):
    pass


    class Config:
        orm_mode = True



# Define a Pydantic schema for returning user data
class UserBase(BaseModel):
    username: str
    pword: str

class UserCreate(UserBase):
    is_admin: Optional[bool] = False 


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True  # This tells Pydantic to convert SQLAlchemy objects to Pydantic models


class QuestionnaireResponse(BaseModel):
    id: int
    title: str


class AnswerSubmit(BaseModel):
    question_id: int
    answer: Union[str, List[str]]
    

class AnswerSubmission(BaseModel):
    user_id: int
    answers: Union[str, List[str]]  


     