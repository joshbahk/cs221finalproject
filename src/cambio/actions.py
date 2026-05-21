from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class Action: 
    kind: str
    params: tuple[tuple[str, Any], ...] = field(default_factory=tuple)

    @staticmethod
    def make(kind: str, **params: Any) -> "Action":
        return Action(kind=kind, params=tuple(sorted(params.items())))

    def get(self, key: str, default=None):
        return dict(self.params).get(key, default)

    def to_json(self) -> dict:
        return {
            "kind": self.kind,
            "params": dict(self.params),
        }