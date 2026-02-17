from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    topics = relationship("Topic", back_populates="subject")

class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    
    subject = relationship("Subject", back_populates="topics")
    questions = relationship("Question", back_populates="topic")

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    year = Column(Integer, index=True)  # Exam Year
    marks = Column(Integer)             # Weightage
    difficulty = Column(String, default="Medium") # Easy, Medium, Hard
    topic_id = Column(Integer, ForeignKey("topics.id"))
    
    topic = relationship("Topic", back_populates="questions")
    answers = relationship("StudentAnswer", back_populates="question")

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    
    test_results = relationship("TestResult", back_populates="student")

class TestResult(Base):
    __tablename__ = "test_results"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    taken_at = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", back_populates="test_results")
    answers = relationship("StudentAnswer", back_populates="test_result")

class StudentAnswer(Base):
    __tablename__ = "student_answers"
    id = Column(Integer, primary_key=True, index=True)
    test_result_id = Column(Integer, ForeignKey("test_results.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    is_correct = Column(Boolean)
    time_taken_seconds = Column(Integer)
    
    test_result = relationship("TestResult", back_populates="answers")
    question = relationship("Question", back_populates="answers")
