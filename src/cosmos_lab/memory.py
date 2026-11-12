"""A transparent append-only JSONL learning journal with simple lexical recall."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable

from .models import LearningEpisode

_TOKEN_RE = re.compile(r"[a-z0-9]+", re.IGNORECASE)


def _tokens(text: str) -> set[str]:
    return {token.lower() for token in _TOKEN_RE.findall(text) if len(token) > 1}


class MemoryStore:
    """Persist learning episodes without pretending stored notes are verified truth.

    Each line is one independent JSON object. This format is easy to inspect, back up,
    version, and migrate. Concurrent multi-process writes are not coordinated.
    """

    def __init__(self, path: str | Path = ".cosmos/memory.jsonl") -> None:
        self.path = Path(path).expanduser()

    def add(self, episode: LearningEpisode) -> LearningEpisode:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(episode.to_dict(), ensure_ascii=False) + "\n")
        return episode

    def all(self) -> list[LearningEpisode]:
        if not self.path.exists():
            return []
        episodes: list[LearningEpisode] = []
        with self.path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                try:
                    episodes.append(LearningEpisode.from_dict(json.loads(line)))
                except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
                    raise ValueError(f"Invalid memory record at {self.path}:{line_number}") from exc
        return episodes

    def search(self, query: str, limit: int = 5) -> list[LearningEpisode]:
        if limit < 1:
            raise ValueError("limit must be at least 1")
        query_tokens = _tokens(query)
        if not query_tokens:
            return []

        scored: list[tuple[float, int, LearningEpisode]] = []
        for index, episode in enumerate(self.all()):
            haystack = " ".join(
                [episode.question, episode.lesson, episode.uncertainty, *episode.concepts]
            )
            words = _tokens(haystack)
            overlap = len(query_tokens & words)
            if overlap:
                # Jaccard-like score rewards precision, while a tiny recency tie-break
                # keeps newer matching notes visible without dominating relevance.
                score = overlap / len(query_tokens | words)
                scored.append((score, index, episode))
        scored.sort(key=lambda item: (item[0], item[1]), reverse=True)
        return [episode for _, _, episode in scored[:limit]]
