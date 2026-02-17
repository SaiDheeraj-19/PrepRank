from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- Input Schemas ---

class QuestionCreate(BaseModel):
    subject: str
    topic: str
    content: str
    year: int
    marks: int
    difficulty: str = "Medium"

class QuestionBulkUpload(BaseModel):
    questions: List[QuestionCreate]

class AnswerCreate(BaseModel):
    question_id: int
    is_correct: bool
    time_taken_seconds: int

class MockTestSubmission(BaseModel):
    student_id: int
    answers: List[AnswerCreate]

# --- Output Schemas ---

class TopicPriority(BaseModel):
    topic_name: str
    subject: str
    importance_score: float
    mastery_score: float
    priority_score: float
    recommendation: str  # "Study Now", "Revise Later", "Deprioritize"

class StudyPlan(BaseModel):
    student_id: int
    generated_at: datetime
    priorities: List[TopicPriority]
