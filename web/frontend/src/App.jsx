import { useGame } from "./useGame";

export default function App() {
  const { game, loading, error } = useGame();

  if (loading) return <p style={{ padding: 32 }}>Loading...</p>;
  if (error)
    return (
      <p style={{ padding: 32 }}>Error: {error} — is the backend running?</p>
    );

  return (
    <div>
      <h1>Cambio</h1>
      <pre>{JSON.stringify(game, null, 2)}</pre>
    </div>
  );
}
