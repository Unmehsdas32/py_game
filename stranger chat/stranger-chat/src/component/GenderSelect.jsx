export default function GenderSelect({ onSelect }) {
return (
<div className="screen">
<h2>Select Your Gender</h2>
<button onClick={() => onSelect('male')}>Male</button>
<button onClick={() => onSelect('female')}>Female</button>
</div>
)
}