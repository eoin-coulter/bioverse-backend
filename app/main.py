# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from .database import engine,get_db
from . import models, schemas  
from .routes import router
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session  
from typing import List



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create database tables if they don't exist
models.Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(router)

# For debugging purposes
@app.get("/")
def read_root():
    return {"message": "Welcome to the questionnaire API!"}

# Signup endpoint
@app.post("/signup/")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    new_user = models.User(username=user.username, pword=user.pword,is_admin=user.is_admin) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}

# Login endpoint
@app.post("/login/")
def login(user: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or db_user.pword != user.pword:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    return {
        "message": "Login successful",
        "user": {
            "id": db_user.id,
            "username": db_user.username,
            "is_admin": db_user.is_admin,
        },
    }
@app.get("/questionnaires/")
def get_all_questionnaires(db: Session = Depends(get_db)):
    # Query all questionnaires from the database
    questionnaires = db.query(models.Questionnaire).all()
    return questionnaires

@app.get("/questionnaire/{questionnaire_id}")
def get_questionnaire(questionnaire_id: int, db: Session = Depends(get_db)):
    questionnaire = db.query(models.Questionnaire).filter(models.Questionnaire.id == questionnaire_id).first()
    
    if not questionnaire:
        raise HTTPException(status_code=404, detail="Questionnaire not found")

    # Join the QuestionnaireJunction and Question table to fetch questions, ordered by priority
    questions = db.query(models.Question).join(
        models.QuestionnaireJunction, models.QuestionnaireJunction.question_id == models.Question.id
    ).filter(
        models.QuestionnaireJunction.questionnaire_id == questionnaire_id
    ).order_by(
        models.QuestionnaireJunction.priority
    ).all()

    if not questions:
        raise HTTPException(status_code=404, detail="No questions found for this questionnaire")
    
    # Construct the response with ordered questions
    response = {
        "id": questionnaire.id,
        "title": questionnaire.title,
        "questions": [{"id": q.id, "data": q.question} for q in questions]  # Access the question data directly
    }

    return response


@app.get("/previous-answers/{user_id}/{questionnaire_id}")
def get_previous_answers(user_id: int, questionnaire_id: int, db: Session = Depends(get_db)):
    # Fetch the user's previous answers for the specific questionnaire
    previous_answers = db.query(models.Answer).join(
        models.QuestionnaireJunction, models.Answer.question_id == models.QuestionnaireJunction.question_id
    ).join(
        models.Question, models.Answer.question_id == models.Question.id
    ).filter(
        models.Answer.user_id == user_id,  # Filter by user_id
        models.QuestionnaireJunction.questionnaire_id == questionnaire_id  # Filter by questionnaire_id
    ).all()

    if not previous_answers:
        return []

    # Construct response with question data and user's previous answers
    response = []
    for answer in previous_answers:
        response.append({
            "question_id": answer.question.id,
            "user_answer": answer.answer  # The user's previous answer
        })

    return response


@app.post("/submit-answers/")
def submit_answers(submission: schemas.AnswerRes, db: Session = Depends(get_db)):
    for answer_data in submission.answers:
                # Check if answer_content is a list or a string
        if isinstance(answer_data.answer, list):
            # Process it (e.g., join list of strings into a single string)
            processed_answer = ', '.join(answer_data.answer)
        else:
            # If it's already a string, use it directly
            processed_answer = answer_data.answer
        # Check if the answer already exists
        existing_answer = db.query(models.Answer).filter(
            models.Answer.user_id == submission.user_id,
            models.Answer.question_id == answer_data.question_id
        ).first()

        if existing_answer:
            # Update the existing answer
            print(f"Existing answer before update: {existing_answer}")
            existing_answer.answer = processed_answer
            print(f"Existing answer after update: {existing_answer.answer}")
            db.add(existing_answer) 

        else:
            # Insert a new answer
            new_answer = models.Answer(
                user_id=submission.user_id,
                question_id=answer_data.question_id,
                answer=processed_answer
            )
            db.add(new_answer)

    # Commit the transaction to save all answers
    db.commit()

    return {"message": "Answers submitted successfully"}