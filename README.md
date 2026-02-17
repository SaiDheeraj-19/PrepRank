
<div align="center">

  # 🎓 PrepRank
  ### The Intelligent Study Priority Engine

  <p align="center">
    <a href="https://react.dev/">
      <img src="https://img.shields.io/badge/Frontend-React%2018-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React" />
    </a>
    <a href="https://fastapi.tiangolo.com/">
      <img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
    </a>
    <a href="https://tailwindcss.com/">
      <img src="https://img.shields.io/badge/Style-Tailwind%20CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind" />
    </a>
    <a href="https://www.python.org/">
      <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    </a>
  </p>

  <p align="center">
    <strong>Stop guessing what to study. Let data decide.</strong>
    <br />
    PrepRank analyzes exam patterns and your personal mastery to generate the perfect study plan.
    <br />
    <br />
    <a href="#-quick-start"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="#-demo">View Demo</a>
    ·
    <a href="https://github.com/SaiDheeraj-19/PrepRank/issues">Report Bug</a>
    ·
    <a href="https://github.com/SaiDheeraj-19/PrepRank/issues">Request Feature</a>
  </p>
</div>

<br />

---

## ⚡ The "Why"

> *"I have 2 months left, 50 chapters to cover, and no idea where to start."*

Every student faces this. Most study schedulers are just **calendars**. They tell you *when* to study, but not *what* or *why*.

**PrepRank is different.** It is a **Decision Support System** that answers:
1.  Which topics carry the most weight in the exam? 🏋️‍♀️
2.  Which of those strictly important topics am I weak at? 📉
3.  **Therefore, what should I study TODAY to maximize my marks?** 🚀

---

## ✨ Features at a Glance

| Feature | Description |
| :--- | :--- |
| **📊 Smart Ranking** | Algorithms rank topics by `Importance * (1 - Mastery)`. |
| **🧠 Mastery Tracking** | Tracks your mock test accuracy and applies a "Confidence Penalty" for lucky guesses. |
| **📅 Exam Analytics** | Weights topics by Frequency (35%), Marks (45%), and Recency (20%). |
| **🎨 Visual Dashboard** | Beautiful, color-coded bar charts to visualize your study gaps. |
| **🚀 Instant Action** | clear "Study Now", "Revise Later", and "Deprioritize" lists. |

---

## 🔬 The Science (The Algorithm)

We don't use AI black boxes. We use deterministic, explainable math.

### 1. The Global Importance Score
How valuable is a topic?
```math
Importance = (0.35 \times Frequency) + (0.45 \times Marks) + (0.20 \times Recency)
```

### 2. The Personal Mastery Score
How good are you at it?
```math
Mastery = \frac{Correct \ Answers}{Total \ Attempts} \times ConfidenceFactor
```
*(ConfidenceFactor penalty applied if attempts < 3)*

### 3. The Priority Score (The Magic) 🪄
```math
Priority = Importance \times (1 - Mastery)
```
- **High Importance + Low Mastery** = 🔴 **CRITICAL (Study Now)**
- **High Importance + High Mastery** = 🟢 **Low Priority (Don't waste time)**

---

## 💻 Tech Stack

This project is built with a modern, scalable stack:

- **Frontend**: 
  - [React](https://react.dev/) (Vite) for a blazing fast SPA.
  - [TailwindCSS](https://tailwindcss.com/) for professional, responsive styling.
  - [Recharts](https://recharts.org/) for data visualization.
  
- **Backend**: 
  - [FastAPI](https://fastapi.tiangolo.com/) for high-performance async APIs.
  - [Pandas](https://pandas.pydata.org/) for complex data analytics.
  - [SQLAlchemy](https://www.sqlalchemy.org/) for ORM database management.

---

## 🚀 Quick Start

Get the engine running locally in 2 minutes.

### 1. Clone & Install
```bash
git clone https://github.com/SaiDheeraj-19/PrepRank.git
cd PrepRank
```

### 2. Ignition (Backend) 🔥
```bash
# Setup Python Environment
pip install -r backend/requirements.txt

# Seed with Demo Data
python backend/seed_data.py

# Launch Server
uvicorn backend.app.main:app --reload --port 8000
```

### 3. Launchpad (Frontend) 🛸
```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173` and start optimizing!

---

## 📂 Project Structure

```text
PrepRank/
├── backend/
│   ├── app/
│   │   ├── analytics.py    # 🧠 The mathematical brain
│   │   ├── models.py       # 🗄️ Database schema
│   │   └── main.py         # 🔌 API Endpoints
│   └── seed_data.py        # 🌱 Demo data generator
└── frontend/
    └── src/
        ├── components/     # 🧩 React components
        └── services/       # 📡 API integrations
```

---

## 🤝 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">
  <p>Built with 💻 and ☕ by <strong>Sai Dheeraj</strong></p>
  <p>Star ⭐ this repo if you found it useful!</p>
</div>
