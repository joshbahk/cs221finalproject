import { useEffect, useState } from "react";

export default function App() {
  const [game, setGame] = useState(null);

  async function loadGame() {
    const response = await fetch("http://127.0.0.1:8000/state");

    const data = await response.json();

    setGame(data);
  }

  useEffect(() => {
    loadGame();
  }, []);

  if (!game) {
    return <h1>Loading...</h1>;
  }

  return (
    <div>
      <h1>Cambio</h1>

      <pre>{JSON.stringify(game, null, 2)}</pre>
    </div>
  );
}
