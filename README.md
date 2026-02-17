
<!-- PROJECT HEADER -->
<br />
<div align="center">
  <h1 align="center">🚀 PrepRank</h1>

  <p align="center">
    <strong>The Intelligent Study Priority Engine</strong>
    <br />
    <em>"Stop guessing. Start ranking. Optimize your limited study time."</em>
    <br />
    <br />
    <a href="https://github.com/SaiDheeraj-19/PrepRank/issues">Report Bug</a>
    ·
    <a href="https://github.com/SaiDheeraj-19/PrepRank/issues">Request Feature</a>
  </p>
</div>

<!-- TECH STACK BADGES -->
<div align="center">
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React" />
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind" />
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
</div>

<br />

<!-- TABLE OF CONTENTS -->
<details>
  <summary><strong>📚 Table of Contents</strong> (Click to Expand)</summary>
  <ol>
    <li><a href="#-about-the-project">About The Project</a></li>
    <li><a href="#-key-features">Key Features</a></li>
    <li><a href="#-the-algorithm">The Algorithm</a></li>
    <li><a href="#-getting-started">Getting Started</a></li>
    <li><a href="#-project-structure">Project Structure</a></li>
    <li><a href="#-license">License</a></li>
    <li><a href="#-contact">Contact</a></li>
  </ol>
</details>

---

## 💡 About The Project

> **"I have 50 topics to study and only 30 days left. Where do I even start?"**

Every student faces decision paralysis. Traditional tools are passive—they track what you *did*. **PrepRank** is active—it tells you what you *should do*.

It acts as a **Decision Support System**, analyzing exam history and your personal performance to generate a scientifically prioritized roadmap.

### Why PrepRank?
*   ✅ **Data-Driven**: No more intuition. Uses hard data (frequency, marks, recency).
*   ✅ **Personalized**: Adapts to *your* weaknesses.
*   ✅ **Visual**: See your progress in beautiful, interactive charts.

---

## ✨ Key Features

| Feature | Description |
| :--- | :--- |
| **📊 Smart Ranking Engine** | Dynamically re-ranks topics daily based on new performance data. |
| **🧠 Mastery Tracking** | Intelligent "Confidence Score" penalizes lucky guesses on mock tests. |
| **📅 Exam DNA Analysis** | Weights topics by Frequency (35%), Marks (45%), and Recency (20%). |
| **🎨 Actionable Dashboard** | Clean UI separating tasks into "Study Now" 🔴, "Revise" 🟡, and "Mastered" 🟢. |
| **🔌 Extensible API** | Built on FastAPI, ready integration with any LMS. |

---

## 🧬 The Algorithm

We believe in transparency. Here is the math that powers your success:

<div align="center">
  <h3><code>Priority = Importance × (1 - Mastery)</code></h3>
</div>

<details>
<summary><strong>See Detailed Formula Breakdown</strong> (Click to Expand)</summary>

#### 1. Global Importance Score (The "Yield")
How valuable is a topic globally?
```math
Importance = (0.35 \times Frequency) + (0.45 \times Marks) + (0.20 \times Recency)
```

#### 2. Personal Mastery Score (The "Gap")
How well do *you* know it?
```math
Mastery = \frac{Correct \ Answers}{Total \ Attempts} \times ConfidenceFactor
```
*(ConfidenceFactor penalty applied if attempts < 3)*

#### 3. Interpretation
| Score | Meaning | Action |
| :--- | :--- | :--- |
| **High Importance + Low Mastery** | 🔴 Critical Gap | **STUDY NOW** |
| **High Importance + High Mastery** | 🟢 Secure | **Revise Later** |
| **Low Importance** | ⚪ Low Yield | **Deprioritize** |

</details>

---

## 🚀 Getting Started

Follow these steps to get your local copy up and running.

### Prerequisites

*   **Python 3.9+**
*   **Node.js 16+**

### Installation

**1. Clone the Repository**
```bash
git clone https://github.com/SaiDheeraj-19/PrepRank.git
cd PrepRank
```

**2. Ignite the Backend (Python)** 🔥
```bash
# Create virtual environment (Recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Seed the database with demo data impact
python backend/seed_data.py

# Launch the API
uvicorn backend.app.main:app --reload --port 8000
```

**3. Launch the Frontend (React)** 🛸
```bash
# Open a new terminal
cd frontend

# Install dependencies
npm install

# Start the dashboard
npm run dev
```

Visit `http://localhost:5173` and see your priorities!

---

## 📂 Project Structure

A clean architecture for a clean mind.

```text
PrepRank/
├── backend/                # FastAPI Application
│   ├── app/
│   │   ├── analytics.py    # 🧠 The core ranking logic
│   │   ├── models.py       # 🗄️ Database schema (SQLAlchemy)
│   │   └── main.py         # 🔌 API Routes
│   ├── seed_data.py        # 🌱 Script to generate sample exam data
│   └── requirements.txt    # 📦 Python dependencies
└── frontend/               # React + Vite Application
    ├── src/
    │   ├── components/     # 🧩 Reusable UI components
    │   │   ├── PriorityChart.jsx
    │   │   └── TopPriorityTable.jsx
    │   ├── services/       # 📡 API fetchers
    │   └── App.jsx         # 📱 Main dashboard layout
    └── tailwind.config.js  # 🎨 Styling configuration
```

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 📬 Contact

**Sai Dheeraj** - [GitHub Profile](https://github.com/SaiDheeraj-19)

<div align="center">
  <br />
  <p>Built with ❤️ and ☕ for students everywhere.</p>
  <img src="https://forthebadge.com/images/badges/built-with-love.svg" alt="Built with Love" />
  <img src="https://forthebadge.com/images/badges/made-with-python.svg" alt="Made with Python" />
</div>
