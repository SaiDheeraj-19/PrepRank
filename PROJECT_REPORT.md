# Study Priority Engine - Project Report

## 1. Abstract
The **Study Priority Engine** is an intelligent decision support system designed to optimize student preparation for competitive exams. Unlike traditional Learning Management Systems (LMS) that merely host content, this engine analyzes past exam trends and individual student performance to generate a personalized, data-driven study plan. By intelligently ranking topics based on "Exam Importance" and "Student Mastery," the system directs students to high-yield areas where they are weakest, thereby maximizing score potential in limited time.

## 2. Problem Statement
Students often waste time revising topics they have already mastered or studying low-weightage topics that rarely appear in exams. Existing solutions lack:
1.  **Context**: They don't account for how often a topic appears in actual exams.
2.  **Personalization**: They don't combine exam trends with individual weakness.
3.  **Actionability**: They provide raw scores instead of clear "what to do next" guidance.

## 3. System Architecture
The system follows a 3-tier architecture:
-   **Frontend**: React-based dashboard for visualization.
-   **Backend**: FastAPI (Python) acting as the REST API layer.
-   **Analytics Engine**: Pandas-based logic processing relational data from PostgreSQL/SQLite.

**Core Data Flow:**
1.  *Input*: Past specific exam questions (tagged by Topic, Year, Marks).
2.  *Input*: Student mock test results.
3.  *Process*: Analytics Engine computes `ImportanceScore` and `MasteryScore`.
4.  *Output*: Ranked list of topics with recommendations (e.g., "Study Now").

## 4. Methodology & Algorithms

### A. Topic Importance (Global)
We calculate the "yield" of a topic using three weighted factors:
$$ \text{Importance} = (W_f \times \text{NormFreq}) + (W_m \times \text{NormMarks}) + (W_r \times \text{NormRecency}) $$
-   **Frequency ($W_f=0.35$)**: How often does it appear?
-   **Marks ($W_m=0.45$)**: How much is it worth?
-   **Recency ($W_r=0.20$)**: Is it trending recently?

### B. Student Mastery (Personal)
$$ \text{Mastery} = \frac{\text{Correct Answers}}{\text{Total Attempts}} \times \text{ConfidenceFactor} $$
-   *ConfidenceFactor*: Penalizes 100% accuracy if attempts are too low (<3).

### C. Priority Ranking (The Core Logic)
$$ \text{Priority} = \text{Importance} \times (1 - \text{Mastery}) $$
-   **Logic**: High Importance + Low Mastery = **High Priority**.
-   **Logic**: High Mastery (1.0) forces Priority to 0, regardless of importance.

## 5. Assumptions & Limitations
**Assumptions:**
-   Manual tagging of questions to topics is accurate.
-   Mock tests are representative of actual exam difficulty.

**Limitations:**
-   **Cold Start**: New students/topics have no data (handled by default weights).
-   **Static Weights**: Importance weights are currently hardcoded, not learned.
-   **No Semantic Understanding**: The system tracks tags, not actual question content (NLP).

## 6. Future Scope
1.  **Automated Tagging**: Use NLP (BERT/LLMs) to auto-tag questions from PDFs.
2.  **Dynamic Weighing**: Use Regression to learn optimal $W_f, W_m$ from success rates.
3.  **Spaced Repetition**: Integrate forgetting curves (Ebbinghaus) into the schedule.
