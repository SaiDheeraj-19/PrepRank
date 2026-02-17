"""
Automated Test Suite for Study Priority Engine Analytics

Tests verify:
1. Edge cases (empty data, zero division)
2. Formula correctness (mastery impact, recency decay)
3. Categorization logic (percentile-based bucketing)
4. Data integrity (NaN handling, type safety)

Run: pytest test_analytics.py -v
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock
from app.analytics import calculate_priorities

# ============================================
# HELPER: Create Mock Database Session
# ============================================

def create_mock_db(questions_data=None, answers_data=None):
    """
    Creates a mock SQLAlchemy session for testing.
    """
    mock_db = Mock()
    
    # Mock query builder pattern
    query_obj = Mock()
    
    # Questions query result
    if questions_data is not None:
        df_questions = pd.DataFrame(questions_data)
        query_obj.statement = Mock()
        mock_db.query.return_value.select_from.return_value.join.return_value.join.return_value.statement = query_obj.statement
        pd.read_sql = Mock(side_effect=[df_questions, pd.DataFrame(answers_data) if answers_data else pd.DataFrame()])
    else:
        # Empty database
        query_obj.statement = Mock()
        mock_db.query.return_value.select_from.return_value.join.return_value.join.return_value.statement = query_obj.statement
        pd.read_sql = Mock(return_value=pd.DataFrame())
    
    mock_db.bind = Mock()
    return mock_db

# ============================================
# TEST CASES
# ============================================

def test_empty_database():
    """
    Test 1: Empty Database
    Given: No questions in database
    Expected: Return empty list []
    Rationale: Graceful degradation instead of crashing
    """
    # Arrange
    mock_db = Mock()
    query_obj = Mock()
    query_obj.statement = Mock()
    mock_db.query.return_value.select_from.return_value.join.return_value.join.return_value.statement = query_obj.statement
    mock_db.bind = Mock()
    
    # Mock empty dataframe
    import app.analytics as analytics_module
    original_read_sql = pd.read_sql
    pd.read_sql = Mock(return_value=pd.DataFrame())
    
    # Act
    result = calculate_priorities(mock_db, student_id=1)
    
    # Assert
    assert result == [], "Empty database should return empty list"
    
    # Cleanup
    pd.read_sql = original_read_sql


def test_zero_mastery_equals_full_importance():
    """
    Test 2: Zero Mastery → Priority = Importance
    Given: Topic with high importance, student never attempted
    Expected: Priority = Importance * (1 - 0) = Importance
    Rationale: Unstudied important topics should be highest priority
    """
    # Arrange
    questions_data = {
        "question_id": [1, 2],
        "year": [2025, 2024],
        "marks": [10, 10],
        "topic_id": [100, 100],
        "topic_name": ["Calculus", "Calculus"],
        "subject_name": ["Math", "Math"]
    }
    
    # No student answers (student never attempted this topic)
    answers_data = []
    
    mock_db = Mock()
    query_obj = Mock()
    query_obj.statement = Mock()
    mock_db.query.return_value.select_from.return_value.join.return_value.join.return_value.statement = query_obj.statement
    mock_db.bind = Mock()
    
    # Mock pandas read_sql to return our test data
    df_q = pd.DataFrame(questions_data)
    df_a = pd.DataFrame(columns=["is_correct", "topic_id"])  # Empty answers
    
    import app.analytics as analytics_module
    original_read_sql = pd.read_sql
    pd.read_sql = Mock(side_effect=[df_q, df_a])
    
    # Act
    result = calculate_priorities(mock_db, student_id=1)
    
    # Assert
    assert len(result) == 1, "Should have one topic"
    topic = result[0]
    assert topic["mastery_score"] == 0.0, "Mastery should be 0.0 for unstudied topics"
    assert topic["priority_score"] == topic["importance_score"], "Priority should equal Importance when Mastery=0"
    assert topic["recommendation"] in ["Study Now", "Revise Later"], "Should recommend studying"
    
    # Cleanup
    pd.read_sql = original_read_sql


def test_perfect_mastery_equals_zero_priority():
    """
    Test 3: Perfect Mastery → Priority = 0
    Given: Topic with high importance but 100% mastery (10/10 attempts correct)
    Expected: Priority = Importance * (1 - 1.0) = 0
    Rationale: Already mastered topics should not be prioritized
    """
    # Arrange
    questions_data = {
        "question_id": [1, 2, 3],
        "year": [2025, 2024, 2023],
        "marks": [10, 10, 10],
        "topic_id": [100, 100, 100],
        "topic_name": ["Algebra", "Algebra", "Algebra"],
        "subject_name": ["Math", "Math", "Math"]
    }
    
    # Perfect score: 10/10 correct
    answers_data = {
        "is_correct": [True] * 10,  # All correct
        "topic_id": [100] * 10
    }
    
    mock_db = Mock()
    query_obj = Mock()
    query_obj.statement = Mock()
    mock_db.query.return_value.filter.return_value.statement = query_obj.statement
    mock_db.query.return_value.select_from.return_value.join.return_value.join.return_value.statement = query_obj.statement
    mock_db.bind = Mock()
    
    df_q = pd.DataFrame(questions_data)
    df_a = pd.DataFrame(answers_data)
    
    import app.analytics as analytics_module
    original_read_sql = pd.read_sql
    pd.read_sql = Mock(side_effect=[df_q, df_a])
    
    # Act
    result = calculate_priorities(mock_db, student_id=1)
    
    # Assert
    assert len(result) == 1
    topic = result[0]
    # With 10 attempts, no damping factor applied
    assert topic["mastery_score"] == 1.0, "Mastery should be 1.0 for 10/10 correct"
    assert topic["priority_score"] == 0.0, "Priority must be 0 for perfect mastery"
    assert topic["recommendation"] == "Mastered", "Should be marked as Mastered"
    
    # Cleanup
    pd.read_sql = original_read_sql


def test_recency_weights_recent_years():
    """
    Test 4: Recency Calculation
    Given: Two topics, same frequency/marks, different years (2025 vs 2020)
    Expected: Recent topic (2025) should have higher importance
    Rationale: Exam patterns evolve; recent questions matter more
    """
    # Arrange
    questions_data = {
        "question_id": [1, 2],
        "year": [2025, 2020],  # One recent, one old
        "marks": [10, 10],
        "topic_id": [100, 101],
        "topic_name": ["ModernTopic", "OldTopic"],
        "subject_name": ["Math", "Math"]
    }
    
    # Both unstudied
    answers_data = []
    
    mock_db = Mock()
    query_obj = Mock()
    query_obj.statement = Mock()
    mock_db.query.return_value.select_from.return_value.join.return_value.join.return_value.statement = query_obj.statement
    mock_db.bind = Mock()
    
    df_q = pd.DataFrame(questions_data)
    df_a = pd.DataFrame(columns=["is_correct", "topic_id"])
    
    import app.analytics as analytics_module
    original_read_sql = pd.read_sql
    pd.read_sql = Mock(side_effect=[df_q, df_a])
    
    # Act
    result = calculate_priorities(mock_db, student_id=1)
    
    # Assert
    assert len(result) == 2
    modern = next(t for t in result if t["topic_name"] == "ModernTopic")
    old = next(t for t in result if t["topic_name"] == "OldTopic")
    
    # Recent topic should have higher importance (due to recency factor)
    assert modern["importance_score"] > old["importance_score"], "Recent year should boost importance"
    
    # Cleanup
    pd.read_sql = original_read_sql


def test_low_attempts_damping():
    """
    Test 5: Confidence Damping for Low Attempts
    Given: Student got 1/1 question correct (100% raw accuracy)
    Expected: Mastery should be penalized to ~0.7 (not 1.0)
    Rationale: Single lucky guess shouldn't indicate mastery
    """
    # Arrange
    questions_data = {
        "question_id": [1],
        "year": [2025],
        "marks": [10],
        "topic_id": [100],
        "topic_name": ["Calculus"],
        "subject_name": ["Math"]
    }
    
    # Only 1 attempt, correct
    answers_data = {
        "is_correct": [True],
        "topic_id": [100]
    }
    
    mock_db = Mock()
    query_obj = Mock()
    query_obj.statement = Mock()
    mock_db.query.return_value.filter.return_value.statement = query_obj.statement
    mock_db.query.return_value.select_from.return_value.join.return_value.join.return_value.statement = query_obj.statement
    mock_db.bind = Mock()
    
    df_q = pd.DataFrame(questions_data)
    df_a = pd.DataFrame(answers_data)
    
    import app.analytics as analytics_module
    original_read_sql = pd.read_sql
    pd.read_sql = Mock(side_effect=[df_q, df_a])
    
    # Act
    result = calculate_priorities(mock_db, student_id=1)
    
    # Assert
    topic = result[0]
    raw_mastery = 1.0  # 1/1 correct
    expected_adjusted = raw_mastery * 0.7  # Damping factor
    
    assert topic["mastery_score"] == pytest.approx(expected_adjusted, abs=0.01), \
        f"Low attempts should be damped: expected ~{expected_adjusted}, got {topic['mastery_score']}"
    
    # Cleanup
    pd.read_sql = original_read_sql


def test_all_equal_topics_normalized_correctly():
    """
    Test 6: Edge Case - All Topics Identical Stats
    Given: 3 topics, all with same frequency, marks, year
    Expected: All should have identical importance scores (1.0 after normalization)
    Rationale: robust_normalize should handle max - min = 0 case
    """
    # Arrange
    questions_data = {
        "question_id": [1, 2, 3],
        "year": [2024, 2024, 2024],
        "marks": [10, 10, 10],
        "topic_id": [100, 101, 102],
        "topic_name": ["TopicA", "TopicB", "TopicC"],
        "subject_name": ["Math", "Math", "Math"]
    }
    
    answers_data = []
    
    mock_db = Mock()
    query_obj = Mock()
    query_obj.statement = Mock()
    mock_db.query.return_value.select_from.return_value.join.return_value.join.return_value.statement = query_obj.statement
    mock_db.bind = Mock()
    
    df_q = pd.DataFrame(questions_data)
    df_a = pd.DataFrame(columns=["is_correct", "topic_id"])
    
    import app.analytics as analytics_module
    original_read_sql = pd.read_sql
    pd.read_sql = Mock(side_effect=[df_q, df_a])
    
    # Act
    result = calculate_priorities(mock_db, student_id=1)
    
    # Assert
    assert len(result) == 3
    importance_scores = [t["importance_score"] for t in result]
    
    # All should be equal (within floating point tolerance)
    assert importance_scores[0] == pytest.approx(importance_scores[1], abs=0.001)
    assert importance_scores[1] == pytest.approx(importance_scores[2], abs=0.001)
    
    # Cleanup
    pd.read_sql = original_read_sql


def test_priority_ranking_order():
    """
    Test 7: Correct Priority Ranking
    Given: 3 topics with known importance/mastery
    Expected: Correct descending order by priority score
    """
    # Arrange
    questions_data = {
        "question_id": [1, 2, 3],
        "year": [2025, 2024, 2023],
        "marks": [20, 10, 5],  # Different marks
        "topic_id": [100, 101, 102],
        "topic_name": ["HighPriority", "MediumPriority", "LowPriority"],
        "subject_name": ["Math", "Math", "Math"]
    }
    
    # Different mastery levels
    answers_data = {
        "is_correct": [False] * 5 + [True] * 5 + [True] * 10,  # 0%, 50%, 100%
        "topic_id": [100]*5 + [101]*5 + [102]*10
    }
    
    mock_db = Mock()
    query_obj = Mock()
    query_obj.statement = Mock()
    mock_db.query.return_value.filter.return_value.statement = query_obj.statement
    mock_db.query.return_value.select_from.return_value.join.return_value.join.return_value.statement = query_obj.statement
    mock_db.bind = Mock()
    
    df_q = pd.DataFrame(questions_data)
    df_a = pd.DataFrame(answers_data)
    
    import app.analytics as analytics_module
    original_read_sql = pd.read_sql
    pd.read_sql = Mock(side_effect=[df_q, df_a])
    
    # Act
    result = calculate_priorities(mock_db, student_id=1)
    
    # Assert
    assert len(result) == 3
    # Result should be sorted by priority (descending)
    for i in range(len(result) - 1):
        assert result[i]["priority_score"] >= result[i+1]["priority_score"], \
            "Results should be sorted by priority in descending order"
    
    # Cleanup
    pd.read_sql = original_read_sql


# ============================================
# INTEGRATION TEST (Full Flow)
# ============================================

def test_realistic_scenario():
    """
    Test 8: Realistic Multi-Topic Scenario
    Given: Mix of topics with varying importance and mastery
    Expected: Correct categorization (Study Now, Revise Later, etc.)
    """
    # Arrange: Real-world-like data
    questions_data = {
        "question_id": list(range(1, 21)),  # 20 questions
        "year": [2025]*5 + [2024]*5 + [2023]*5 + [2020]*5,
        "marks": [15, 10, 8, 5, 3] * 4,
        "topic_id": [100]*5 + [101]*5 + [102]*5 + [103]*5,
        "topic_name": ["Calculus"]*5 + ["Algebra"]*5 + ["Geometry"]*5 + ["OldTopic"]*5,
        "subject_name": ["Math"]*20
    }
    
    # Mixed performance
    answers_data = {
        "is_correct": (
            [False]*10 +  # Calculus: 0% (10 attempts)
            [True]*10 +   # Algebra: 100% (10 attempts)
            [True]*3 + [False]*3 +  # Geometry: 50% (6 attempts)
            []  # OldTopic: Never attempted
        ),
        "topic_id": (
            [100]*10 +
            [101]*10 +
            [102]*6
        )
    }
    
    mock_db = Mock()
    query_obj = Mock()
    query_obj.statement = Mock()
    mock_db.query.return_value.filter.return_value.statement = query_obj.statement
    mock_db.query.return_value.select_from.return_value.join.return_value.join.return_value.statement = query_obj.statement
    mock_db.bind = Mock()
    
    df_q = pd.DataFrame(questions_data)
    df_a = pd.DataFrame(answers_data)
    
    import app.analytics as analytics_module
    original_read_sql = pd.read_sql
    pd.read_sql = Mock(side_effect=[df_q, df_a])
    
    # Act
    result = calculate_priorities(mock_db, student_id=1)
    
    # Assert
    assert len(result) == 4
    
    calculus = next(t for t in result if t["topic_name"] == "Calculus")
    algebra = next(t for t in result if t["topic_name"] == "Algebra")
    
    # Calculus: High importance (recent, high marks), Low mastery (0%)
    # Should be top priority
    assert calculus["recommendation"] in ["Study Now"], "Weak + Important = Study Now"
    
    # Algebra: High importance, but perfect mastery (100%)
    # Should be deprioritized or mastered
    assert algebra["recommendation"] in ["Mastered", "Deprioritize"], "Mastered topics should not be prioritized"
    
    # Cleanup
    pd.read_sql = original_read_sql


# ============================================
# RUN TESTS
# ============================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
