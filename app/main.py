# app/main.py
from fastapi import FastAPI
from .database import engine
from . import models
from .routes import router
from fastapi.middleware.cors import CORSMiddleware

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
