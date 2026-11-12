import pytest

from cosmos_lab.agent import Tool, ToolDeniedError, ToolRegistry


def test_tool_requires_registration_allowlist_and_approval():
    registry = ToolRegistry()
    registry.register(Tool("add", "Add two numbers", lambda args: args["a"] + args["b"]))

    with pytest.raises(ToolDeniedError, match="allowlist"):
        registry.execute("add", {"a": 1, "b": 2}, allowed_tools=set(), approve=lambda *_: True)

    with pytest.raises(ToolDeniedError, match="not approved"):
        registry.execute("add", {"a": 1, "b": 2}, allowed_tools={"add"}, approve=lambda *_: False)

    result = registry.execute(
        "add", {"a": 1, "b": 2}, allowed_tools={"add"}, approve=lambda *_: True
    )
    assert result == 3


def test_unknown_tool_is_denied():
    with pytest.raises(ToolDeniedError, match="not registered"):
        ToolRegistry().execute("shell", {}, allowed_tools={"shell"}, approve=lambda *_: True)

from cosmos_lab.agent import AgentDecision, ResearchAgent
from cosmos_lab.memory import MemoryStore


class TwoStepModel:
    def __init__(self):
        self.calls = 0

    def decide(self, *, task, memories, observations, available_tools):
        self.calls += 1
        if not observations:
            assert "add" in available_tools
            return AgentDecision(action="tool", tool_name="add", arguments={"a": 20, "b": 22})
        assert observations[-1]["result"] == 42
        return AgentDecision(action="answer", answer="The computed result is 42.", uncertainty="Arithmetic only.")


def test_research_agent_uses_tool_and_remembers_answer(tmp_path):
    registry = ToolRegistry()
    registry.register(Tool("add", "Add integers", lambda args: args["a"] + args["b"]))
    memory = MemoryStore(tmp_path / "memory.jsonl")
    agent = ResearchAgent(TwoStepModel(), registry, memory)

    result = agent.run(
        "What is 20 plus 22?",
        allowed_tools={"add"},
        approve=lambda tool, args: tool.name == "add" and args == {"a": 20, "b": 22},
        max_steps=2,
    )

    assert result.answer == "The computed result is 42."
    assert result.tool_calls == 1
    assert memory.all()[-1].lesson == result.answer


def test_research_agent_stops_at_step_limit(tmp_path):
    class EndlessToolModel:
        def decide(self, **kwargs):
            return AgentDecision(action="tool", tool_name="add", arguments={"a": 1, "b": 1})

    registry = ToolRegistry()
    registry.register(Tool("add", "Add integers", lambda args: args["a"] + args["b"]))
    agent = ResearchAgent(EndlessToolModel(), registry, MemoryStore(tmp_path / "memory.jsonl"))
    with pytest.raises(RuntimeError, match="step limit"):
        agent.run("Add", allowed_tools={"add"}, approve=lambda *_: True, max_steps=2)
