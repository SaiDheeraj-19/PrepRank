import pandas as pd
import numpy as np

# Mock implementation of the logic for verification
def verify_logic():
    print("=== STUDY PRIORITY ENGINE VERIFICATION ===\n")
    
    # 1. Mock Data (Topics)
    data = {
        "topic_name": ["Algebra", "Calculus", "Thermodynamics", "Optics"],
        "frequency":  [10,       2,          8,                5],       # Algebra appears often
        "total_marks":[50,       10,         40,               25],      # Algebra has high marks
        "avg_year":   [2024,     2020,       2025,             2022],    # Thermo is very recent
        "mastery":    [0.9,      0.1,        0.4,              0.6]      # Already mastered Algebra
    }
    df = pd.DataFrame(data)
    
    print("INPUT DATA:")
    print(df)
    print("\n------------------------------")

    # 2. Normalize
    def norm(s):
        return (s - s.min()) / (s.max() - s.min())
    
    df["n_freq"] = norm(df["frequency"])
    df["n_marks"] = norm(df["total_marks"])
    # Recency: 2026 - Year
    df["recency_score"] = df["avg_year"].apply(lambda y: 1 / (2026 - y + 1))
    df["n_recency"] = norm(df["recency_score"])
    
    # 3. Importance (Freq 0.35, Marks 0.45, Recency 0.20)
    df["importance"] = (df["n_freq"]*0.35 + df["n_marks"]*0.45 + df["n_recency"]*0.20)
    
    # 4. Priority = Importance * (1 - Mastery)
    df["gap"] = 1 - df["mastery"]
    df["priority"] = df["importance"] * df["gap"]
    
    # Sort
    df = df.sort_values("priority", ascending=False)
    
    print("CALCULATED PRIORITIES:")
    print(df[["topic_name", "importance", "mastery", "priority"]])
    
    print("\n------------------------------")
    print("EXPLANATION:")
    print("1. Thermodynamics should likely be #1:")
    print("   - High Importance (High Marks + Recent)")
    print("   - Low Mastery (0.4)")
    print("2. Algebra should be lower:")
    print("   - High Importance (Max Freq/Marks)")
    print("   - BUT High Mastery (0.9) kills the priority.")
    
if __name__ == "__main__":
    verify_logic()
