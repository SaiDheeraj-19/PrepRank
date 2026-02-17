
<div align="center">

  <h1>🚀 PrepRank: The Study Priority Engine</h1>
  
  <p>
    <strong>Optimize Your Study Time. Maximize Your Exam Score.</strong>
  </p>

  <p>
    <a href="#-the-problem">The Problem</a> •
    <a href="#-the-solution">The Solution</a> •
    <a href="#-how-it-works">How It Works</a> •
    <a href="#-tech-stack">Tech Stack</a> •
    <a href="#-quick-start">Quick Start</a>
  </p>

  <br>

  ![Python](https://img.shields.io/badge/Backend-Python_3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
  ![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
  ![React](https://img.shields.io/badge/Frontend-React_18-61DAFB?style=for-the-badge&logo=react&logoColor=black)
  ![Tailwind](https://img.shields.io/badge/Style-Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)

</div>

<br>

---

## 🎯 The Problem

Students preparing for competitive exams (JEE, NEET, SATs) face a critical challenge: **Information Overload**. 

- 📚 **Too many topics** (50-100+) to cover in limited time.
- 😵 **Decision Paralysis**: "Should I study Algebra or Optics today?"
- 📉 **Inefficient Strategy**: Wasting hours on topics that rarely appear in exams or topics they've already mastered.

The result? **Hard work, but suboptimal scores.**

## 💡 The Solution

**PrepRank** is not just a study tracker. It is an **intelligent decision support system**. 

It analyzes past exam patterns and your personal performance to answer one simple question: **"What should I study *right now* to get the most marks?"**

---

## 🧠 How It Works

The engine uses a weighted priority algorithm to rank every topic dynamically.

### The Algorithm

$$ \text{Priority} = \text{Importance} \times (1 - \text{Mastery}) $$

#### 1. Global Importance (The "Yield")
We calculate how valuable a topic is based on 3 factors:
- **Frequency (35%)**: How often does it appear in exams?
- **Marks (45%)**: How many marks is it worth?
- **Recency (20%)**: Is it trending in recent years?

#### 2. Personal Mastery (The "Gap")
$$ \text{Mastery} = \frac{\text{Correct Answers}}{\text{Total Attempts}} \times \text{Confidence Factor} $$
- If you've mastered a topic (Mastery ≈ 1.0), the Priority drops to **0**, regardless of importance.
- If you're weak in a high-yield topic, the Priority skyrockets.

---

## 🛠 Tech Stack

### **Frontend**
- **React + Vite**: Blazing fast, component-based UI.
- **Tailwind CSS**: Modern, utility-first styling for a clean, professional dashboard.
- **Recharts**: Beautiful, responsive data visualization.

### **Backend**
- **FastAPI (Python)**: High-performance, async-ready REST API.
- **Pandas**: Powerful data manipulation for the analytics engine.
- **SQLAlchemy (PostgreSQL/SQLite)**: Robust ORM for data persistence.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+

### 1. Clone the Repository
```bash
git clone https://github.com/SaiDheeraj-19/PrepRank.git
cd PrepRank
```

### 2. Setup Backend
```bash
# Install dependencies
pip install -r backend/requirements.txt

# Initialize database with sample data
python backend/seed_data.py

# Start the API server
uvicorn backend.app.main:app --reload --port 8000
```

### 3. Setup Frontend
```bash
# Open a new terminal
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

Visit `http://localhost:5173` to view your personalized dashboard!

---

## 📸 Screenshots

*(Add screenshots of your dashboard here)*

| Priority Dashboard | Action Plan |
|:---:|:---:|
| Visualizes your Mastery vs Importance | Clear "Study Now" vs "Revise Later" lists |

---

## 🔮 Future Roadmap

- [ ] **Spaced Repetition**: Integrity forgetting curves to flag topics for revision.
- [ ] **PDF Auto-Tagging**: Use NLP to extract topics from uploaded question papers.
- [ ] **Study Time Optimization**: "I have 2 hours" -> Generates the perfect 2-hour schedule.


---

<div align="center">
  
  <p>Built with ❤️ by <strong>Sai Dheeraj</strong></p>
  
  <p>
    <em>"Optimize study time. Maximize exam scores."</em>
  </p>

</div>
