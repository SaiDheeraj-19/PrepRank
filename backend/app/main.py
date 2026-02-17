from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, database, analytics

# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Study Priority Engine", version="1.0")

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Study Priority Engine API is running"}

@app.post("/upload-question-paper", response_model=dict)
def upload_questions(payload: schemas.QuestionBulkUpload, db: Session = Depends(get_db)):
    """
    Accepts exam questions, year, marks, subject.
    Automatically maps them to Topics (creating Topics/Subjects if needed).
    """
    count = 0
    for q_data in payload.questions:
        # 1. Get or Create Subject
        subject = db.query(models.Subject).filter(models.Subject.name == q_data.subject).first()
        if not subject:
            subject = models.Subject(name=q_data.subject)
            db.add(subject)
            db.commit()
            db.refresh(subject)
        
        # 2. Get or Create Topic
        topic = db.query(models.Topic).filter(
            models.Topic.name == q_data.topic, 
            models.Topic.subject_id == subject.id
        ).first()
        if not topic:
            topic = models.Topic(name=q_data.topic, subject_id=subject.id)
            db.add(topic)
            db.commit()
            db.refresh(topic)
            
        # 3. Create Question
        question = models.Question(
            content=q_data.content,
            year=q_data.year,
            marks=q_data.marks,
            difficulty=q_data.difficulty,
            topic_id=topic.id
        )
        db.add(question)
        count += 1
    
    db.commit()
    return {"status": "success", "questions_uploaded": count}

@app.post("/mock-test-result", response_model=dict)
def submit_test_result(submission: schemas.MockTestSubmission, db: Session = Depends(get_db)):
    """
    Stores student answers, correctness, and time taken.
    """
    # Create Test Result entry
    test_result = models.TestResult(student_id=submission.student_id)
    db.add(test_result)
    db.commit()
    db.refresh(test_result)
    
    # Store Answers
    for ans in submission.answers:
        db_answer = models.StudentAnswer(
            test_result_id=test_result.id,
            question_id=ans.question_id,
            is_correct=ans.is_correct,
            time_taken_seconds=ans.time_taken_seconds
        )
        db.add(db_answer)
    
    db.commit()
    return {"status": "success", "test_id": test_result.id}

@app.get("/study-plan/{student_id}", response_model=schemas.StudyPlan)
def get_study_plan(student_id: int, db: Session = Depends(get_db)):
    """
    Returns the synthesized priority list for a specific student.
    """
    priorities = analytics.calculate_priorities(db, student_id)
    
    from datetime import datetime
    return {
        "student_id": student_id,
        "generated_at": datetime.now(),
        "priorities": priorities
    }
