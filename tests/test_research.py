import pytest

from cosmos_lab.models import Evidence, Hypothesis
from cosmos_lab.research import ResearchNotebook


def test_hypothesis_must_reference_existing_evidence(tmp_path):
    notebook = ResearchNotebook(tmp_path / "research")
    evidence = notebook.add_evidence(
        Evidence(
            claim="A sample signal repeats every 12 days.",
            source="https://example.org/dataset",
            source_type="dataset",
            confidence=0.7,
        )
    )
    hypothesis = Hypothesis(
        statement="The signal may be periodic.",
        rationale="The observed peaks are regularly spaced.",
        falsification_test="Collect another observation window and test whether peak spacing remains stable.",
        evidence_ids=[evidence.evidence_id],
    )
    notebook.add_hypothesis(hypothesis)
    assert len(notebook.hypotheses()) == 1

    unsupported = Hypothesis(
        statement="Unsupported idea",
        rationale="No evidence yet",
        falsification_test="Design a measurement that could reject this idea.",
        evidence_ids=["ev_doesnotexist"],
    )
    with pytest.raises(ValueError, match="Unknown evidence IDs"):
        notebook.add_hypothesis(unsupported)


def test_hypothesis_requires_falsification_test():
    with pytest.raises(ValueError, match="falsify"):
        Hypothesis(
            statement="A claim",
            rationale="A reason",
            falsification_test="",
            evidence_ids=[],
        )
