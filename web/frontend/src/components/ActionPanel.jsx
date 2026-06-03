export function ActionPanel({ actions, onAction }) {
  return (
    <div className="action-panel">
      {actions.map((action, i) => (
        <button key={i} className="action-btn" onClick={() => onAction(action)}>
          {action.kind}
          {action.params &&
            Object.keys(action.params).length > 0 &&
            ` (${Object.values(action.params).join(", ")})`}
        </button>
      ))}
    </div>
  );
}
