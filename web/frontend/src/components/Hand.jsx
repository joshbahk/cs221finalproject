import { Card } from "./Card";

export function Hand({
  cards,
  label,
  selectableSlots = [],
  onSelectSlot,
  revealedSlots = [],
}) {
  return (
    <div className="hand">
      <p className="hand-label">{label}</p>
      <div className="hand-grid">
        {[2, 3, 0, 1].map((i) => (
          <div
            key={i}
            className={`card-wrapper ${selectableSlots.includes(i) ? "card-wrapper--selectable" : ""}`}
            onClick={() => selectableSlots.includes(i) && onSelectSlot?.(i)}
          >
            <Card card={revealedSlots.includes(i) ? cards[i] : null} />
          </div>
        ))}
      </div>
    </div>
  );
}
