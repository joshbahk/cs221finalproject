import { Card } from "./Card";

export function TableCenter({ discardTop, deckSize }) {
  return (
    <div className="table-center">
      <div className="table-pile">
        <p className="hand-label">Discard</p>
        <Card card={discardTop} />
      </div>
      <div className="table-pile">
        <p className="hand-label">Deck</p>
        <div className="card card--hidden">{deckSize}</div>
      </div>
    </div>
  );
}
