export default function Landing({ onStart }) {
return (
<div className="screen">
<h1>Stranger Chat</h1>
<p>Chat with random strangers</p>
<button onClick={onStart}>Start Chat</button>
</div>
)
}