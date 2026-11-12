# Cosmos Agent Lab

**An open research lab for evidence-grounded scientific discovery, continual learning, and safe agentic systems.**

Cosmos Agent Lab explores a simple question:

> How can we build increasingly capable agents that help us understand the universe while remaining honest about uncertainty, useful to people, and under meaningful human control?

This repository is a practical starting point—not a claim that artificial general intelligence or superintelligence has been solved. It favors measurable progress over grand claims: traceable evidence, falsifiable hypotheses, reproducible experiments, retained lessons, and bounded tool use.

## What is here

- **Learning journal:** append-only JSONL storage for lessons, outcomes, uncertainty, and concepts. Retrieve relevant past experiences with a transparent lexical baseline.
- **Evidence-linked hypotheses:** structured scientific hypotheses with supporting evidence IDs, confidence, and a test that could falsify the idea.
- **Agent loop:** an adapter-based think/act/observe cycle with a hard step limit, approved tool calls, and automatic persistence of final learning episodes.
- **Bounded tools:** a small tool registry that denies unregistered tools and requires an explicit approval callback before execution.
- **Research discipline:** templates and principles for evaluating ideas, documenting negative results, and avoiding unsupported conclusions.
- **Safety-first defaults:** no network access, shell access, self-modifying code, autonomous deployment, or model-provider credentials are included by default.

## Quick start

Requires Python 3.10 or newer. The core package uses only the Python standard library.

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\Activate.ps1

python -m pip install -e ".[dev]"
pytest
```

Add a learning episode:

```bash
cosmos remember \
  --question "What does the cosmic microwave background tell us?" \
  --lesson "It is relic radiation from the early universe and provides evidence for a hot, dense early phase." \
  --uncertainty "This short note is not a substitute for checking current cosmology sources." \
  --concept cosmology --concept CMB
```

Recall related episodes:

```bash
cosmos recall "early universe radiation"
```

The journal is written to `.cosmos/memory.jsonl` by default. Set `COSMOS_MEMORY_PATH` to choose another location. Treat this file as research data: back it up and do not put secrets in it.

Run the approval-gated agent example (it asks before invoking its calculator tool):

```bash
PYTHONPATH=src python examples/basic_agent.py
```

To connect a model, implement the `AgentModel` protocol in `cosmos_lab.agent`. Keep credentials outside the repository, validate every model-generated tool argument, and retain the explicit allowlist and approval gate.

## First principles

1. **Evidence before eloquence.** Separate observations, source-backed claims, assumptions, and speculation.
2. **Falsifiability before confidence.** Important hypotheses need a test that could prove them wrong.
3. **Memory is not truth.** Retrieved notes are prior experiences, not automatically verified facts.
4. **Learn from failure.** Store negative results, corrections, and uncertainty—not only successes.
5. **Bound agency.** Tools are opt-in, allowlisted, and approval-gated. Start with read-only capabilities.
6. **Evaluate capability and risk together.** A more capable agent is not automatically a better or safer one.
7. **Keep humans in control.** High-impact actions, external side effects, and deployment require human review.

## Project map

```text
src/cosmos_lab/
  agent.py       Bounded research-agent loop and approval-gated tool execution
  memory.py      Persistent learning journal and lexical recall
  research.py    Evidence records and falsifiable hypotheses
  models.py      Shared data structures
  cli.py         Small command-line interface
  __main__.py    python -m cosmos_lab entry point

docs/
  architecture.md
  research-roadmap.md
  safety.md
  experiment-template.md
tests/
  test_agent.py
  test_memory.py
  test_research.py
```

## Roadmap

See [docs/research-roadmap.md](docs/research-roadmap.md). The intended path is incremental:

1. Reliable evidence and memory.
2. Reproducible task and scientific-reasoning evaluations.
3. A model adapter with transparent provenance and cost tracking.
4. Sandboxed, human-approved experiments.
5. Continual-learning studies that test retention, forgetting, calibration, and transfer.
6. Multi-agent research only when it beats simpler baselines under controlled evaluation.

## Contributing

Start with [CONTRIBUTING.md](CONTRIBUTING.md). Small, testable contributions are preferred. Every proposed capability should include an evaluation and a discussion of failure modes.

## License

MIT. See [LICENSE](LICENSE).
