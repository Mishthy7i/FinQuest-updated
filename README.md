# 💸 FinQuest  

**FinQuest** is a **gamified personal finance tracker** that makes saving and budgeting fun, engaging, and habit-forming.  
Developed to encourage Gen Z users to build better financial habits through **gamification** and **AI-powered insights**.  

---

## 🚀 Problem / Need  
- Financial literacy among youth is still low.  
- Existing apps are either too educational (theory-heavy) or too tool-focused (just tracking).  
- There is a need for a **balanced platform** that teaches financial concepts while enabling real-world money management.  

---

## ✨ Features  
- 📊 **Expense Tracking** – Categorize expenses (Food, Travel, Bills, etc.)  
- 💸 **Savings Challenges** – e.g. “Save ₹500 this week”  
- 🔥 **Daily Streaks & Habits** – Build consistency with rewards  
- 🏆 **Achievements & Badges** – Unlock financial milestones  
- 📈 **Leaderboards** – Friendly competition with peers  
- 🎮 **XP & Levels** – Gamified progression system  
- 🤖 **AI Budget Coach** – Smart financial insights and personalized tips  

---

## 🛠️ Tech Stack  

| Component       | Technology Used |
|-----------------|-----------------|
| **Frontend**    | Flutter (Mobile App) |
| **Backend**     | FastAPI (Python) |
| **Database**    | MySQL |
| **Authentication** | JWT Tokens |
| **AI Coach**    | OpenAI GPT-4 Model |

---

## 📂 Project Structure  

```bash
FinQuest/
│
├── backend/          # FastAPI backend (Python)
│   ├── main.py       # API entrypoint
│   ├── routes/       # Expense, challenge, streak APIs
│   ├── models/       # Pydantic models
│   ├── db/           # SQL scripts & connection
│   └── auth/         # JWT authentication
│
├── frontend/         # Flutter mobile app
│   ├── lib/          
│   │   ├── screens/  # UI Screens
│   │   ├── widgets/  # Reusable widgets
│   │   ├── services/ # API calls
│   │   └── main.dart # App entrypoint
│
├── docs/             # Documentation & assets
│   └── screenshots/  # App screenshots
│
└── README.md         # Project readme
