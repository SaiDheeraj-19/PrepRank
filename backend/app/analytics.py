import pandas as pd
import numpy as np
import datetime
from sqlalchemy.orm import Session
from .models import Question, Topic, StudentAnswer, Subject

def calculate_priorities(db: Session, student_id: int):
    """
    Core Analytics Engine for Study Priority.
    
    Formula:
    Priority = Topic Importance * (1 - Student Mastery)
    
    1. Topic Importance (Global):
       - Frequency: How often it appears in exams
       - Weightage: Total marks associated
       - Recency: Weighted more if appeared in recent years
       
    2. Student Mastery (Personal):
       - Accuracy: Correct / Total Attempts
       - Damping: Low attempts (<3) reduce confidence in high mastery scores
       
    Returns:
       List of topics with priority scores and actionable recommendations.
    """
    
    # ---------------------------------------------------------
    # 1. Fetch Data
    # ---------------------------------------------------------
    query = db.query(
        Question.id.label("question_id"),
        Question.year,
        Question.marks,
        Topic.id.label("topic_id"),
        Topic.name.label("topic_name"),
        Subject.name.label("subject_name")
    ).select_from(Question).join(Topic).join(Subject).statement
    
    df_questions = pd.read_sql(query, db.bind)
    
    if df_questions.empty:
        return []

    # ---------------------------------------------------------
    # 2. Calculate Topic Importance (Global)
    # ---------------------------------------------------------
    
    # Weights for Importance Formula
    W_FREQ = 0.35
    W_MARKS = 0.45
    W_RECENCY = 0.20
    CURRENT_YEAR = datetime.datetime.now().year

    # Aggregation
    topic_stats = df_questions.groupby(["topic_id", "topic_name", "subject_name"]).agg(
        frequency=("question_id", "count"),
        total_marks=("marks", "sum"),
        # We calculate a weighted mean year later, or use max year as proxy
        max_year=("year", "max"), 
        avg_year=("year", "mean") 
    ).reset_index()

    # Robust Normalization Helper
    # Scales values between 0.0 and 1.0 safely
    def robust_normalize(series):
        if series.empty: return series
        _min, _max = series.min(), series.max()
        if _max == _min:
            # If all topics have same stats, they are equally important (1.0) if > 0
            return pd.Series([1.0 if x > 0 else 0.0 for x in series]) 
        return (series - _min) / (_max - _min)

    topic_stats["norm_freq"] = robust_normalize(topic_stats["frequency"])
    topic_stats["norm_marks"] = robust_normalize(topic_stats["total_marks"])
    
    # Recency Calculation:
    # 1 / (Age_Gap + 1). Recent years (gap=0) get score 1.0. Old years get lower.
    # We use avg_year to smooth out one-off appearances.
    topic_stats["recency_raw"] = topic_stats["avg_year"].apply(lambda y: 1 / (CURRENT_YEAR - y + 1) if (CURRENT_YEAR - y) >= 0 else 0.1)
    topic_stats["norm_recency"] = robust_normalize(topic_stats["recency_raw"])

    # Final Importance Score
    topic_stats["importance_score"] = (
        (topic_stats["norm_freq"] * W_FREQ) + 
        (topic_stats["norm_marks"] * W_MARKS) + 
        (topic_stats["norm_recency"] * W_RECENCY)
    )

    # ---------------------------------------------------------
    # 3. Calculate Student Mastery (Personalized)
    # ---------------------------------------------------------
    ans_query = db.query(
        StudentAnswer.is_correct,
        Question.topic_id
    ).join(Question).filter(StudentAnswer.test_result.has(student_id=student_id)).statement

    df_answers = pd.read_sql(ans_query, db.bind)

    if not df_answers.empty:
        mastery_stats = df_answers.groupby("topic_id").agg(
            correct=("is_correct", "sum"),
            attempts=("is_correct", "count")
        ).reset_index()
        
        # Raw Mastery = Accuracy
        mastery_stats["raw_mastery"] = mastery_stats["correct"] / mastery_stats["attempts"]
        
        # Damping Factor:
        # If attempts < 3, we don't fully trust "100% mastery".
        # We cap the mastery impact or multiply by a confidence factor.
        # Here: simple rule. If attempts < 3, max mastery is capped at 0.7 
        # (unless it's 0, then it stays 0). 
        # Better approach: Bayesian average or simple penalization.
        def adjust_mastery(row):
            score = row["raw_mastery"]
            if row["attempts"] < 3:
                # Penalize confidence. Trust purely positive results less.
                return score * 0.7 
            return score

        mastery_stats["mastery_score"] = mastery_stats.apply(adjust_mastery, axis=1)
        
    else:
        mastery_stats = pd.DataFrame(columns=["topic_id", "mastery_score"])

    # ---------------------------------------------------------
    # 4. Integrate Data
    # ---------------------------------------------------------
    final_df = pd.merge(topic_stats, mastery_stats, on="topic_id", how="left")
    
    # Important: If NO attempts, mastery is 0.0 (High Priority to study)
    final_df["mastery_score"] = final_df["mastery_score"].fillna(0.0)

    # ---------------------------------------------------------
    # 5. Calculate Priority
    # ---------------------------------------------------------
    # Priority = Importance * Gap
    # Higher Importance + Lower Mastery = Higher Priority
    final_df["priority_score"] = final_df["importance_score"] * (1 - final_df["mastery_score"])

    # ---------------------------------------------------------
    # 6. Generate Actionable Categories (Percentile Based)
    # ---------------------------------------------------------
    # Sort first
    final_df = final_df.sort_values(by="priority_score", ascending=False).reset_index(drop=True)
    
    n_topics = len(final_df)
    
    def get_category(index):
        if n_topics == 0: return "N/A"
        # Percentile rank: 0.0 (top) to 1.0 (bottom)
        rank_pct = index / n_topics 
        
        if rank_pct < 0.20:
            return "Study Now"     # Top 20%
        elif rank_pct < 0.70:
            return "Revise Later"  # Next 50%
        else:
            return "Deprioritize"  # Bottom 30%

    # Apply ranking logic
    # Edge case: If Priority is very low (e.g. < 0.1), force Deprioritize regardless of rank
    # Edge case: If Mastery > 0.9, force "Revise" or "Mastered"
    
    categories = []
    for idx, row in final_df.iterrows():
        p_score = row["priority_score"]
        m_score = row["mastery_score"]
        
        if m_score > 0.9:
            categories.append("Mastered")
        elif p_score == 0:
             categories.append("Deprioritize")
        else:
            categories.append(get_category(idx))
            
    final_df["recommendation"] = categories

    # Create final response with correct column names matching schema
    final_df = final_df.rename(columns={"subject_name": "subject"})
    
    return final_df.to_dict(orient="records")
