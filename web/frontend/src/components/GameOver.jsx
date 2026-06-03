export function GameOver({ scores, onReset }) {
  const youWon = scores.you < scores.opponent;
  const tied = scores.you === scores.opponent;

  return (
    <div className="game-over">
      <h2 className="game-over-result">
        {tied ? "Tie!" : youWon ? "You win!" : "You lose"}
      </h2>
      <div className="game-over-scores">
        <div className="score-item">
          <span className="hand-label">You</span>
          <span className="score-value">{scores.you}</span>
        </div>
        <div className="score-item">
          <span className="hand-label">Opponent</span>
          <span className="score-value">{scores.opponent}</span>
        </div>
      </div>
      <button className="reset-btn" onClick={onReset}>
        Play Again
      </button>
    </div>
  );
}
