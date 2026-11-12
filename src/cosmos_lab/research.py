"""Evidence and hypothesis notebook primitives."""

from __future__ import annotations

import json
from pathlib import Path

from .models import Evidence, Hypothesis


class ResearchNotebook:
    """Store source-linked evidence and testable hypotheses as JSONL records."""

    def __init__(self, directory: str | Path = ".cosmos/research") -> None:
        self.directory = Path(directory).expanduser()
        self.evidence_path = self.directory / "evidence.jsonl"
        self.hypotheses_path = self.directory / "hypotheses.jsonl"

    @staticmethod
    def _append(path: Path, record: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    @staticmethod
    def _read(path: Path) -> list[dict]:
        if not path.exists():
            return []
        records = []
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    raise ValueError(f"Invalid research record at {path}:{line_number}") from exc
        return records

    def add_evidence(self, evidence: Evidence) -> Evidence:
        self._append(self.evidence_path, evidence.to_dict())
        return evidence

    def evidence(self) -> list[Evidence]:
        return [Evidence(**record) for record in self._read(self.evidence_path)]

    def add_hypothesis(self, hypothesis: Hypothesis) -> Hypothesis:
        known_ids = {item.evidence_id for item in self.evidence()}
        missing = sorted(set(hypothesis.evidence_ids) - known_ids)
        if missing:
            raise ValueError(f"Unknown evidence IDs: {', '.join(missing)}")
        self._append(self.hypotheses_path, hypothesis.to_dict())
        return hypothesis

    def hypotheses(self) -> list[dict]:
        return self._read(self.hypotheses_path)
