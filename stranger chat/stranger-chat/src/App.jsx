
import { useState } from 'react'
import Landing from './components/Landing'
import GenderSelect from './components/GenderSelect'
import ChatRoom from './components/ChatRoom'


export default function App() {
const [step, setStep] = useState('landing')
const [gender, setGender] = useState(null)


return (
<div className="app">
{step === 'landing' && <Landing onStart={() => setStep('gender')} />}
{step === 'gender' && (
<GenderSelect
onSelect={(g) => {
setGender(g)
setStep('chat')
}}
/>
)}
{step === 'chat' && <ChatRoom gender={gender} />}
</div>
)
}