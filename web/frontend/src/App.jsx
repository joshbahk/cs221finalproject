import { useGame } from "./useGame";
import { Hand } from "./components/Hand";
import { TableCenter } from "./components/TableCenter";
import { ActionPanel } from "./components/ActionPanel";
import { GameLog } from "./components/GameLog";
import { AgentSelector } from "./components/AgentSelector";
import { GameOver } from "./components/GameOver";
import { HelpPanel } from "./components/HelpPanel";

import "./App.css";

export default function App() {
  const {
    game,
    loading,
    error,
    setError,
    log,
    acting,
    selectedAgent,
    setSelectedAgent,
    takeAction,
    reset,
    revealedSlots,
  } = useGame();

  if (loading) return <p style={{ padding: 32 }}>Loading...</p>;
  if (error)
    return (
      <p style={{ padding: 32 }}>Error: {error} — is the backend running?</p>
    );

  if (game.done)
    return (
      <div className="game">
        <div className="game-header">
          <h1>Cambio</h1>
          <AgentSelector
            selected={selectedAgent}
            onChange={setSelectedAgent}
            onStart={reset}
          />
          <HelpPanel />
        </div>
        <GameOver scores={game.scores} onReset={() => reset(selectedAgent)} />
      </div>
    );

  const { observation } = game;
  const gameInProgress = !game.done && game.observation.turn_count > 0;
  const replaceActions = game.legal_actions.filter(
    (a) => a.kind === "replace_self",
  );
  const selectableSlots = replaceActions.map((a) => a.params.slot);
  const handleSlotSelect = (slot) => {
    const action = replaceActions.find((a) => a.params.slot === slot);
    if (action) takeAction(action);
  };
  const panelActions = game.legal_actions.filter(
    (a) => a.kind !== "replace_self",
  );

  return (
    <div className="game">
      <div className="game-header">
        <h1>Cambio</h1>
        <AgentSelector
          selected={selectedAgent}
          onChange={setSelectedAgent}
          onStart={reset}
          gameInProgress={gameInProgress}
        />
        <HelpPanel />
      </div>
      {error && (
        <div className="error-banner">
          ⚠️ {error}
          <button className="error-dismiss" onClick={() => setError(null)}>
            ✕
          </button>
        </div>
      )}
      <Hand
        cards={observation.opponent_cards}
        label="Opponent"
        revealedSlots={revealedSlots.opponent}
      />
      <TableCenter
        discardTop={observation.discard_top}
        deckSize={observation.deck_size}
      />
      <Hand
        cards={observation.my_cards}
        label="You"
        selectableSlots={selectableSlots}
        onSelectSlot={handleSlotSelect}
      />
      <ActionPanel
        actions={panelActions}
        onAction={takeAction}
        acting={acting}
        revealedSlots={revealedSlots.my}
      />
      <GameLog log={log} />
    </div>
  );
}
