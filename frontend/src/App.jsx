import { useState, useRef, useEffect } from 'react'
import axios from 'axios'
import ReactMarkdown from 'react-markdown'

const API_URL = 'http://localhost:8000'

const QUICK_ACTIONS = [
  { label: '📋 List all invoices', prompt: 'Show me all my invoices' },
  { label: '⚠️ Overdue invoices', prompt: 'Show me all unpaid and overdue invoices' },
  { label: '📊 Revenue this month', prompt: 'Show me my revenue summary for this month' },
  { label: '🔔 Send all reminders', prompt: 'Send payment reminders to all overdue clients' },
]

const SUGGESTIONS = [
  '"Invoice john@email.com $500 for website design"',
  '"How much did I earn last month?"',
  '"Send reminder for invoice INV-001"',
  '"Show all unpaid invoices"',
]

function TypingDots() {
  return (
    <div style={{ display: 'flex', gap: 4, alignItems: 'center', padding: '8px 4px' }}>
      {[0, 1, 2].map(i => (
        <div key={i} style={{
          width: 8, height: 8, borderRadius: '50%', background: '#003087',
          animation: 'bounce 1.2s infinite',
          animationDelay: `${i * 0.2}s`,
        }} />
      ))}
      <style>{`
        @keyframes bounce {
          0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
          40% { transform: scale(1); opacity: 1; }
        }
      `}</style>
    </div>
  )
}

function Message({ msg }) {
  const isUser = msg.role === 'user'
  return (
    <div style={{
      display: 'flex',
      justifyContent: isUser ? 'flex-end' : 'flex-start',
      marginBottom: 16,
      alignItems: 'flex-end',
      gap: 8,
    }}>
      {!isUser && (
        <div style={{
          width: 36, height: 36, borderRadius: '50%',
          background: 'linear-gradient(135deg, #003087 0%, #0070BA 100%)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: 16, flexShrink: 0,
        }}>
          🤖
        </div>
      )}
      <div style={{
        maxWidth: '72%',
        padding: '12px 16px',
        borderRadius: isUser ? '20px 20px 4px 20px' : '20px 20px 20px 4px',
        background: isUser
          ? 'linear-gradient(135deg, #003087 0%, #0070BA 100%)'
          : 'white',
        color: isUser ? 'white' : '#1a1a2e',
        boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
        fontSize: 14,
        lineHeight: 1.6,
      }}>
        {msg.typing ? (
          <TypingDots />
        ) : (
          <ReactMarkdown
            components={{
              p: ({ children }) => <p style={{ margin: '4px 0' }}>{children}</p>,
              ul: ({ children }) => <ul style={{ paddingLeft: 20, margin: '8px 0' }}>{children}</ul>,
              li: ({ children }) => <li style={{ margin: '2px 0' }}>{children}</li>,
              strong: ({ children }) => <strong style={{ color: isUser ? 'white' : '#003087' }}>{children}</strong>,
              code: ({ children }) => (
                <code style={{
                  background: isUser ? 'rgba(255,255,255,0.2)' : '#f0f2f5',
                  padding: '1px 6px', borderRadius: 4, fontSize: 13,
                }}>{children}</code>
              ),
            }}
          >
            {msg.content}
          </ReactMarkdown>
        )}
      </div>
      {isUser && (
        <div style={{
          width: 36, height: 36, borderRadius: '50%',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: 16, flexShrink: 0,
        }}>
          👤
        </div>
      )}
    </div>
  )
}

export default function App() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: `👋 **Welcome to SmartPay Agent!**

I'm your AI-powered PayPal business assistant. I can help you:

- 📄 **Create & send invoices** instantly
- 📊 **Track revenue** and transaction history  
- ⚠️ **Follow up** on overdue payments
- 🔔 **Send payment reminders** to late clients

**Try asking me something like:**
> "Invoice sarah@example.com $750 for social media management"

What would you like to do today?`,
    },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [status, setStatus] = useState('checking')
  const bottomRef = useRef(null)
  const inputRef = useRef(null)

  // Auto-scroll to bottom
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Check backend health with retry
  useEffect(() => {
    const checkHealth = () => {
      axios.get(`${API_URL}/health`, { timeout: 3000 })
        .then(() => setStatus('online'))
        .catch(() => setStatus('offline'))
    }
    checkHealth()
    const interval = setInterval(checkHealth, 5000)
    return () => clearInterval(interval)
  }, [])

  const sendMessage = async (text) => {
    const msgText = text || input.trim()
    if (!msgText || loading) return

    setInput('')

    // Add user message
    const userMsg = { role: 'user', content: msgText }
    setMessages(prev => [...prev, userMsg])

    // Add typing indicator
    const typingId = Date.now()
    setMessages(prev => [...prev, { role: 'assistant', content: '', typing: true, id: typingId }])
    setLoading(true)

    try {
      const history = messages.map(m => ({ role: m.role, content: m.content }))
      const { data } = await axios.post(`${API_URL}/chat`, {
        message: msgText,
        history: history,
      }, { timeout: 60000 })

      setMessages(prev => [
        ...prev.filter(m => m.id !== typingId),
        { role: 'assistant', content: data.response },
      ])
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message;
      setMessages(prev => [
        ...prev.filter(m => m.id !== typingId),
        {
          role: 'assistant',
          content: `❌ **Error:** ${errorMsg}`,
        },
      ])
    }

    setLoading(false)
    inputRef.current?.focus()
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', maxWidth: 900, margin: '0 auto' }}>

      {/* Header */}
      <div style={{
        background: 'linear-gradient(135deg, #003087 0%, #0070BA 100%)',
        padding: '16px 24px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        boxShadow: '0 2px 12px rgba(0,48,135,0.3)',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div style={{ fontSize: 32 }}>💰</div>
          <div>
            <h1 style={{ color: 'white', fontSize: 20, fontWeight: 700, letterSpacing: '-0.3px' }}>
              SmartPay Agent
            </h1>
            <p style={{ color: 'rgba(255,255,255,0.75)', fontSize: 12 }}>
              AI-powered PayPal Business Assistant
            </p>
          </div>
        </div>
        <div style={{
          display: 'flex', alignItems: 'center', gap: 6,
          background: 'rgba(255,255,255,0.15)', padding: '6px 12px', borderRadius: 20,
        }}>
          <div style={{
            width: 8, height: 8, borderRadius: '50%',
            background: status === 'online' ? '#4ade80' : status === 'offline' ? '#f87171' : '#fbbf24',
          }} />
          <span style={{ color: 'white', fontSize: 12, fontWeight: 500 }}>
            {status === 'online' ? 'Connected to PayPal' : status === 'offline' ? 'Backend Offline' : 'Connecting...'}
          </span>
        </div>
      </div>

      {/* Quick Actions */}
      <div style={{
        background: 'white',
        padding: '12px 20px',
        display: 'flex',
        gap: 8,
        overflowX: 'auto',
        borderBottom: '1px solid #e8ecf0',
        flexShrink: 0,
      }}>
        {QUICK_ACTIONS.map(action => (
          <button
            key={action.label}
            onClick={() => sendMessage(action.prompt)}
            disabled={loading}
            style={{
              padding: '6px 14px',
              borderRadius: 20,
              border: '1.5px solid #0070BA',
              background: 'white',
              color: '#003087',
              cursor: loading ? 'not-allowed' : 'pointer',
              fontSize: 13,
              fontWeight: 500,
              whiteSpace: 'nowrap',
              transition: 'all 0.2s',
              opacity: loading ? 0.6 : 1,
            }}
            onMouseEnter={e => { e.target.style.background = '#003087'; e.target.style.color = 'white' }}
            onMouseLeave={e => { e.target.style.background = 'white'; e.target.style.color = '#003087' }}
          >
            {action.label}
          </button>
        ))}
      </div>

      {/* Messages */}
      <div style={{
        flex: 1,
        overflowY: 'auto',
        padding: '20px 20px 8px',
        background: '#f0f2f5',
      }}>
        {messages.map((msg, i) => (
          <Message key={msg.id || i} msg={msg} />
        ))}
        <div ref={bottomRef} />
      </div>

      {/* Input Area */}
      <div style={{
        background: 'white',
        padding: '16px 20px',
        borderTop: '1px solid #e8ecf0',
        flexShrink: 0,
      }}>
        {/* Example suggestions (shown when only 1 message) */}
        {messages.length === 1 && (
          <div style={{ marginBottom: 12 }}>
            <p style={{ fontSize: 12, color: '#888', marginBottom: 8 }}>💡 Try these examples:</p>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
              {SUGGESTIONS.map(s => (
                <button
                  key={s}
                  onClick={() => setInput(s.replace(/"/g, ''))}
                  style={{
                    padding: '4px 10px', borderRadius: 12,
                    border: '1px solid #ddd', background: '#f8f9fa',
                    color: '#555', cursor: 'pointer', fontSize: 12,
                  }}
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}

        <div style={{ display: 'flex', gap: 10, alignItems: 'flex-end' }}>
          <textarea
            ref={inputRef}
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault()
                sendMessage()
              }
            }}
            placeholder='Ask me anything... e.g. "Invoice john@email.com $500 for logo design"'
            rows={1}
            style={{
              flex: 1,
              padding: '12px 16px',
              borderRadius: 24,
              border: '2px solid #e0e4eb',
              fontSize: 14,
              resize: 'none',
              outline: 'none',
              lineHeight: 1.5,
              transition: 'border-color 0.2s',
              fontFamily: 'inherit',
              maxHeight: 120,
              overflowY: 'auto',
            }}
            onFocus={e => e.target.style.borderColor = '#0070BA'}
            onBlur={e => e.target.style.borderColor = '#e0e4eb'}
          />
          <button
            onClick={() => sendMessage()}
            disabled={loading || !input.trim()}
            style={{
              width: 48, height: 48,
              borderRadius: '50%',
              background: loading || !input.trim()
                ? '#c0c0c0'
                : 'linear-gradient(135deg, #003087 0%, #0070BA 100%)',
              border: 'none',
              cursor: loading || !input.trim() ? 'not-allowed' : 'pointer',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: 20,
              transition: 'all 0.2s',
              flexShrink: 0,
              boxShadow: loading || !input.trim() ? 'none' : '0 2px 8px rgba(0,112,186,0.4)',
            }}
          >
            {loading ? '⏳' : '➤'}
          </button>
        </div>
        <p style={{ fontSize: 11, color: '#aaa', marginTop: 8, textAlign: 'center' }}>
          Powered by Google Gemini + PayPal APIs · Sandbox Mode · Press Enter to send
        </p>
      </div>
    </div>
  )
}
