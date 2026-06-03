export function Card({ card }) {
  if (!card) return <div className="card card--hidden">?</div>;

  const rank = card.slice(0, -1); // "JH" -> "J"
  const suit = card.slice(-1); // "JH" -> "H"

  return (
    <div className="card">
      <span className="card-rank">{rank}</span>
      <span className="card-suit">{suit}</span>
    </div>
  );
}
