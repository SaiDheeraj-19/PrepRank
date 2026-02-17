from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models
import random

def seed():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Clear existing data (optional, be careful in prod)
    # db.query(models.StudentAnswer).delete()
    # db.query(models.TestResult).delete()
    # db.query(models.Question).delete()
    # db.query(models.Topic).delete()
    # db.query(models.Subject).delete()
    # db.query(models.Student).delete()
    # db.commit()

    if db.query(models.Student).first():
        print("Data already exists. Skipping seed.")
        return

    print("Seeding data...")

    # Create Student
    student = models.Student(name="John Doe")
    db.add(student)
    db.commit()

    # Subjects and Topics
    subjects = {
        "Mathematics": ["Algebra", "Calculus", "Probability"],
        "Physics": ["Mechanics", "Electromagnetism", "Optics"]
    }

    questions = []
    
    for sub_name, topic_names in subjects.items():
        sub = models.Subject(name=sub_name)
        db.add(sub)
        db.commit()
        
        for topic_name in topic_names:
            topic = models.Topic(name=topic_name, subject_id=sub.id)
            db.add(topic)
            db.commit()
            
            # Create Questions (varying importance)
            for i in range(5):
                q = models.Question(
                    content=f"Question {i+1} about {topic_name}",
                    topic_id=topic.id,
                    year=random.choice([2023, 2024, 2025]),
                    marks=random.choice([2, 5, 10]),
                    difficulty=random.choice(["Easy", "Medium", "Hard"])
                )
                db.add(q)
                questions.append(q)
    
    db.commit()

    # Create Mock Test Data (Simulate Student Performance)
    # Let's say the student is bad at Calculus but good at Algebra
    
    # Refresh questions to get IDs
    all_questions = db.query(models.Question).all()
    
    tr = models.TestResult(student_id=student.id)
    db.add(tr)
    db.commit()

    for q in all_questions:
        # Simulate correctness
        if "Calculus" in q.topic.name:
            is_correct = random.random() > 0.8 # mostly wrong
        elif "Algebra" in q.topic.name:
            is_correct = random.random() > 0.2 # mostly right
        else:
            is_correct = random.choice([True, False]) # random
            
        ans = models.StudentAnswer(
            test_result_id=tr.id,
            question_id=q.id,
            is_correct=is_correct,
            time_taken_seconds=random.randint(30, 120)
        )
        db.add(ans)
    
    db.commit()
    print("Seeding complete.")
    db.close()

if __name__ == "__main__":
    seed()
