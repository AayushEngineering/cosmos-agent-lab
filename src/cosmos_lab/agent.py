"""A bounded research-agent loop with an explicit tool-permission boundary."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Mapping, Protocol

from .memory import MemoryStore
from .models import LearningEpisode


@dataclass(frozen=True, slots=True)
class Tool:
    name: str
    description: str
    handler: Callable[[Mapping[str, Any]], Any]
    risk: str = "low"  # low, medium, high


class ToolDeniedError(PermissionError):
    """Raised when a tool is not explicitly permitted or approved."""


class ToolRegistry:
    """Execute only explicitly registered tools after an approval decision.

    The registry is empty unless the application developer adds tools. This is not a
    sandbox: tool handlers must still enforce their own resource and input limits.
    """

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if not tool.name or tool.name in self._tools:
            raise ValueError("Tool name must be non-empty and unique")
        self._tools[tool.name] = tool

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._tools))

    def execute(
        self,
        name: str,
        arguments: Mapping[str, Any],
        *,
        allowed_tools: set[str],
        approve: Callable[[Tool, Mapping[str, Any]], bool],
    ) -> Any:
        if name not in allowed_tools:
            raise ToolDeniedError(f"Tool is not on the caller's allowlist: {name}")
        tool = self._tools.get(name)
        if tool is None:
            raise ToolDeniedError(f"Tool is not registered: {name}")
        if not approve(tool, arguments):
            raise ToolDeniedError(f"Execution was not approved: {name}")
        return tool.handler(arguments)


@dataclass(frozen=True, slots=True)
class AgentDecision:
    """One model decision: either request one tool or return a final answer."""

    action: str  # "tool" or "answer"
    answer: str = ""
    uncertainty: str = ""
    tool_name: str = ""
    arguments: Mapping[str, Any] = field(default_factory=dict)


class AgentModel(Protocol):
    """Adapter contract; implement this with a model provider or a deterministic policy."""

    def decide(
        self,
        *,
        task: str,
        memories: list[LearningEpisode],
        observations: list[dict[str, Any]],
        available_tools: tuple[str, ...],
    ) -> AgentDecision:
        """Return the next tool request or final answer."""


@dataclass(frozen=True, slots=True)
class AgentRun:
    answer: str
    uncertainty: str
    tool_calls: int
    memory_episode_id: str


class ResearchAgent:
    """Run a bounded think/act/observe loop and persist the final learning episode."""

    def __init__(self, model: AgentModel, tools: ToolRegistry, memory: MemoryStore) -> None:
        self.model = model
        self.tools = tools
        self.memory = memory

    def run(
        self,
        task: str,
        *,
        allowed_tools: set[str] | None = None,
        approve: Callable[[Tool, Mapping[str, Any]], bool] | None = None,
        max_steps: int = 5,
    ) -> AgentRun:
        if not task.strip():
            raise ValueError("Task cannot be empty")
        if max_steps < 1:
            raise ValueError("max_steps must be at least 1")
        allowed = set(allowed_tools or set())
        approval = approve or (lambda _tool, _arguments: False)
        memories = self.memory.search(task, limit=5)
        observations: list[dict[str, Any]] = []
        tool_calls = 0
        available = tuple(name for name in self.tools.names() if name in allowed)

        for _step in range(max_steps):
            decision = self.model.decide(
                task=task,
                memories=memories,
                observations=list(observations),
                available_tools=available,
            )
            if decision.action == "answer":
                if not decision.answer.strip():
                    raise ValueError("Model returned an empty final answer")
                episode = self.memory.add(
                    LearningEpisode(
                        question=task,
                        lesson=decision.answer,
                        uncertainty=decision.uncertainty,
                        outcome="agent_answer",
                    )
                )
                return AgentRun(
                    answer=decision.answer,
                    uncertainty=decision.uncertainty,
                    tool_calls=tool_calls,
                    memory_episode_id=episode.episode_id,
                )
            if decision.action != "tool":
                raise ValueError(f"Unsupported model action: {decision.action}")

            result = self.tools.execute(
                decision.tool_name,
                decision.arguments,
                allowed_tools=allowed,
                approve=approval,
            )
            observations.append(
                {
                    "tool": decision.tool_name,
                    "arguments": dict(decision.arguments),
                    "result": result,
                }
            )
            tool_calls += 1

        raise RuntimeError(f"Agent reached its {max_steps}-step limit without a final answer")
