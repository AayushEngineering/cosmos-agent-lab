"""Run a tiny approval-gated agent without an external model provider.

This deterministic adapter is a teaching example. Replace DemoModel with a tested
provider adapter for real research tasks; keep the allowlist and approval gate.
"""

from pathlib import Path

from cosmos_lab.agent import AgentDecision, ResearchAgent, Tool, ToolRegistry
from cosmos_lab.memory import MemoryStore


class DemoModel:
    def decide(self, *, task, memories, observations, available_tools):
        if not observations:
            return AgentDecision(
                action="tool",
                tool_name="multiply",
                arguments={"left": 6, "right": 7},
            )
        product = observations[-1]["result"]
        return AgentDecision(
            action="answer",
            answer=f"The demo calculation gives {product}.",
            uncertainty="This only demonstrates tool orchestration; it is not a scientific result.",
        )


def main() -> None:
    registry = ToolRegistry()
    registry.register(
        Tool(
            name="multiply",
            description="Multiply two integers.",
            handler=lambda args: int(args["left"]) * int(args["right"]),
            risk="low",
        )
    )
    memory = MemoryStore(Path(".cosmos") / "demo-memory.jsonl")
    agent = ResearchAgent(DemoModel(), registry, memory)

    def ask_for_approval(tool, arguments) -> bool:
        print(f"Agent requests {tool.name} with {dict(arguments)}")
        return input("Approve this tool call? [y/N] ").strip().lower() == "y"

    result = agent.run(
        "Demonstrate a multiplication tool call.",
        allowed_tools={"multiply"},
        approve=ask_for_approval,
        max_steps=3,
    )
    print("Answer:", result.answer)
    print("Uncertainty:", result.uncertainty)
    print("Tool calls:", result.tool_calls)
    print("Saved memory episode:", result.memory_episode_id)


if __name__ == "__main__":
    main()
