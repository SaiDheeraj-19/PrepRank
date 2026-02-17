# 🎯 VIVA QUICK REFERENCE CARD

> **PRINT THIS** and keep handy during viva for quick formula/fact lookup

---

## 📐 THE FORMULA (Memorize This)

### Priority Score
```
Priority = Importance × (1 - Mastery)
```

### Importance (Global)
```
Importance = (0.35 × Freq) + (0.45 × Marks) + (0.20 × Recency)
```

**Weights Rationale:**
- **Marks (0.45)** = Scoring potential is primary goal
- **Frequency (0.35)** = Reliable topics guarantee marks
- **Recency (0.20)** = Gentle adaptation to trends

### Mastery (Personal)
```
Mastery = (Correct / Total Attempts) × Confidence Factor

where:
Confidence Factor = 0.7 if attempts < 3, else 1.0
```

### Recency Calculation
```
Recency = 1 / (CurrentYear - ExamYear + 1)
```

**Example:** 2025 exam in 2026 = 1/(2026-2025+1) = 1/2 = 0.50

---

## 🔢 Quick Example

**Topic: Calculus**
- Frequency: 8/10 exams = Normalized 0.8
- Marks: 25 marks total = Normalized 0.9
- Recency: 2025 = 1/(2026-2025+1) = 0.5 → Normalized 0.9
- **Importance:** (0.35×0.8) + (0.45×0.9) + (0.20×0.9) = **0.865**

**Student Performance:**
- 2 correct out of 10 attempts = 0.2
- Attempts ≥ 3, so Confidence Factor = 1.0
- **Mastery:** 0.2 × 1.0 = **0.2**

**Priority:**
- **0.865 × (1 - 0.2) = 0.692** → Top 20% → **STUDY NOW**

---

## Edge Cases (Code Lines)

| Case | Handling | Line # |
|------|----------|--------|
| Empty Database | Return `[]` | 42 |
| Division by Zero | All get 1.0 | 65-71 |
| No Attempts | Mastery = 0.0 | 132 |
| Lucky Guess (<3 attempts) | Mastery × 0.7 | 114-119 |
| Perfect Mastery (100%) | Priority = 0 | 139 |

---

## 🎤 30-Second Elevator Pitch

*"Students preparing for exams with 50-100 topics face decision paralysis—they don't know what to study first. My system analyzes past exam patterns (frequency, marks, recency) and combines that with personal mock test performance. It calculates Priority = Importance × (1 - Mastery), ensuring students focus on high-yield topics where they're weakest. The output is a clear 'Top 5 to study this week' list that maximizes score improvement in limited time."*

---

## 🆚 Differentiators (vs LMS)

| Feature | LMS | Study Priority Engine |
|---------|-----|----------------------|
| Focus | "You completed 30%" | "Study Calculus next" |
| Data | Progress tracking | Exam patterns + mastery |
| Output | Course recommendations | Ranked priority list |
| Personalization | Generic | YOUR weaknesses |
| Goal | Content delivery | Decision optimization |

**Analogy:** LMS = Library (tracks what you read). This = Tutor (tells you what to study).

---

## 🧪 Key Technical Decisions

**Q: Why multiply instead of add?**
**A:** Mastered topics MUST have Priority=0, regardless of importance.
- Addition: P = 0.9 + 0.0 = 0.9 (wrong!)
- Multiplication: P = 0.9 × 0.0 = 0 (correct!)

**Q: Why normalize?**
**A:** Different scales (Freq: 1-100, Marks: 5-50, Recency: 0.05-1). Normalization ensures fair comparison.

**Q: Why penalize low attempts?**
**A:** 1/1 correct = 100% but unreliable (lucky guess). Damping: 100% × 0.7 = 70%.

**Q: Why these weights (0.35, 0.45, 0.20)?**
**A:** Heuristic starting point. Future: Learn optimal weights from student outcomes via regression.

---

## 📊 Categorization Rules

```python
Percentile Rank < 20%  → "Study Now"     (Top priority)
Percentile Rank < 70%  → "Revise Later"  (Secondary)
Percentile Rank ≥ 70%  → "Deprioritize"  (Low yield)

Special Overrides:
Mastery > 0.9 → "Mastered" (always)
Priority = 0  → "Deprioritize" (always)
```

---

## 🛠️ Tech Stack (One-Liner Each)

- **FastAPI:** Async Python web framework for REST API
- **SQLAlchemy:** Python ORM for database abstraction
- **Pandas:** Data manipulation & analytics (aggregation, normalization)
- **React:** Component-based UI library
- **PostgreSQL/SQLite:** Relational database for structured data
- **Vite:** Fast frontend build tool

---

## ⚠️ Limitations (Be Honest)

1. **Cold Start:** New students/topics lack data → Default to importance ranking
2. **Static Weights:** Hardcoded (0.35, 0.45, 0.20) → Future: Learn from outcomes
3. **Manual Tagging:** Questions require human topic mapping → Future: LLM auto-tagging
4. **No Time Estimation:** Says "what" not "how long" → Future: Study time optimizer

---

## 🚀 Future Scope (3 Concrete Items)

**Phase 2 (MVP+):**
1. **Spaced Repetition:** Re-boost priority after 30 days (forgetting curves)
2. **PDF Auto-Extract:** OCR + GPT-4 for question upload (5 min → 30 sec)
3. **Study Time Optimizer:** "3 hours free" → Generates sequence (knapsack algorithm)

---

## 💼 Business Model

**B2C (Students):**
- Free: 3 plans/month
- Pro: $5/month unlimited

**B2B (Institutes):**
- $500/month (white-label for 500 students)

**API (Platforms):**
- $0.10 per API call (pay-per-use)

**Moat:** Curated question bank (6-12 months) + Validated weights from outcomes (network effects)

---

## 📍 Key Line Numbers in analytics.py

- **Line 7-25:** Function docstring (explains entire approach)
- **Line 30-37:** SQL query for questions
- **Line 49-51:** Weight definitions (W_FREQ, W_MARKS, W_RECENCY)
- **Line 65-71:** robust_normalize() function
- **Line 79:** Recency formula
- **Line 82-87:** Importance calculation
- **Line 106:** Raw mastery calculation
- **Line 114-119:** adjust_mastery() damping
- **Line 132:** fillna(0.0) for cold start
- **Line 139:** Priority formula
- **Line 149-159:** get_category() percentile logic

---

## 🎬 Demo Flow (3 Minutes)

**0:00-0:30** "This is Study Priority Engine for Student 1 with 12 topics"

**0:30-1:30** "Calculus is #1 because:
- Importance: 92% (8/10 exams, 25 marks)
- Mastery: 15% (only 2/10 correct)
- Priority: 92% × (1 - 0.15) = 78%"

**1:30-2:00** "Chart confirms. Notice Algebra is low despite high importance—student mastered it (90%)"

**2:00-2:30** "Formula: Priority = Importance × (1 - Mastery). Multiplication ensures mastered topics get 0 priority"

**2:30-3:00** "Students can download text summary. Switch to Student 2 to see different personalized plan"

---

## 🚨 If Demo Breaks

**Backup Plan:**
1. Show `verify_logic.py` output (proves formula works)
2. Walk through `analytics.py` code (lines 82-87, 139)
3. Show screenshots (take beforehand!)
4. Explain: "Logic is correct, likely port/config issue"

**Never panic. You know the code inside-out.**

---

## ✅ Final Mental Checklist

**Can you:**
- [ ] Recite the formula from memory?
- [ ] Explain why multiplication (not addition)?
- [ ] Describe 3 edge cases + handling?
- [ ] Differentiate from LMS in 30 seconds?
- [ ] Walk through lines 82-87 of analytics.py?
- [ ] State 3 honest limitations?
- [ ] Propose 3 future enhancements?

**If YES to all → YOU'RE READY 🎓**

---

## 🎯 What Evaluators Look For

✅ **Technical Soundness:** Formula justified, edge cases handled  
✅ **Problem-Solution Fit:** Solves real problem clearly  
✅ **Honesty:** Admits limitations confidently  
✅ **Thought Process:** Considered alternatives (ML, collab filtering)  
✅ **Clarity:** Can explain to non-technical person  

**You have ALL of these. Don't doubt yourself.**

---

## 💪 Confidence Boosters

1. **Your code WORKS** (90% of student demos break)
2. **Your formula is SOUND** (mathematically justified)
3. **Your problem is REAL** (everyone understands it)
4. **Your docs are COMPREHENSIVE** (23,000+ words)
5. **You UNDERSTAND every line** (you can explain it all)

---

**Print this card. Keep it visible. You've got this. 🚀**

**Reminder:** Speak slowly. Use whiteboard. Show code. Be honest about limitations. You know this better than anyone in that room.
