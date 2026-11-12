"""Command-line interface for the learning journal."""

from __future__ import annotations

import argparse
import os

from .memory import MemoryStore
from .models import LearningEpisode


def _store() -> MemoryStore:
    return MemoryStore(os.environ.get("COSMOS_MEMORY_PATH", ".cosmos/memory.jsonl"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cosmos", description="Cosmos Agent Lab research journal")
    sub = parser.add_subparsers(dest="command", required=True)

    remember = sub.add_parser("remember", help="append a learning episode")
    remember.add_argument("--question", required=True)
    remember.add_argument("--lesson", required=True)
    remember.add_argument("--uncertainty", default="")
    remember.add_argument("--concept", action="append", default=[])
    remember.add_argument("--outcome", default="recorded")

    recall = sub.add_parser("recall", help="search prior learning episodes")
    recall.add_argument("query")
    recall.add_argument("--limit", type=int, default=5)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    store = _store()
    if args.command == "remember":
        episode = store.add(
            LearningEpisode(
                question=args.question,
                lesson=args.lesson,
                uncertainty=args.uncertainty,
                concepts=args.concept,
                outcome=args.outcome,
            )
        )
        print(f"Saved learning episode: {episode.episode_id}")
    elif args.command == "recall":
        matches = store.search(args.query, limit=args.limit)
        if not matches:
            print("No matching learning episodes found.")
            return
        for episode in matches:
            print(f"\n[{episode.episode_id}] {episode.question}")
            print(f"Lesson: {episode.lesson}")
            if episode.uncertainty:
                print(f"Uncertainty: {episode.uncertainty}")
            if episode.concepts:
                print("Concepts: " + ", ".join(episode.concepts))
