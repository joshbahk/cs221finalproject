const SUIT_SYMBOLS = { H: "♥", D: "♦", C: "♣", S: "♠" };
const RED_SUITS = new Set(["H", "D"]);

export function Card({ card }) {
  if (!card) return <div className="card card--hidden"></div>;

  if (card === "JOKER")
    return (
      <div className="card card--joker">
        <span className="card-corner-rank">🃏</span>
        <span className="card-center-suit">🃏</span>
      </div>
    );

  const rank = card.slice(0, -1);
  const suitKey = card.slice(-1);
  const suit = SUIT_SYMBOLS[suitKey] || suitKey;
  const isRed = RED_SUITS.has(suitKey);

  return (
    <div className={`card ${isRed ? "card--red" : "card--black"}`}>
      <div className="card-corner card-corner--top">
        <span className="card-corner-rank">{rank}</span>
      </div>
      <span className="card-center-suit">{suit}</span>
      <div className="card-corner card-corner--bottom">
        <span className="card-corner-rank">{rank}</span>
      </div>
    </div>
  );
}
