export function Card({ card }) {
  if (!card) return <div className="card card--hidden">?</div>;
  return (
    <div className="card">
      <span className="card-rank">{card.rank}</span>
      <span className="card-suit">{card.suit}</span>
    </div>
  );
}
