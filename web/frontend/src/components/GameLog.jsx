export function GameLog({ log }) {
  if (!log.length) return null;
  return (
    <div className="game-log">
      {log.map((entry, i) => (
        <p key={i} className="log-entry">
          {entry}
        </p>
      ))}
    </div>
  );
}
