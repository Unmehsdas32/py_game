import { useEffect, useState } from 'react'
import MessageBubble from './MessageBubble'
import Controls from './Controls'

export default function ChatRoom({ gender }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [connected, setConnected] = useState(false)

  useEffect(() => {
    // Fake matchmaking logic
    if (gender === 'male') {
      const foundGirl = Math.random() > 0.5
      if (!foundGirl) {
        setMessages([{ from: 'system', text: 'No girls available right now' }])
        return
      }
    }
    setConnected(true)
    setMessages([{ from: 'system', text: 'You are now connected!' }])
  }, [gender])

  const sendMessage = () => {
    if (!input) return
    setMessages([...messages, { from: 'me', text: input }])
    setInput('')
  }

  return (
    <div className="chatroom">
      <div className="messages">
        {messages.map((m, i) => (
          <MessageBubble key={i} msg={m} />
        ))}
      </div>
      {connected && (
        <div className="input-area">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message"
          />
          <button onClick={sendMessage}>Send</button>
        </div>
      )}
      <Controls />
    </div>
  )
}
