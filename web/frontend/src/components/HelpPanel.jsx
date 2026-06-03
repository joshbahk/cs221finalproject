import { useState } from "react";

const CARD_POWERS = [
  { cards: "7, 8", power: "Peek at one of your own cards" },
  { cards: "9, 10", power: "Peek at one of the opponent's cards" },
  {
    cards: "J, Q",
    power: "Blind swap — swap any card with opponent without looking",
  },
  { cards: "Black K", power: "King swap — look at both cards before swapping" },
  { cards: "Red K", power: "No power, but worth -1 point" },
  { cards: "Joker", power: "Worth 0 points" },
];

export function HelpPanel() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <button className="help-btn" onClick={() => setOpen(true)}>
        ?
      </button>

      {open && (
        <div className="modal-overlay">
          <div className="modal modal--wide">
            <h2 className="modal-title">How to Play</h2>
            <p className="help-text">
              Try to have the lowest total card value. Draw a card each turn and
              either swap it with one in your hand or discard it. Call Cambio
              when you think you have the lowest hand — everyone else gets one
              more turn.
            </p>
            <h3 className="help-subtitle">Card Powers</h3>
            <div className="help-table">
              {CARD_POWERS.map((row, i) => (
                <div key={i} className="help-row">
                  <span className="help-cards">{row.cards}</span>
                  <span className="help-power">{row.power}</span>
                </div>
              ))}
            </div>
            <h3 className="help-subtitle">Scoring</h3>
            <p className="help-text">
              Ace = 1 · Number cards = face value · J/Q/Black K = 10 · Red K =
              -1 · Joker = 0
            </p>
            <button className="action-btn" onClick={() => setOpen(false)}>
              Got it
            </button>
          </div>
        </div>
      )}
    </>
  );
}
