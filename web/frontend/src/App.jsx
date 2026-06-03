import { useGame } from "./useGame";
import { Hand } from "./components/Hand";
import { TableCenter } from "./components/TableCenter";
import { ActionPanel } from "./components/ActionPanel";
import { GameLog } from "./components/GameLog";

import "./App.css";

export default function App() {
  const { game, loading, error, log, takeAction } = useGame();

  if (loading) return <p style={{ padding: 32 }}>Loading...</p>;
  if (error)
    return (
      <p style={{ padding: 32 }}>Error: {error} — is the backend running?</p>
    );

  const { observation } = game;

  return (
    <div className="game">
      <h1>Cambio</h1>
      <Hand cards={observation.opponent_cards} label="Opponent" />
      <TableCenter
        discardTop={observation.discard_top}
        deckSize={observation.deck_size}
      />
      <Hand cards={observation.my_cards} label="You" />
      <ActionPanel actions={game.legal_actions} onAction={takeAction} />
    </div>
  );
}
