"""Small, serializable data models used throughout Cosmos Agent Lab."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


@dataclass(slots=True)
class LearningEpisode:
    question: str
    lesson: str
    uncertainty: str = ""
    concepts: list[str] = field(default_factory=list)
    outcome: str = "recorded"
    episode_id: str = field(default_factory=lambda: new_id("ep"))
    created_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "LearningEpisode":
        return cls(
            question=str(raw["question"]),
            lesson=str(raw["lesson"]),
            uncertainty=str(raw.get("uncertainty", "")),
            concepts=[str(x) for x in raw.get("concepts", [])],
            outcome=str(raw.get("outcome", "recorded")),
            episode_id=str(raw.get("episode_id") or new_id("ep")),
            created_at=str(raw.get("created_at") or utc_now()),
        )


@dataclass(slots=True)
class Evidence:
    claim: str
    source: str
    source_type: str = "paper"  # paper, dataset, observation, book, documentation, other
    notes: str = ""
    confidence: float = 0.5
    evidence_id: str = field(default_factory=lambda: new_id("ev"))
    recorded_at: str = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.claim.strip():
            raise ValueError("Evidence claim cannot be empty")
        if not self.source.strip():
            raise ValueError("Evidence source cannot be empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Evidence confidence must be between 0 and 1")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class Hypothesis:
    statement: str
    rationale: str
    falsification_test: str
    evidence_ids: list[str]
    confidence: float = 0.3
    hypothesis_id: str = field(default_factory=lambda: new_id("hyp"))
    status: str = "proposed"
    created_at: str = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.statement.strip() or not self.rationale.strip():
            raise ValueError("Hypothesis statement and rationale are required")
        if not self.falsification_test.strip():
            raise ValueError("A hypothesis needs a test that could falsify it")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Hypothesis confidence must be between 0 and 1")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
