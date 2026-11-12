import pytest

from cosmos_lab.memory import MemoryStore
from cosmos_lab.models import LearningEpisode


def test_episode_round_trip_and_recall(tmp_path):
    store = MemoryStore(tmp_path / "memory.jsonl")
    episode = LearningEpisode(
        question="How do stars form?",
        lesson="Stars form as dense regions of molecular clouds collapse under gravity.",
        uncertainty="This is a simplified summary.",
        concepts=["astronomy", "star formation"],
    )
    store.add(episode)

    assert store.all()[0].episode_id == episode.episode_id
    assert store.search("molecular clouds gravity")[0].episode_id == episode.episode_id


def test_empty_query_returns_no_results(tmp_path):
    store = MemoryStore(tmp_path / "memory.jsonl")
    store.add(LearningEpisode(question="Q", lesson="L"))
    assert store.search("!!!") == []


def test_invalid_record_is_reported(tmp_path):
    path = tmp_path / "memory.jsonl"
    path.write_text("not-json\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid memory record"):
        MemoryStore(path).all()
