import { useGame } from "./useGame";
import { Hand } from "./components/Hand";

export default function App() {
  const { game, loading, error } = useGame();

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
      <Hand cards={observation.my_cards} label="You" />
    </div>
  );
}
