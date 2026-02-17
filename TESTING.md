# System Validation & Testing Guide

## 1. Sanity Check (Manual)
You can manually verify the system logic without writing code:
1.  **Identify a Topic**: Pick "Calculus".
2.  **Check importance**: high marks? frequent? (Should be high importance).
3.  **Check Mastery**: Did the student get questions wrong? (Should be low mastery).
4.  **Expectation**: High Priority.
5.  **Verify**: Look at `recommendation`. If it says "Deprioritize", check if the mastery was actually recorded as high.

## 2. Edge Case Handling
The `analytics.py` handles these specific edge cases:

| Case | Handling | Code Ref |
| --- | --- | --- |
| **No Data** | Returns empty list `[]` | `if df_questions.empty: return []` |
| **Division by Zero** | Normalization returns 0.0 or 1.0 safely | `robust_normalize` function |
| **Old Exams** | Recency score decays automatically | `1 / (DateDelta + 1)` formula |
| **Lucky Guesses** | Low attempts (<3) are penalized | `adjust_mastery` function |
| **Perfect Mastery** | Priority forced to 0.0 | `Priority * (1 - Mastery)` |

## 3. How to Run Verification
Run the included python script to see a trace of the logic on small data:
```bash
python3 verify_logic.py
```
This script proves that the formula behaves correctly:
-   **Algebra**: High Importance, but High Mastery -> **Low Priority**.
-   **Thermo**: High Importance, Low Mastery -> **High Priority**.
