from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field
from typing import List, Optional
import secrets
import random

app = FastAPI(
    title="MCQ API",
    description="An API to provide randomized MCQs. Includes basic auth and admin creation of new questions.",
    version="1.0.0"
)

security = HTTPBasic()

# -------------------------------------------------------------------------
# 1) Basic Auth Data
# -------------------------------------------------------------------------
# Dictionary of username: password
users_db = {
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine"
}

ADMIN_PASSWORD = "4dM1n"  # The admin password

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Verify the user credentials against the users_db. 
    If a match is not found, raise an HTTPException(401).
    """
    correct_password = users_db.get(credentials.username)
    if not correct_password:
        # The username is not in our "database"
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    # Use 'secrets.compare_digest' to avoid timing attacks
    if not secrets.compare_digest(credentials.password, correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

def check_admin_password(password: str):
    """
    Verify if the provided password matches the admin password.
    """
    if not secrets.compare_digest(password, ADMIN_PASSWORD):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect admin password"
        )

# -------------------------------------------------------------------------
# 2) Data Model
# -------------------------------------------------------------------------
class Question(BaseModel):
    question: str = Field(..., description="The question text")
    subject: str = Field(..., description="The category of the question")
    correct: List[str] = Field(..., description="List of correct answer(s), e.g. ['A'] or ['A','C']")
    use: str = Field(..., description="Type of MCQ for which this question is used")
    answerA: str
    answerB: str
    answerC: Optional[str] = None
    answerD: Optional[str] = None

# In-memory storage for MCQs
mcq_data: List[Question] = [
    Question(
        question="What is the capital of France?",
        subject="Geography",
        correct=["B"],
        use="general",
        answerA="Berlin",
        answerB="Paris",
        answerC="Madrid",
        answerD="Rome"
    ),
    Question(
        question="2 + 2 = ?",
        subject="Math",
        correct=["C"],
        use="school",
        answerA="1",
        answerB="3",
        answerC="4",
        answerD="5"
    ),
    Question(
        question="Who wrote 'To Kill a Mockingbird'?",
        subject="Literature",
        correct=["A"],
        use="general",
        answerA="Harper Lee",
        answerB="Jane Austen",
        answerC="Mark Twain",
        answerD="Charles Dickens"
    )
]

# -------------------------------------------------------------------------
# 3) Endpoints
# -------------------------------------------------------------------------

@app.get("/health", tags=["Utility"])
def health_check():
    """
    Returns a simple message confirming that the API is responsive.
    """
    return {"status": "OK", "message": "The API is functional."}


@app.get("/questions", response_model=List[Question], tags=["Questions"])
def get_questions(
    use: str,
    subject: str,
    number_of_questions: int,
    current_user: str = Depends(get_current_username)
):
    """
    Returns a randomized list of `number_of_questions` MCQs 
    filtered by `use` and `subject`.
    Valid `number_of_questions` are commonly 5, 10, or 20 (per the exercise).
    """
    # Filter MCQs based on requested 'use' and 'subject'
    filtered_questions = [
        q for q in mcq_data
        if q.use.lower() == use.lower() and q.subject.lower() == subject.lower()
    ]
    # Shuffle and take the requested number
    random.shuffle(filtered_questions)
    
    if number_of_questions <= 0:
        raise HTTPException(status_code=400, detail="Number of questions must be > 0")

    # If requested more than available, just return them all
    selected_questions = filtered_questions[:number_of_questions]

    if not selected_questions:
        raise HTTPException(
            status_code=404,
            detail="No questions found with the given parameters."
        )
    return selected_questions


@app.post("/questions", tags=["Admin"])
def create_question(
    new_question: Question,
    admin_password: str,
    current_user: str = Depends(get_current_username)
):
    """
    Allows an admin user (with `admin_password == '4dM1n'`) to create a new question.
    The question payload follows the `Question` model.
    """
    # Check admin password
    check_admin_password(admin_password)

    # Add to in-memory list
    mcq_data.append(new_question)
    return {"message": "Question created successfully", "created": new_question.dict()}

