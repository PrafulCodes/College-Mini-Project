# 💰 Money Council — Financial Advisory Dashboard

> **A full-stack web app that looks at your income, expenses, and debts — and tells you exactly what to do with your money.**

---

## 📖 Table of Contents

1. [What Is This Project?](#-what-is-this-project)
2. [What Can It Do?](#-what-can-it-do)
3. [How It Works (Simple Version)](#-how-it-works-simple-version)
4. [Tech Stack — What's Used & Why](#-tech-stack--whats-used--why)
5. [Project Folder Structure](#-project-folder-structure)
6. [Setup Guide — Step by Step](#-setup-guide--step-by-step)
   - [Windows Setup](#-windows-setup)
   - [Mac Setup](#-mac-setup)
   - [Linux Setup](#-linux-setup)
7. [Running the App](#-running-the-app)
8. [Using the App](#-using-the-app)
9. [API Endpoints Reference](#-api-endpoints-reference)
10. [Financial Agents Explained](#-financial-agents-explained)
11. [How the Dashboard Works](#-how-the-dashboard-works)
12. [Connecting Frontend to Backend](#-connecting-frontend-to-backend)
13. [Deploying to the Internet](#-deploying-to-the-internet)
14. [Troubleshooting](#-troubleshooting)
15. [Future Ideas](#-future-ideas)

---

## 🤔 What Is This Project?

**Money Council** is like having a smart financial advisor in your browser — for free.

You tell it:
- How much money you earn every month
- What you spend money on (rent, food, Netflix, etc.)
- What debts you have (credit card, student loan, etc.)
- How risky you're willing to be with investments

It tells you:
- Where your money is going (a colorful pie chart!)
- How much you could save in the next 6 months (a line chart!)
- How long it will take to pay off your debts (a bar chart!)
- A prioritized action plan: what to fix **first**, **second**, **third**

**Who is this for?** Students, working professionals, or anyone who wants to understand their finances better. If you've ever wondered "what should I do with my money?", this app is for you.

---

## ✨ What Can It Do?

### Frontend (The Website Part)
- **Input Form** — Enter your income, add/remove expense rows, add/remove debt rows
- **Live Validation** — Catches mistakes before you submit (like negative numbers)
- **Dashboard** — Shows your financial health with 3 interactive charts
- **Action Plan** — Gives you a numbered to-do list for your finances
- **Works on Phone & Desktop** — Responsive design

### Backend (The Brain Part)
- **4 AI-style Agents** that each analyze one part of your finances:
  - 🧾 **Budget Agent** — Are you spending too much?
  - 💰 **Savings Agent** — Do you have enough saved up?
  - 💳 **Debt Agent** — How should you pay off your debts?
  - 📈 **Investment Agent** — Are you ready to invest?
- **Action Plan Generator** — Combines all agent advice into one priority list
- **Save Your Plan** — Store your action plan and retrieve it later
- **Interactive API Docs** — Test the API yourself at `/docs`

---

## 🔄 How It Works (Simple Version)

Think of it like a doctor's visit, but for your wallet:

```
You fill out the form  →  Your data is sent to the backend
        ↓
The backend runs 4 specialist "agents" on your data
        ↓
Each agent gives advice (budget, savings, debt, investments)
        ↓
A "council" combines all advice into one priority action plan
        ↓
The dashboard shows everything with charts and recommendations
```

---

## 🛠 Tech Stack — What's Used & Why

### Frontend

| Technology | What It Does | Why We Use It |
|---|---|---|
| **React 18** | Builds the user interface | Fast, reusable components; industry standard |
| **Vite 7** | Runs the development server and builds the app | Much faster than older tools like Webpack |
| **React Router 6** | Switches between Form page and Dashboard page | Lets us have multiple "pages" without reloading |
| **Axios 1.6** | Sends data to the backend API | Easier to use than built-in `fetch()` |
| **Chart.js 4.4** | Draws the interactive charts | Best charting library for the web |
| **react-chartjs-2** | Connects Chart.js with React | Makes Chart.js work nicely with React components |
| **Plain CSS** | Styles the app | No extra framework needed; kept simple |

### Backend

| Technology | What It Does | Why We Use It |
|---|---|---|
| **Python 3.8+** | The programming language | Great for data logic; easy to read |
| **FastAPI** | Creates the web API | Automatically creates documentation; very fast |
| **Uvicorn** | Runs the FastAPI server | Lightweight and production-ready |
| **Pydantic 2.5** | Validates all incoming data | Prevents bad data from crashing the app |

---

## 📁 Project Folder Structure

Here's what every file and folder does:

```
Money Council/
│
├── 📁 src/                          ← All frontend (React) code lives here
│   ├── 📁 components/
│   │   ├── SummaryCard.jsx          ← The little metric cards on the dashboard
│   │   └── ActionPlan.jsx           ← Displays the numbered recommendations
│   │
│   ├── 📁 pages/
│   │   ├── InputForm.jsx            ← The main form where you enter your data
│   │   └── Dashboard.jsx            ← The results page with charts
│   │
│   ├── 📁 services/
│   │   ├── api.js                   ← Handles all communication with the backend
│   │   └── mockData.js              ← Fake data used if backend is not running
│   │
│   ├── 📁 styles/
│   │   ├── index.css                ← Global styles (fonts, resets)
│   │   ├── App.css                  ← Styles for the App wrapper
│   │   ├── InputForm.css            ← Styles for the form (responsive!)
│   │   ├── Dashboard.css            ← Styles for the dashboard layout
│   │   ├── SummaryCard.css          ← Styles for the metric cards
│   │   └── ActionPlan.css           ← Styles for the recommendation cards
│   │
│   ├── App.jsx                      ← Sets up the two routes (form & dashboard)
│   └── main.jsx                     ← Entry point — starts the React app
│
├── 📁 backend/                      ← All backend (Python/FastAPI) code lives here
│   ├── main.py                      ← Starts the FastAPI server, sets up CORS
│   │
│   ├── 📁 schemas/
│   │   └── financial.py             ← Defines the shape of all data (Pydantic models)
│   │
│   ├── 📁 routes/
│   │   └── financial.py             ← The API endpoints (/analyze, /plan, etc.)
│   │
│   ├── 📁 services/
│   │   ├── agent_service.py         ← The 4 financial analysis agents
│   │   ├── council_service.py       ← Combines agent advice into an action plan
│   │   └── storage.py               ← Saves/retrieves action plans in memory
│   │
│   ├── 📁 agents/                   ← Standalone rule-based agent modules
│   │   ├── __init__.py
│   │   ├── budget_agent.py          ← Analyzes spending patterns
│   │   ├── savings_agent.py         ← Evaluates emergency fund readiness
│   │   ├── debt_agent.py            ← Recommends debt repayment strategy
│   │   └── investment_agent.py      ← Checks if you're ready to invest
│   │
│   ├── requirements.txt             ← List of Python packages to install
│   └── .env.example                 ← Example environment configuration
│
├── index.html                       ← The single HTML file the React app loads into
├── package.json                     ← List of JavaScript packages + run scripts
├── vite.config.js                   ← Configuration for Vite (the build tool)
└── README.md                        ← This file!
```

---

## 🚀 Setup Guide — Step by Step

> **Before you start:** You need two things installed on your computer:
> - **Node.js** (version 16 or higher) — for the frontend
> - **Python** (version 3.8 or higher) — for the backend
>
> Don't have them? Download Node.js from [nodejs.org](https://nodejs.org) and Python from [python.org](https://python.org). Install both, then come back here.

---

### 🪟 Windows Setup

**Step 1 — Check if Node.js and Python are installed**

Open the "Command Prompt" app (search for `cmd` in your Start Menu) and type:

```cmd
node --version
python --version
```

If both show a version number (like `v18.0.0` and `Python 3.10.0`), you're good! If not, install them from the links above.

---

**Step 2 — Download or clone the project**

If you have Git, open Command Prompt and run:
```cmd
git clone https://github.com/your-username/money-council.git
cd money-council
```

If you don't have Git, download the ZIP from GitHub and extract it, then `cd` into the folder.

---

**Step 3 — Install the frontend packages**

In Command Prompt, inside the project folder, run:
```cmd
npm install
```

This downloads all the JavaScript packages (React, Chart.js, etc.). It may take a minute. You'll see a `node_modules` folder appear — that's normal.

---

**Step 4 — Set up the backend (Python virtual environment)**

A "virtual environment" is like a clean room just for this project's Python packages so they don't mix with other projects.

```cmd
cd backend
python -m venv venv
```

Now activate the virtual environment:
```cmd
venv\Scripts\activate
```

You'll see `(venv)` appear at the start of your command line. That means it worked!

---

**Step 5 — Install Python packages**

With the virtual environment active, run:
```cmd
pip install -r requirements.txt
```

This installs FastAPI, Uvicorn, Pydantic, and other needed packages.

---

**You're done setting up on Windows!** Jump to [Running the App](#-running-the-app) below.

---

### 🍎 Mac Setup

**Step 1 — Check if Node.js and Python are installed**

Open the "Terminal" app (find it in Applications → Utilities) and run:
```bash
node --version
python3 --version
```

> **Mac tip:** Mac comes with Python 2 pre-installed. Make sure you use `python3` (not `python`) throughout this guide.

If not installed, you can install them using Homebrew:
```bash
# Install Homebrew first (if you don't have it)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Then install Node and Python
brew install node python3
```

---

**Step 2 — Download or clone the project**

```bash
git clone https://github.com/your-username/money-council.git
cd money-council
```

---

**Step 3 — Install frontend packages**

```bash
npm install
```

---

**Step 4 — Set up the Python virtual environment**

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

You'll see `(venv)` at the start of your terminal line. 

---

**Step 5 — Install Python packages**

```bash
pip install -r requirements.txt
```

---

**You're done setting up on Mac!** Jump to [Running the App](#-running-the-app) below.

---

### 🐧 Linux Setup

**Step 1 — Install Node.js and Python**

On Ubuntu/Debian:
```bash
sudo apt update
sudo apt install nodejs npm python3 python3-pip python3-venv -y
```

On Fedora/RHEL:
```bash
sudo dnf install nodejs npm python3 python3-pip -y
```

Verify:
```bash
node --version
python3 --version
```

---

**Step 2 — Clone the project**

```bash
git clone https://github.com/your-username/money-council.git
cd money-council
```

---

**Step 3 — Install frontend packages**

```bash
npm install
```

---

**Step 4 — Set up the Python virtual environment**

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

---

**Step 5 — Install Python packages**

```bash
pip install -r requirements.txt
```

---

**You're done setting up on Linux!** Continue below.

---

## ▶️ Running the App

You need **two terminal/command prompt windows open at the same time** — one for the backend, one for the frontend.

---

### Terminal 1 — Start the Backend (Python/FastAPI)

**Windows:**
```cmd
cd backend
venv\Scripts\activate
uvicorn main:app --reload --port 5000
```

**Mac/Linux:**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 5000
```

**✅ Success looks like this:**
```
INFO:     Uvicorn running on http://0.0.0.0:5000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

The backend is now running. Leave this terminal open!

---

### Terminal 2 — Start the Frontend (React/Vite)

Open a **new** terminal window, navigate to the project root folder (NOT the backend folder), and run:

**Windows:**
```cmd
cd money-council
npm run dev
```

**Mac/Linux:**
```bash
cd money-council
npm run dev
```

**✅ Success looks like this:**
```
  VITE v7.x.x  ready in 500ms

  ➜  Local:   http://localhost:5173/
  ➜  Press h to show help
```

---

### Open the App in Your Browser

Go to: **http://localhost:5173**

You should see the Money Council form! 🎉

---

### Quick Access Links (while everything is running)

| What | URL |
|---|---|
| The App (frontend) | http://localhost:5173 |
| Backend API | http://localhost:5000 |
| API Documentation (Swagger) | http://localhost:5000/docs |
| Alternative API Docs (ReDoc) | http://localhost:5000/redoc |

---

## 🖱️ Using the App

**Step 1 — Enter your monthly income**

Type how much money you earn per month (before taxes or after — just be consistent).

**Step 2 — Add your expenses**

Click `+ Add Expense` to add a row. Fill in:
- **Category** — What you spend on (e.g., "Rent", "Food", "Netflix")
- **Amount** — How much per month (e.g., `1500`)

Add as many categories as you like. Click the ❌ button to remove a row.

**Step 3 — Add your debts**

Click `+ Add Debt` to add a row. Fill in:
- **Name** — What the debt is (e.g., "Credit Card", "Student Loan")
- **Amount** — Total amount still owed (e.g., `5000`)
- **Interest Rate** — Annual interest rate percentage (e.g., `18.5`)

If you have no debts, leave the default row empty.

**Step 4 — Select Risk Tolerance**

Choose how comfortable you are with investment risk:
- **Low** — You want safe, stable investments
- **Medium** — You want a balance of growth and safety
- **High** — You're okay with ups and downs for potentially higher returns

**Step 5 — Click "Analyze My Finances"**

If everything is filled out correctly, you'll be taken to your Dashboard!

---

### What You'll See on the Dashboard

**6 Summary Cards** at the top:
- 💵 Monthly Income
- 💸 Total Expenses
- 🎯 Disposable Income (what's left over)
- 📊 Total Debt
- 📈 Savings Rate (%)
- ⚖️ Debt-to-Income Ratio

**3 Interactive Charts:**
- 🥧 **Pie Chart** — See exactly where your money goes each month
- 📈 **Line Chart** — See your projected savings growth over 6 months
- 📊 **Bar Chart** — See all your debts side by side, with repayment comparison

**Action Plan** at the bottom:
- A numbered list of what to do, from most urgent to least urgent
- Each item shows: what to do, why, estimated savings, and timeframe

---

## 📡 API Endpoints Reference

You can test all these from **http://localhost:5000/docs** using the interactive Swagger UI.

---

### POST `/api/analyze` — Analyze Finances

The main endpoint. Send your financial data, get back a full analysis + action plan.

**Request body:**
```json
{
  "monthly_income": 5000,
  "expenses": [
    { "category": "Housing", "amount": 1500 },
    { "category": "Food", "amount": 400 }
  ],
  "debts": [
    { "name": "Credit Card", "amount": 2000, "interest_rate": 18 }
  ],
  "risk_tolerance": "Medium"
}
```

**Response:**
```json
{
  "status": "success",
  "summary": {
    "monthly_income": 5000,
    "total_expenses": 1900,
    "disposable_income": 3100,
    "total_debt": 2000,
    "savings_rate": 0.62,
    "debt_to_income_ratio": 0.4
  },
  "action_plan": {
    "plan": [
      "Pay extra towards high-interest debt (Credit Card 18%)",
      "Build emergency fund with $300/month",
      "Reduce discretionary spending by 15%",
      "Start a small monthly SIP investment"
    ],
    "priority_order": ["debt", "savings", "budget", "investment"],
    "total_actions": 4
  },
  "recommendations": [ ... ],
  "budget_advice": "...",
  "savings_advice": "...",
  "debt_advice": "...",
  "investment_advice": "..."
}
```

**Status Codes:**
- `200` — Analysis successful
- `400` — Bad data sent
- `422` — Validation error (check field types/names)
- `500` — Server error

---

### GET `/api/plan/{user_id}` — Get Saved Plan

Retrieve a previously saved action plan for a user.

**Example:**
```bash
curl http://localhost:5000/api/plan/1
```

**Response:**
```json
{
  "user_id": 1,
  "plan": ["Pay debt", "Save money", "Budget wisely"],
  "created_at": "2026-02-22T10:30:00",
  "updated_at": "2026-02-22T10:30:00"
}
```

- Returns `404` if no plan found for that user ID.

---

### POST `/api/plan/{user_id}` — Save or Update a Plan

Save an action plan for a user. If one already exists, it updates it.

**Request body:**
```json
{
  "plan": [
    "Pay off credit card",
    "Save $500/month",
    "Cut expenses by 10%"
  ]
}
```

**Rules:**
- Plan must have between **1 and 20 items**
- Each item must be a string

---

### DELETE `/api/plan/{user_id}` — Delete a Plan

Removes a saved plan for the given user.

```bash
curl -X DELETE http://localhost:5000/api/plan/1
```

Returns `404` if no plan found.

---

### GET `/health` — Check if Backend is Running

```bash
curl http://localhost:5000/health
```

Returns:
```json
{ "status": "healthy", "service": "Money Council API" }
```

---

## 🤖 Financial Agents Explained

The backend has **4 independent agents** — each one looks at your finances from one angle and gives specific advice.

---

### 🧾 Budget Agent

**What it does:** Looks at how much of your income you're spending.

**How it works:**
- Calculates your total expenses and expense ratio (expenses ÷ income)
- Finds your biggest spending category
- Rates your situation:
  - **50–70%** of income on expenses → Healthy ✅
  - **70–85%** → Warning ⚠️
  - **85%+** → Critical 🚨

**Output example:**
```
"Your expense ratio (64%) is healthy. Your biggest category is Rent (40%)."
```

---

### 💰 Savings Agent

**What it does:** Checks if you have enough emergency savings.

**How it works:**
- Emergency fund target = 3× your monthly expenses
- Recommended monthly savings = 20% of your income
- Calculates how many months until you hit the target

**Output example:**
```
"You need ₹192,000 in emergency savings. At ₹20,000/month, you'll reach it in 4.6 months."
```

---

### 💳 Debt Agent

**What it does:** Tells you the smartest way to pay off your debts.

**Two strategies it uses:**

| Strategy | When Used | How It Works |
|---|---|---|
| **Avalanche** | You told it your interest rates | Pay highest-interest debt first (saves the most money) |
| **Snowball** | No interest rates given | Pay smallest balance first (keeps you motivated) |

**High-interest debt** (above 15% APR) is flagged as urgent!

**Output example:**
```
"Use AVALANCHE method. Pay Credit Card (18%) first, then Personal Loan (12%)."
```

---

### 📈 Investment Agent

**What it does:** Decides if you're ready to invest — and if so, how.

**You must pass two tests before investing:**
1. ✅ Emergency fund covers at least 3 months of expenses
2. ✅ No high-interest debt (above 15%)

If you pass, it recommends an allocation based on your risk tolerance:

| Risk Level | Recommended Split |
|---|---|
| **Low** | 70% Index Funds, 20% Bonds, 10% Savings Account |
| **Medium** | 40% Index Funds, 30% Mutual Funds, 20% ETFs, 10% Savings |
| **High** | 30% Index Funds, 30% ETFs, 25% Sectoral Funds, 15% Growth Stocks |

---

### 🏛️ Council Service (The Synthesizer)

After all 4 agents run, the **Council Service** combines their advice into one clean, prioritized action plan:

1. **Debt actions** — highest priority (stop the bleeding)
2. **Savings actions** — second priority (build your safety net)
3. **Budget actions** — third priority (optimize your spending)
4. **Investment actions** — lowest priority (grow your wealth)

---

## 📊 How the Dashboard Works

### Data Flow Diagram

```
InputForm.jsx
    ↓  (validates form, sends data)
api.js
    ↓  (POST /api/analyze)
Backend processes → 4 agents run
    ↓  (JSON response back)
Dashboard.jsx receives data
    ↓  (extracts summary, charts, recommendations)
SummaryCard ×6  +  3 Charts  +  ActionPlan component
```

### What Happens If the Backend Is Down?

The frontend has a **mock data fallback** built in. If the API call fails, the dashboard will load with sample data so you can still see how it looks. This is useful for testing or demos when the backend isn't running.

---

### Charts Deep Dive

**Pie Chart — Expense Distribution**
- Shows each expense category as a slice
- Hover over slices to see exact amounts
- Powered by Chart.js

**Line Chart — Savings Projection**
- X-axis: Months 0 through 6
- Y-axis: Your projected cumulative savings
- Formula: `Month N = Current Savings + (Monthly Contribution × N)`

**Bar Chart — Debt Repayment Timeline**
- Shows all your debts side by side
- Two bars per debt: total amount vs. monthly payment
- Includes a table below with full details (name, amount, interest rate)

---

## 🔗 Connecting Frontend to Backend

By default, the frontend looks for the backend at `http://localhost:5000/api`.

**To change this** (e.g., for production), edit this one line in `src/services/api.js`:

```javascript
// Line 4 — change this to your backend URL
const API_BASE_URL = 'http://localhost:5000/api'

// For production, use something like:
// const API_BASE_URL = 'https://api.yoursite.com/api'
```

**Optional — Use Environment Variables Instead:**

Create a file called `.env.local` in the project root:
```
VITE_API_URL=http://localhost:5000/api
```

Then update `api.js` to:
```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'
```

---

## 🌐 Deploying to the Internet

### Frontend Deployment (Vercel — Easiest)

1. Create a free account at [vercel.com](https://vercel.com)
2. Install the Vercel CLI:
   ```bash
   npm install -g vercel
   ```
3. Run in the project folder:
   ```bash
   npm run build
   vercel
   ```
4. Follow the prompts. Your site will be live in seconds!

---

### Frontend Deployment (Netlify)

1. Build the project:
   ```bash
   npm run build
   ```
2. Go to [netlify.com](https://netlify.com) → "Add new site" → "Deploy manually"
3. Drag and drop the `dist/` folder into the browser window
4. Done!

---

### Backend Deployment

The FastAPI backend can be deployed to platforms like **Heroku**, **Railway**, **Render**, or a **VPS (Virtual Private Server)**.

**Production command:**
```bash
uvicorn main:app --host 0.0.0.0 --port 5000 --workers 4
```

**Before deploying, update CORS settings in `backend/main.py`:**
```python
# Change this:
allow_origins=["*"]  # Allows everything (OK for development)

# To this:
allow_origins=["https://your-frontend-domain.com"]  # Only your site
```

---

### Docker Deployment

Create a `Dockerfile` in the project root:

```dockerfile
# Build stage
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Runtime stage
FROM node:18-alpine
WORKDIR /app
RUN npm install -g serve
COPY --from=build /app/dist ./dist
EXPOSE 3000
CMD ["serve", "-s", "dist", "-l", "3000"]
```

Build and run:
```bash
docker build -t money-council .
docker run -p 3000:3000 money-council
```

---

## 🐛 Troubleshooting

### "npm: command not found" or "node: command not found"
→ Node.js is not installed. Download it from [nodejs.org](https://nodejs.org) and restart your terminal.

---

### "python: command not found" (Mac/Linux)
→ Try `python3` instead of `python`. On Mac/Linux, Python 3 is often installed as `python3`.

---

### "Cannot connect to API" or Charts not loading
→ Make sure the backend is running! Open a terminal, activate the virtual environment, and run `uvicorn main:app --reload --port 5000`. Check that you see the "Application startup complete" message.

---

### "CORS error" in the browser console
→ The frontend and backend are on different ports, which is expected. Check that `backend/main.py` includes `http://localhost:5173` in the CORS origins list. It should look like:
```python
allow_origins=["http://localhost:5173", "http://localhost:3000", "*"]
```

---

### "422 Unprocessable Entity" from the API
→ The data you're sending doesn't match what the API expects. Common mistakes:
- Field names are wrong (use `monthly_income`, not `monthlyIncome`)
- An amount is text instead of a number
- A required field is missing

Check the Swagger docs at http://localhost:5000/docs for the exact expected format.

---

### "ModuleNotFoundError" when starting the backend
→ Your virtual environment is not activated, or packages are not installed.

**Windows:** Run `venv\Scripts\activate` inside the `backend/` folder  
**Mac/Linux:** Run `source venv/bin/activate` inside the `backend/` folder  

Then run `pip install -r requirements.txt` again.

---

### Port 5173 or 5000 is already in use

**Frontend — use a different port:**
```bash
npm run dev -- --port 5174
```

**Backend — kill the process using the port:**

Mac/Linux:
```bash
lsof -i :5000
kill -9 <PID shown above>
```

Windows:
```cmd
netstat -ano | findstr :5000
taskkill /PID <PID shown above> /F
```

---

### Plans disappear when I restart the backend
→ This is expected! The current storage is **in-memory only** — plans are stored in RAM and lost when the server stops. To make plans permanent, you would need to add a database (like PostgreSQL or MongoDB). This is listed in Future Ideas below.

---

### Charts are rendering but showing wrong data
→ Check your browser console (press F12 → Console tab). Look for any JavaScript errors. Also verify the API response structure matches what the Dashboard expects — you can check the response in the Network tab (F12 → Network).

---

## 🔮 Future Ideas

Here are things that could be added to make this even better:

- 🔐 **User Authentication** — Login so each user has their own private data
- 🗄️ **Database Storage** — Save user plans permanently (PostgreSQL/MongoDB)
- 📥 **Import from Bank** — Connect to bank APIs to pull transactions automatically
- 📊 **Historical Tracking** — See how your finances changed month over month
- 🧮 **What-If Scenarios** — "What if I paid an extra $200/month on my loan?"
- 📄 **Export to PDF** — Download your financial report as a PDF
- 🌙 **Dark Mode** — For those late-night budgeting sessions
- 📱 **Mobile App** — A native iOS/Android version
- 🔔 **Notifications** — Alerts when you're overspending in a category
- 🌍 **Multi-Currency** — Support currencies beyond USD/INR

---

## ⚡ Quick Reference Card

```
STARTING THE APP
─────────────────────────────────────────────────
Terminal 1 (Backend):
  cd backend
  venv\Scripts\activate     (Windows)
  source venv/bin/activate  (Mac/Linux)
  uvicorn main:app --reload --port 5000

Terminal 2 (Frontend):
  npm run dev

Open browser: http://localhost:5173

─────────────────────────────────────────────────
USEFUL URLS
─────────────────────────────────────────────────
App:           http://localhost:5173
Backend:       http://localhost:5000
API Docs:      http://localhost:5000/docs

─────────────────────────────────────────────────
BUILDING FOR PRODUCTION
─────────────────────────────────────────────────
npm run build       → Creates dist/ folder
npm run preview     → Test the production build locally

─────────────────────────────────────────────────
CHANGE API URL
─────────────────────────────────────────────────
Edit: src/services/api.js → line 4
const API_BASE_URL = 'http://your-backend.com/api'

─────────────────────────────────────────────────
TEST THE BACKEND MANUALLY
─────────────────────────────────────────────────
curl http://localhost:5000/health
→ Should return: {"status":"healthy","service":"Money Council API"}
```

---

## 📦 Build Statistics

**Frontend Production Build Output:**
```
CSS:           10.17 kB  (gzipped: 2.51 kB)
JavaScript:   391.07 kB  (gzipped: 133.79 kB)
Build Time:   ~4.3 seconds
Modules:      96 total
```

**Backend Performance:**
```
Input validation:    10–50ms
Agent analysis:      50–100ms
Full response time:  ~100–150ms
Plan retrieval:      <5ms
```

---

## 🧑‍💻 Development Notes

### Form Validation Rules

| Field | Rules |
|---|---|
| Monthly Income | Required, must be greater than 0 |
| Expense Category | Optional, but required if Amount is filled |
| Expense Amount | Must be 0 or more |
| Debt Name | Optional, but required if Amount is filled |
| Debt Amount | Must be 0 or more |
| Debt Interest Rate | Must be 0 or more |
| Risk Tolerance | Required — choose Low, Medium, or High |

### Adding a New Page

1. Create `src/pages/YourPage.jsx`
2. Add a route in `src/App.jsx`:
   ```jsx
   <Route path="/your-page" element={<YourPage />} />
   ```
3. Add styles in `src/styles/YourPage.css`

### Adding a New Backend Endpoint

1. Add the route in `backend/routes/financial.py`
2. Create a Pydantic schema in `backend/schemas/financial.py`
3. Add business logic in `backend/services/agent_service.py` or a new service file

### Code Style Conventions

- **Frontend:** React functional components with Hooks; camelCase variable names
- **Backend:** FastAPI with Pydantic validation; snake_case variable names
- **CSS:** Mobile-first design with responsive breakpoints at 768px and 1024px

---

## 📄 License

This is a college mini-project. Free to use, modify, and extend.

---

**Made with 💸 for better financial decisions**

*Last updated: February 2026 | Version 1.0*