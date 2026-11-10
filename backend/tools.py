"""
Tool definitions for the Gemini AI function-calling layer.
Each tool maps directly to a PayPal API action.
"""

TOOLS = [
    {
        "name": "create_and_send_invoice",
        "description": (
            "Create a new PayPal invoice and send it immediately to a client or customer. "
            "Use this when the user says things like 'invoice', 'bill', 'charge', 'send payment request'."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "recipient_email": {
                    "type": "string",
                    "description": "The email address of the client to invoice.",
                },
                "amount": {
                    "type": "number",
                    "description": "The invoice amount as a number (e.g. 299.99). Do NOT include currency symbols.",
                },
                "description": {
                    "type": "string",
                    "description": "What the invoice is for (e.g. 'Logo design', 'Web development - Phase 1').",
                },
                "currency": {
                    "type": "string",
                    "description": "Currency code, default USD. Use USD unless user specifies otherwise.",
                },
            },
            "required": ["recipient_email", "amount", "description"],
        },
    },
    {
        "name": "list_all_invoices",
        "description": (
            "List invoices from PayPal. Use this when user wants to see their invoices, "
            "check invoice status, find unpaid/overdue invoices, or get an overview of outstanding payments."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "status_filter": {
                    "type": "string",
                    "description": "Optional status to filter by: DRAFT, SENT, PAID, UNPAID, CANCELLED, REFUNDED. Leave empty for all.",
                },
            },
            "required": [],
        },
    },
    {
        "name": "send_payment_reminder",
        "description": (
            "Send a payment reminder for a specific invoice. Use when user wants to follow up "
            "or remind a client about an unpaid invoice."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "invoice_id": {
                    "type": "string",
                    "description": "The PayPal invoice ID to send a reminder for.",
                },
            },
            "required": ["invoice_id"],
        },
    },
    {
        "name": "get_revenue_summary",
        "description": (
            "Get a summary of transactions and revenue for a specific date range. "
            "Use when user asks about income, revenue, earnings, money received, payment history, "
            "or financial summaries for any time period."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "Start date in format YYYY-MM-DDTHH:MM:SSZ (e.g. 2026-11-01T00:00:00Z)",
                },
                "end_date": {
                    "type": "string",
                    "description": "End date in format YYYY-MM-DDTHH:MM:SSZ (e.g. 2026-11-30T23:59:59Z)",
                },
            },
            "required": ["start_date", "end_date"],
        },
    },
    {
        "name": "cancel_invoice",
        "description": "Cancel an existing invoice that has been sent. Use when user wants to void or cancel an invoice.",
        "parameters": {
            "type": "object",
            "properties": {
                "invoice_id": {
                    "type": "string",
                    "description": "The PayPal invoice ID to cancel.",
                },
            },
            "required": ["invoice_id"],
        },
    },
]
