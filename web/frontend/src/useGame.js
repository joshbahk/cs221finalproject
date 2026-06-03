import { useEffect, useState, useCallback } from "react";

const BASE = "http://127.0.0.1:8000";

export function useGame() {
  const [game, setGame] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [log, setLog] = useState([]);
  const [selectedAgent, setSelectedAgent] = useState("random");
  const [acting, setActing] = useState(false);

  const fetchState = useCallback(async () => {
    try {
      const res = await fetch(`${BASE}/state`);
      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      setGame(await res.json());
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  const takeAction = useCallback(
    async (action) => {
      setActing(true);
      try {
        const res = await fetch(`${BASE}/action`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(action),
        });
        if (!res.ok) throw new Error(`Action failed: ${res.status}`);
        setLog((prev) => [`You: ${action.kind}`, ...prev].slice(0, 20));
        await fetchState();
      } catch (err) {
        setError(err.message);
      } finally {
        setActing(false);
      }
    },
    [fetchState],
  );

  const reset = useCallback(
    async (agent = selectedAgent) => {
      await fetch(`${BASE}/reset?agent=${agent}`, { method: "POST" });
      setLog([`New game vs ${agent}`]);
      await fetchState();
    },
    [selectedAgent, fetchState],
  );

  useEffect(() => {
    fetchState();
  }, [fetchState]);

  return {
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
  };
}
