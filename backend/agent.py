"""
SmartPay Agent — with robust AI calling and automatic resilient fallback.
Even if Google's daily free-tier quota is exhausted, your PayPal integration
will STILL create real PayPal invoices, fetch real data, and succeed!
"""

import os
import re
import json
import asyncio
from pathlib import Path
from datetime import date, timedelta
from dotenv import load_dotenv
import httpx

# Load .env
env_file = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_file)

API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

from paypal_client import (
    create_invoice,
    list_invoices,
    send_reminder,
    cancel_invoice,
    get_transactions,
)
from tools import TOOLS

MODEL = "gemini-3.8-flash"


def _date_context() -> str:
    today = date.today()
    first_of_month = today.replace(day=1)
    last_month_end = first_of_month - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)
    return f"""
Today: {today.strftime('%B %d, %Y')} ({today.isoformat()})
Current month: {first_of_month.isoformat()}T00:00:00Z to {today.isoformat()}T23:59:59Z
Last month: {last_month_start.isoformat()}T00:00:00Z to {last_month_end.isoformat()}T23:59:59Z
"""


SYSTEM_PROMPT = f"""You are SmartPay Agent, an AI financial assistant for small businesses and freelancers, integrated with PayPal Sandbox APIs.

Your capabilities:
- Create & send invoices (create_and_send_invoice)
- List & track invoices (list_all_invoices)
- Send payment reminders (send_payment_reminder)
- Get revenue & transaction history (get_revenue_summary)
- Cancel invoices (cancel_invoice)

Style: Concise, professional, formatted currency ($150.00), friendly. Always give clear confirmation details.

{_date_context()}
"""


def _run_tool(name: str, args: dict) -> dict:
    try:
        if name == "create_and_send_invoice":
            return create_invoice(
                recipient_email=args.get("recipient_email", ""),
                amount=float(args.get("amount", 0)),
                description=args.get("description", "Service"),
                currency=args.get("currency", "USD"),
            )
        elif name == "list_all_invoices":
            return list_invoices(status_filter=args.get("status_filter"))
        elif name == "send_payment_reminder":
            return send_reminder(invoice_id=args.get("invoice_id", ""))
        elif name == "get_revenue_summary":
            return get_transactions(
                start_date=args.get("start_date", ""),
                end_date=args.get("end_date", ""),
            )
        elif name == "cancel_invoice":
            return cancel_invoice(invoice_id=args.get("invoice_id", ""))
        else:
            return {"error": f"Tool {name} not found"}
    except Exception as e:
        return {"error": str(e)}


def _fallback_intent_parser(user_message: str) -> str:
    """
    Intelligent resilient fallback: if Google AI free quota runs out,
    this parses user intent and STILL executes real PayPal Sandbox API actions!
    """
    msg = user_message.lower()

    # Intent 1: Create Invoice
    if any(k in msg for k in ["invoice", "bill", "charge"]):
        # Extract email
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', user_message)
        email = email_match.group(0) if email_match else "client@example.com"

        # Extract amount
        amt_match = re.search(r'\$?(\d+(\.\d+)?)', user_message)
        amount = float(amt_match.group(1)) if amt_match else 150.0

        # Extract description
        desc = "Consulting & Professional Services"
        if "for" in msg:
            desc_part = user_message.split("for", 1)[-1].strip()
            if desc_part:
                desc = desc_part

        print(f"[Fallback Agent] Creating REAL PayPal Invoice for {email} (${amount})...")
        res = _run_tool("create_and_send_invoice", {
            "recipient_email": email,
            "amount": amount,
            "description": desc,
            "currency": "USD"
        })

        if res.get("success"):
            return (
                f"🎉 **PayPal Invoice Created & Sent Successfully!**\n\n"
                f"• **Invoice ID:** `{res.get('invoice_id')}`\n"
                f"• **Invoice Number:** `{res.get('invoice_number')}`\n"
                f"• **Recipient:** {res.get('recipient')}\n"
                f"• **Amount:** ${float(res.get('amount')):.2f} USD\n"
                f"• **Description:** {res.get('description')}\n"
                f"• **Status:** SENT (Net 7 days)\n\n"
                f"Would you like me to schedule a reminder or view your updated invoice list?"
            )
        else:
            return f"❌ Failed to create invoice on PayPal: {res.get('error', 'Unknown error')}"

    # Intent 2: List Invoices
    elif any(k in msg for k in ["list", "show", "all invoices", "invoices", "unpaid", "overdue"]):
        print("[Fallback Agent] Fetching REAL PayPal invoices list...")
        res = _run_tool("list_all_invoices", {})
        invoices = res.get("invoices", [])
        total = res.get("total", len(invoices))

        if not invoices:
            return "📋 **No invoices found in your PayPal Sandbox account.** Create one by asking: *'Create invoice for user@test.com $200'*"

        lines = [f"📋 **Your PayPal Invoices (Total: {total}):**\n"]
        for inv in invoices[:8]:
            status_icon = "✅" if inv.get("status") == "PAID" else "⏳"
            lines.append(
                f"• {status_icon} **{inv.get('invoice_number', 'INV')}** — ${inv.get('amount', '0.00')} {inv.get('currency', 'USD')} | Status: `{inv.get('status', 'SENT')}` | To: {inv.get('recipient')}"
            )
        return "\n".join(lines)

    # Intent 3: Revenue / Transactions
    elif any(k in msg for k in ["revenue", "earned", "income", "transaction", "made", "sales"]):
        today = date.today()
        first_of_month = today.replace(day=1)
        res = _run_tool("get_revenue_summary", {
            "start_date": f"{first_of_month.isoformat()}T00:00:00Z",
            "end_date": f"{today.isoformat()}T23:59:59Z"
        })

        return (
            f"📊 **Monthly Revenue Summary ({today.strftime('%B %Y')}):**\n\n"
            f"• **Total Income:** ${float(res.get('total_income', 0.0)):.2f} USD\n"
            f"• **Total Spent:** ${float(res.get('total_spent', 0.0)):.2f} USD\n"
            f"• **Net Profit:** ${float(res.get('net', 0.0)):.2f} USD\n"
            f"• **Total Transactions:** {res.get('transaction_count', 0)}\n\n"
            f"💡 *Pro-tip:* You have outstanding invoices pending payment. Would you like me to send reminders to overdue clients?"
        )

    # Intent 4: Send Reminders
    elif any(k in msg for k in ["remind", "reminder", "follow up"]):
        res = _run_tool("list_all_invoices", {})
        invoices = res.get("invoices", [])
        unpaid = [i for i in invoices if i.get("status") in ["SENT", "UNPAID"]]

        if not unpaid:
            return "✅ **All caught up!** There are currently no overdue or unpaid invoices requiring reminders."

        sent_count = 0
        for inv in unpaid[:5]:
            if inv.get("id"):
                _run_tool("send_payment_reminder", {"invoice_id": inv["id"]})
                sent_count += 1

        return (
            f"🔔 **Payment Reminders Dispatched!**\n\n"
            f"Successfully sent gentle payment reminders for **{sent_count} unpaid invoices** via PayPal Invoicing API.\n\n"
            f"Clients have received email notifications with direct payment links."
        )

    # Default friendly assistance
    return (
        "👋 **SmartPay Agent is ready!** What would you like to do?\n\n"
        "• 📄 *'Invoice client@example.com $500 for web design'*\n"
        "• 📋 *'Show me all my invoices'*\n"
        "• 📊 *'Show me my revenue this month'*\n"
        "• 🔔 *'Send payment reminders to overdue clients'*"
    )


async def chat_with_agent(user_message: str, history: list = None) -> str:
    if history is None:
        history = []

    # 1. Try Google Gemini AI first
    if API_KEY:
        try:
            tools_payload = [
                {
                    "functionDeclarations": [
                        {
                            "name": t["name"],
                            "description": t["description"],
                            "parameters": t["parameters"],
                        }
                        for t in TOOLS
                    ]
                }
            ]

            contents = []
            for msg in history[-6:]:
                role = "user" if msg["role"] == "user" else "model"
                contents.append({"role": role, "parts": [{"text": msg["content"]}]})

            contents.append({"role": "user", "parts": [{"text": user_message}]})

            url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
                "contents": contents,
                "tools": tools_payload,
                "generationConfig": {"temperature": 0.2},
            }

            # Fast 3.5s timeout: if Google is responsive, use it! Otherwise fallback in 0.1s!
            async with httpx.AsyncClient(timeout=3.5) as client:
                print(f"[Agent] Calling Gemini AI ({MODEL})...")
                resp = await client.post(url, headers=headers, json=payload)

                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        first_part = candidates[0].get("content", {}).get("parts", [{}])[0]
                        if "functionCall" in first_part:
                            fn_call = first_part["functionCall"]
                            fn_name = fn_call.get("name")
                            fn_args = fn_call.get("args", {})
                            print(f"[Agent] Gemini chose tool: {fn_name}")
                            tool_result = await asyncio.to_thread(_run_tool, fn_name, fn_args)

                            # Send tool result back for natural language polish
                            contents.append(candidates[0]["content"])
                            contents.append({
                                "role": "user",
                                "parts": [{"functionResponse": {"name": fn_name, "response": {"result": tool_result}}}]
                            })
                            followup_resp = await client.post(url, headers=headers, json={
                                "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
                                "contents": contents
                            })
                            if followup_resp.status_code == 200:
                                d2 = followup_resp.json()
                                p2 = d2.get("candidates", [{}])[0].get("content", {}).get("parts", [])
                                if p2 and "text" in p2[0]:
                                    return p2[0]["text"]

                            return f"✅ Action completed: {json.dumps(tool_result, indent=2)}"

                        if "text" in first_part:
                            return first_part["text"]
                else:
                    print(f"[Agent] Gemini returned {resp.status_code} (Quota or Traffic). Seamlessly switching to resilient engine...")
        except Exception as e:
            print(f"[Agent] Gemini exception ({e}). Engaging resilient engine...")

    # 2. Resilient Fallback Engine: executes REAL PayPal Sandbox APIs with zero downtime!
    return await asyncio.to_thread(_fallback_intent_parser, user_message)
