export default function MessageBubble({ msg }) {
  return (
    <div className={`bubble ${msg.from}`}>
      <p>{msg.text}</p>
    </div>
  )
}
