# 💰 SmartPay Agent

> **AI-powered PayPal business assistant for small businesses & freelancers**
> Built for the [PayPal AI Hackathon 2026](https://developer.paypal.com/community/blog/PayPal_AI_Hackathon)

[![Live Demo](https://img.shields.io/badge/Live-Demo-blue)](https://smart-pay-agent.vercel.app)
[![Demo Video](https://img.shields.io/badge/YouTube-Demo%20Video-red?logo=youtube)](YOUR_YOUTUBE_LINK)
[![Devpost](https://img.shields.io/badge/Devpost-Submission-003E54?logo=devpost)](https://devpost.com/software/smartpay-agent-9isz7h)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

🔗 **Live App:** https://smart-pay-agent.vercel.app
⚙️ **Backend API:** https://smart-pay-agent.onrender.com
📝 **Devpost:** https://devpost.com/software/smartpay-agent-9isz7h

> ⚠️ **Please note for testers:**
> - The backend runs on Render's free tier, so the **first request after a period of inactivity can take up to a minute** while the server wakes up. Please be patient on first load.
> - PayPal is in **Sandbox mode**. All invoices are test data and **no real money moves**.

---

## 🎯 The Problem

Small businesses and freelancers waste **2-3 hours every week** on manual payment admin:
- Logging into PayPal and manually creating invoices
- Hunting for unpaid invoices across tabs
- Writing awkward "friendly reminder" emails
- Copying transaction data into spreadsheets for reports

**Nobody has connected PayPal's powerful APIs to natural language — until now.**

---

## ✨ What SmartPay Agent Does

Talk to your PayPal account in plain English:

| You say | SmartPay does |
|---|---|
| *"Invoice john@email.com $500 for logo design"* | Creates & sends PayPal invoice instantly ✅ |
| *"How much did I earn this month?"* | Pulls transaction data & gives revenue summary 📊 |
| *"Show me all overdue invoices"* | Lists unpaid invoices with client details ⚠️ |
| *"Send reminders to late clients"* | Fires payment reminders via PayPal API 🔔 |

---

## 🏗️ Architecture

```
User (Chat UI)  →  React Frontend  →  FastAPI Backend  →  Gemini AI Agent
   (Vercel)                              (Render)                ↓
                                                      Function Calling Layer
                                                                 ↓
                                                       PayPal REST APIs v2
                                                       (Sandbox Environment)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **AI Brain** | Google Gemini (function calling) |
| **Backend** | Python 3.11 + FastAPI |
| **Frontend** | React 18 + Vite |
| **PayPal APIs** | Invoicing V2, Transaction Search V1, Orders V2, OAuth2 |
| **Deployment** | Render (backend) + Vercel (frontend) |

---

## 🚀 Quick Start (Run Locally)

### Prerequisites
- Python 3.11+
- Node.js 18+
- PayPal Developer Sandbox account
- Google Gemini API key

### 1. Clone & Setup
```bash
git clone https://github.com/YOUR_USERNAME/smartpay-agent.git
cd smartpay-agent
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # Mac/Linux

pip install -r requirements.txt

# Create your .env file
cp .env.example .env
# Edit .env with your actual API keys
```

### 3. Add Your Keys to `.env`
```env
PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_CLIENT_SECRET=your_paypal_client_secret
PAYPAL_BASE_URL=https://api-m.sandbox.paypal.com
GEMINI_API_KEY=your_gemini_api_key
```

> 🔒 Never commit your real `.env` file. It is listed in `.gitignore`.

### 4. Run Backend
```bash
uvicorn main:app --reload --port 8000
# Backend running at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### 5. Frontend Setup
```bash
cd ../frontend
npm install
npm run dev
# Frontend running at http://localhost:5173
```

### 6. Open the App
Navigate to **http://localhost:5173** and start chatting!

> 💡 When running locally, make sure `API_URL` in `frontend/src/App.jsx` points to `http://localhost:8000`.

---

## 💬 Example Conversations

```
You:   "Create an invoice for sarah@design.com for $1,200 for brand identity project"
Agent: ✅ Invoice #INV-1730789234 sent to sarah@design.com
       Amount: $1,200.00 | Due in 7 days
       Want me to set a reminder to follow up if unpaid?
```

```
You:   "Show me my revenue for October"
Agent: 📊 October Revenue Summary
       Total Income:    $8,420.00 (23 transactions)
       Total Spent:     $340.00
       Net:             $8,080.00
       Top payer:       client@bigcorp.com ($3,200)
       ⚠️ 3 invoices still unpaid ($2,100 outstanding)
```

```
You:   "Send reminders to everyone who hasn't paid"
Agent: Found 3 overdue invoices. Sending reminders...
       ✅ Reminder sent → john@freelance.com ($500 - 14 days overdue)
       ✅ Reminder sent → agency@co.com ($1,200 - 7 days overdue)
       ✅ Reminder sent → startup@tech.com ($400 - 21 days overdue)
       All reminders sent! Total outstanding: $2,100.00
```

---

## 📡 PayPal APIs Used

- **[Invoicing API v2](https://developer.paypal.com/docs/api/invoicing/v2/)** — Create, send, remind, cancel invoices
- **[Transaction Search API v1](https://developer.paypal.com/docs/api/transaction-search/v1/)** — Revenue analytics & history
- **[Orders API v2](https://developer.paypal.com/docs/api/orders/v2/)** — Order creation
- **[OAuth2 API](https://developer.paypal.com/docs/api/get-an-access-token/)** — Secure authentication

---

## 📁 Project Structure

```
smartpay-agent/
├── backend/
│   ├── main.py           # FastAPI server
│   ├── agent.py          # Gemini AI agent + function calling loop
│   ├── paypal_client.py  # PayPal API wrapper
│   ├── tools.py          # AI tool definitions
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx       # Main chat UI
│   │   └── main.jsx      # Entry point
│   ├── package.json
│   └── vite.config.js
└── README.md
```

---

## 🌐 Deployment

### Backend → Render
1. Create a new **Web Service** on [render.com](https://render.com) and connect this GitHub repo
2. Set **Root Directory** to `backend`
3. **Build Command:** `pip install -r requirements.txt`
4. **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables in the Render dashboard: `PAYPAL_CLIENT_ID`, `PAYPAL_CLIENT_SECRET`, `PAYPAL_BASE_URL`, `GEMINI_API_KEY`

### Frontend → Vercel
1. Import the repo in [vercel.com](https://vercel.com)
2. Set **Root Directory** to `frontend`
3. Update `API_URL` in `src/App.jsx` to your Render URL (`https://smart-pay-agent.onrender.com`)
4. Make sure your Vercel URL is allowed in the backend's CORS `allow_origins`

---

## ⚠️ Limitations

- Runs against the **PayPal Sandbox** only, so no real payments are processed
- Free-tier hosting means a **cold start delay** on the first request
- Built as a hackathon prototype, not yet hardened for production use

---

## 📄 License

MIT License — open source, as required by the hackathon.

---

**Built with ❤️ for the PayPal AI Hackathon 2026**
