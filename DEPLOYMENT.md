# Deployment Guide - Study Priority Engine

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.9+
- Node.js 16+
- npm or yarn

---

## Backend Setup

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
# From project root
export PYTHONPATH=$PYTHONPATH:$(pwd)/backend
python3 backend/seed_data.py
```

This creates SQLite database and seeds with sample data:
- 3 students
- 3 subjects (Math, Physics, Chemistry)
- ~50 questions across various topics
- Mock test results with varying performance

### 3. Start API Server
```bash
# From project root
uvicorn backend.app.main:app --reload --port 8000
```

**Verify:** Visit http://localhost:8000/docs (Swagger UI)

---

## Frontend Setup

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Start Development Server
```bash
npm run dev
```

**Verify:** Visit http://localhost:5173

---

## 🎬 Demo Flow

### Step 1: Verify Backend API
Open http://localhost:8000/docs

Try these endpoints:
1. **GET /** → Should return `{"message": "Study Priority Engine API is running"}`
2. **GET /study-plan/1** → Returns Student 1's priority list

### Step 2: Open Frontend Dashboard
1. Visit http://localhost:5173
2. Should see "API Connected" indicator
3. Default shows Student 1's study plan

### Step 3: Explore Features

**Summary Stats:** Top cards show overview (Total topics, Study Now count, etc.)

**Priority Chart:** Visual bar chart of top 10 priorities

**Priority Cards:** Detailed cards grouped by category (Study Now, Revise Later, etc.)

**Text Output:** Copy-pastable study plan summary

### Step 4: Test Different Students
Use dropdown to switch between:
- **Student 1:** Mixed performance (some mastered, some weak)
- **Student 2:** Different performance profile
- **Student 3:** Minimal data (cold start scenario)

---

## 📊 Understanding the Output

### Priority Card Breakdown
```
┌────────────────────────────────────┐
│ #1  🔴 Study Now                  │
│ Calculus (Mathematics)             │
│                                    │
│ Priority Score:      ████████ 85% │
│ Exam Importance:     █████████ 92%│
│ Your Mastery:        ██ 15%       │
│                                    │
│ "High exam weightage, low accuracy"│
└────────────────────────────────────┘
```

**Interpretation:**
- **Rank #1:** Most urgent topic
- **Priority 85%:** Very high priority (scale 0-100%)
- **Importance 92%:** Appears frequently in exams with high marks
- **Mastery 15%:** Student is currently weak (only 15% accuracy)
- **Recommendation:** Study Now (top 20th percentile)

---

## 🧪 Testing & Validation

### 1. Run Verification Script
```bash
# From project root
python verify_logic.py
```

**Expected Output:**
```
=== STUDY PRIORITY ENGINE VERIFICATION ===

INPUT DATA:
   topic_name  frequency  total_marks  avg_year  mastery
0     Algebra         10           50      2024      0.9
1    Calculus          2           10      2020      0.1
2  Thermodynamics      8           40      2025      0.4
3      Optics          5           25      2022      0.6

CALCULATED PRIORITIES:
        topic_name  importance  mastery  priority
2  Thermodynamics    0.95        0.4      0.57
1      Calculus      0.45        0.1      0.40
3        Optics      0.60        0.6      0.24
0       Algebra     1.00        0.9      0.10
```

**Key Insight:**
- Thermodynamics ranks #1 (high importance + low mastery)
- Algebra ranks #4 despite max importance (already mastered)

### 2. Manual Validation Checklist

Create this spreadsheet to validate logic:

| Topic | Freq | Marks | Year | Accuracy | Expected Rank | API Rank | ✅/❌ |
|-------|------|-------|------|----------|---------------|----------|------|
| Calculus | High | High | 2025 | 10% | 1-2 | ? | |
| Algebra | High | High | 2024 | 95% | 8-10 | ? | |

Fill in API Rank from `/study-plan/1` response and verify logic.

### 3. Run Automated Tests (Optional)
```bash
cd backend
pytest test_analytics.py -v
```

---

## 🌐 Production Deployment (Optional)

### Database: PostgreSQL on Railway
1. Create account at https://railway.app
2. Create PostgreSQL instance
3. Copy connection string
4. Update `backend/app/database.py`:
   ```python
   SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://...")
   ```

### Backend: Deploy to Render
1. Create account at https://render.com
2. New → Web Service → Connect GitHub repo
3. Build Command: `pip install -r backend/requirements.txt`
4. Start Command: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
5. Environment Variables:
   - `DATABASE_URL`: (from Railway)
6. Deploy → Copy URL (e.g., `https://study-engine-api.onrender.com`)

### Frontend: Deploy to Vercel
1. Create account at https://vercel.com
2. Import GitHub repo
3. **Root Directory:** `frontend`
4. **Build Command:** `npm run build`
5. **Output Directory:** `dist`
6. Environment Variables:
   - `VITE_API_URL`: (Render backend URL)
7. Deploy → Copy URL (e.g., `https://study-engine.vercel.app`)

### Seed Production Database
```bash
# SSH into Render or run locally pointing to production DB
export DATABASE_URL="postgresql://..."
python backend/seed_data.py
```

---

## 🐛 Troubleshooting

### Problem: "API Offline" in frontend
**Fix:**
1. Verify backend is running: `curl http://localhost:8000`
2. Check CORS is enabled in `main.py`
3. Check browser console for error details

### Problem: Empty study plan returned
**Fix:**
1. Verify database has data: Check `/docs` → Try `/study-plan/1`
2. Re-run seed script: `python backend/seed_data.py`
3. Check for errors in backend logs

### Problem: Frontend not loading
**Fix:**
1. Clear browser cache
2. Check if port 5173 is in use: `lsof -i :5173`
3. Try: `npm run dev -- --port 3000` (different port)

### Problem: Database locked (SQLite)
**Fix:**
1. Stop all running instances
2. Delete `study_engine.db`
3. Re-run seed script

---

## 📦 Project Structure Reference

```
studnet/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI app + CORS
│   │   ├── models.py         # Database models
│   │   ├── analytics.py      # Core engine
│   │   ├── schemas.py        # Pydantic schemas
│   │   └── database.py       # DB connection
│   ├── seed_data.py          # Sample data generator
│   ├── test_analytics.py     # Automated tests
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── PriorityList.jsx   # Card grid
│   │   │   ├── PriorityChart.jsx  # Bar chart
│   │   │   └── StudyPlanOutput.jsx# Text output
│   │   ├── services/
│   │   │   └── api.js        # Backend integration
│   │   ├── App.jsx           # Main component
│   │   └── App.css
│   └── package.json
├── COMPLETION_ROADMAP.md    # This file
├── VIVA_PREP.md             # Q&A preparation
├── PROJECT_REPORT.md        # Documentation
├── ARCHITECTURE.md          # System design
└── verify_logic.py          # Logic validation
```

---

## 🎯 Demo Presentation Tips

### 30-Second Elevator Pitch
*"This system analyzes past exam patterns and your mock test performance to tell you exactly which topics to study next. It ranks topics by Priority = Importance × (1 - Mastery), ensuring you focus on high-yield areas where you're weakest."*

### Live Demo Flow (3 minutes)
1. **Show API Docs (15 sec):** "This is the backend API with 3 endpoints"
2. **Show Frontend (30 sec):** "This is the dashboard. Student 1 has 12 topics."
3. **Explain Top Card (1 min):** "Calculus is #1 because it's worth 25 marks, appeared in 8/10 exams, but student only has 15% accuracy."
4. **Show Chart (30 sec):** "The visual confirms the ranking. Notice Algebra is low despite being important—student already mastered it."
5. **Download Output (15 sec):** "Students can copy or download their personalized study plan."
6. **Switch Students (30 sec):** "Different students get different plans based on their performance."

### Backup Plan (If Demo Breaks)
1. **Show verify_logic.py output:** "This proves the formula works on sample data"
2. **Walk through code:** "Let me show you the analytics.py calculation on lines 82-87"
3. **Show screenshots:** (Prepare ahead: Take screenshots of working demo)

---

## 📞 Support & Resources

- **API Documentation:** http://localhost:8000/docs (when running)
- **Formula Reference:** See `ARCHITECTURE.md` lines 31-36
- **Viva Q&A:** See `VIVA_PREP.md` for 22 detailed questions
- **Testing:** See `TESTING.md` for validation guide

---

**Ready to Deploy! 🎉**
