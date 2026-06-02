import { Card } from "./Card";

export function Hand({ cards, label }) {
  return (
    <div className="hand">
      <p className="hand-label">{label}</p>
      <div className="hand-cards">
        {cards.map((card, i) => (
          <Card key={i} card={card} />
        ))}
      </div>
    </div>
  );
}
