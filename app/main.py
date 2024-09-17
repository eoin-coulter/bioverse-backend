# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from .database import engine,get_db
from . import models, schemas  
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session  
from typing import List



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://bioverse-frontend-lime.vercel.app","http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create database tables if they don't exist
models.Base.metadata.create_all(bind=engine)


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



@app.get("/admin/users")
def get_users_with_completed_questionnaires(db: Session = Depends(get_db)):
    users = db.query(models.User).all()  # Get all users

    response = []

    for user in users:
        # Fetch all distinct questionnaire IDs the user has started answering
        questionnaires = db.query(models.Questionnaire.id).join(
            models.QuestionnaireJunction, models.QuestionnaireJunction.questionnaire_id == models.Questionnaire.id
        ).join(
            models.Answer, models.Answer.question_id == models.QuestionnaireJunction.question_id
        ).filter(
            models.Answer.user_id == user.id
        ).distinct().all()

        completed_questionnaires_count = 0

        # Check for each questionnaire if it's completed
        for questionnaire in questionnaires:
            # Count the number of questions in the questionnaire
            total_questions = db.query(models.QuestionnaireJunction).filter(
                models.QuestionnaireJunction.questionnaire_id == questionnaire.id
            ).count()

            # Count the number of answers the user has provided for that questionnaire
            total_answers = db.query(models.Answer).join(
                models.QuestionnaireJunction, models.Answer.question_id == models.QuestionnaireJunction.question_id
            ).filter(
                models.Answer.user_id == user.id,
                models.QuestionnaireJunction.questionnaire_id == questionnaire.id
            ).count()

            # Only count the questionnaire as "completed" if all questions are answered
            if total_questions == total_answers:
                completed_questionnaires_count += 1

        response.append({
            "id": user.id,
            "username": user.username,
            "completed_questionnaires": completed_questionnaires_count
        })

    return response

@app.get("/admin/user/{user_id}/questionnaires")
def get_user_questionnaires_and_answers(user_id: int, db: Session = Depends(get_db)):
    # Fetch all distinct questionnaires that the user has answered questions for
    questionnaires = db.query(models.Questionnaire).join(
        models.QuestionnaireJunction, models.QuestionnaireJunction.questionnaire_id == models.Questionnaire.id
    ).join(
        models.Answer, models.Answer.question_id == models.QuestionnaireJunction.question_id
    ).filter(
        models.Answer.user_id == user_id
    ).distinct().all()

    response = []

    for questionnaire in questionnaires:
        # Fetch questions and corresponding answers for each questionnaire
        questions_and_answers = db.query(models.Question, models.Answer).join(
            models.Answer, models.Answer.question_id == models.Question.id
        ).filter(
            models.Answer.user_id == user_id,
            models.QuestionnaireJunction.questionnaire_id == questionnaire.id
        ).all()

        # Format the question and answer pairs
        qna = [
            {"question": question.question.get('question'), "answer": answer.answer}
            for question, answer in questions_and_answers
        ]

        # Append to the response
        response.append({
            "questionnaire_name": questionnaire.title,
            "qna": qna
        })

    return response
