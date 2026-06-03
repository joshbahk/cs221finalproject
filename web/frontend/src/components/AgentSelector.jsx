export function AgentSelector({ selected, onChange, onStart }) {
  const agents = ["random", "expectimax"];
  return (
    <div className="agent-selector">
      <p className="hand-label">Opponent</p>
      <div className="agent-options">
        {agents.map((a) => (
          <button
            key={a}
            className={`agent-btn ${selected === a ? "agent-btn--active" : ""}`}
            onClick={() => onChange(a)}
          >
            {a}
          </button>
        ))}
      </div>
      <button className="reset-btn" onClick={() => onStart(selected)}>
        New Game
      </button>
    </div>
  );
}
