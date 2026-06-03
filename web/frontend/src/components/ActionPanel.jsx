const ACTION_LABELS = {
  draw_deck: "Draw from Deck",
  draw_discard: "Draw from Discard",
  call_cambio: "Call Cambio!",
  discard_drawn: "Discard Drawn Card",
  swap_drawn: "Swap with Hand",
  peek_self: "Peek at My Card",
  peek_opponent: "Peek at Opponent's Card",
  blind_swap: "Blind Swap",
  king_swap: "King Swap",
  use_power: "Use Power",
  pass_power: "Skip Power",
};

export function ActionPanel({ actions, onAction, acting }) {
  return (
    <div className="action-panel">
      {acting && <p className="acting-status">Bot is thinking...</p>}
      {actions.map((action, i) => (
        <button
          key={i}
          className="action-btn"
          onClick={() => onAction(action)}
          disabled={acting}
        >
          {ACTION_LABELS[action.kind] || action.kind}
          {action.params &&
            Object.keys(action.params).length > 0 &&
            ` (${Object.values(action.params).join(", ")})`}
        </button>
      ))}
    </div>
  );
}
