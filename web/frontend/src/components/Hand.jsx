import { Card } from "./Card";

export function Hand({ cards, label, selectableSlots = [], onSelectSlot }) {
  return (
    <div className="hand">
      <p className="hand-label">{label}</p>
      <div className="hand-cards">
        {cards.map((card, i) => (
          <div
            key={i}
            className={`card-wrapper ${selectableSlots.includes(i) ? "card-wrapper--selectable" : ""}`}
            onClick={() => selectableSlots.includes(i) && onSelectSlot?.(i)}
          >
            <Card card={card} />
          </div>
        ))}
      </div>
    </div>
  );
}
