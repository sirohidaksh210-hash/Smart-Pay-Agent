# 💰 SmartPay Agent

> **AI-powered PayPal business assistant for small businesses & freelancers**  
> Built for the [PayPal AI Hackathon 2026](https://developer.paypal.com/community/blog/PayPal_AI_Hackathon)

[![Demo Video](https://img.shields.io/badge/YouTube-Demo%20Video-red?logo=youtube)](YOUR_YOUTUBE_LINK)
[![Live Demo](https://img.shields.io/badge/Live-Demo-blue)](YOUR_VERCEL_LINK)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

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
                                                                 ↓
                                                      Function Calling Layer
                                                                 ↓
                                                       PayPal REST APIs v2
                                                       (Sandbox Environment)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **AI Brain** | Google Gemini 1.5 Pro (function calling) |
| **Backend** | Python 3.11 + FastAPI |
| **Frontend** | React 18 + Vite |
| **PayPal APIs** | Invoicing V2, Transaction Search V1, Orders V2 |
| **Deployment** | Railway (backend) + Vercel (frontend) |

---

## 🚀 Quick Start

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

---

## 💬 Example Conversations

```
You:   "Create an invoice for sarah@design.com for $1,200 for brand identity project"
Agent: ✅ Invoice #INV-1730789234 sent to sarah@design.com
       Amount: $1,200.00 | Due in 7 days
       Want me to set a reminder to follow up if unpaid?

---

You:   "Show me my revenue for October"
Agent: 📊 October Revenue Summary
       Total Income:    $8,420.00 (23 transactions)
       Total Spent:     $340.00
       Net:             $8,080.00
       Top payer:       client@bigcorp.com ($3,200)
       ⚠️ 3 invoices still unpaid ($2,100 outstanding)

---

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

### Backend → Railway
1. Connect GitHub repo to [railway.app](https://railway.app)
2. Add environment variables in Railway dashboard
3. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Frontend → Vercel
1. Import repo in [vercel.com](https://vercel.com)
2. Set root directory to `frontend/`
3. Update `API_URL` in `src/App.jsx` to your Railway URL

---

## 📄 License

MIT License — open source, as required by the hackathon.

---

**Built with ❤️ for the PayPal AI Hackathon 2026**
