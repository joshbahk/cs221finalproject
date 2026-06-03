import { useState } from "react";

export function AgentSelector({ selected, onChange, onStart, gameInProgress }) {
  const [pendingAgent, setPendingAgent] = useState(selected);
  const [showConfirm, setShowConfirm] = useState(false);

  const handleAgentClick = (a) => {
    setPendingAgent(a);
    if (gameInProgress) {
      setShowConfirm(true);
    } else {
      onChange(a);
      onStart(a);
    }
  };

  const handleNewGame = () => {
    if (gameInProgress) {
      setShowConfirm(true);
    } else {
      onChange(pendingAgent);
      onStart(pendingAgent);
    }
  };

  const handleConfirm = () => {
    setShowConfirm(false);
    onChange(pendingAgent);
    onStart(pendingAgent);
  };

  const handleCancel = () => {
    setShowConfirm(false);
    setPendingAgent(selected);
  };

  const agents = ["random", "expectimax"];

  return (
    <>
      <div className="agent-selector">
        <p className="hand-label">Opponent</p>
        <div className="agent-options">
          {agents.map((a) => (
            <button
              key={a}
              className={`agent-btn ${pendingAgent === a ? "agent-btn--active" : ""}`}
              onClick={() => handleAgentClick(a)}
            >
              {a}
            </button>
          ))}
        </div>
        <button className="reset-btn" onClick={handleNewGame}>
          New Game
        </button>
      </div>

      {showConfirm && (
        <div className="modal-overlay">
          <div className="modal">
            <p className="modal-message">
              Start a new game? Your current game will be lost.
            </p>
            <div className="modal-actions">
              <button className="action-btn" onClick={handleConfirm}>
                Yes, new game
              </button>
              <button className="action-btn" onClick={handleCancel}>
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
