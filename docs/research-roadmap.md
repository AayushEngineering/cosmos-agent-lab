# Research roadmap

The long-term ambition is to help people discover reliable new knowledge about nature and build more capable learning systems. Progress should be defined by reproducible results, not by claims of approaching superintelligence.

## Track A — Understand the universe

- Build source-linked maps of major questions in cosmology, physics, chemistry, biology, Earth science, and mathematics.
- Represent claims with provenance, date, uncertainty, competing explanations, and links to primary sources or datasets.
- Generate hypotheses only when assumptions and a possible falsification test are explicit.
- Reproduce small published results before attempting novel discoveries.
- Invite domain experts to review claims and experiments.

**Measures:** source quality, citation accuracy, calibration, reproducibility, expert review, and rate of independently verified findings.

## Track B — Continual learning

- Establish retrieval baselines and curated memory datasets.
- Test retention after long sequences of tasks, not only immediate recall.
- Measure catastrophic forgetting, transfer to new tasks, correction uptake, and resistance to repeated false information.
- Compare append-only memory, summarization, structured knowledge, and retrieval-augmented approaches.
- Version memory snapshots and provide deletion/correction pathways.

**Measures:** retention, transfer, calibration, contradiction handling, provenance fidelity, and retrieval precision/recall.

## Track C — Agentic systems

- Start with read-only tools and narrow task domains.
- Add simulation and sandboxed computation before real-world actions.
- Require approval for external side effects and high-impact decisions.
- Track every tool call, input, output, cost, and failure.
- Compare single-agent systems with workflows and multi-agent systems under matched budgets.

**Measures:** task completion, tool correctness, cost, latency, recovery from errors, policy violations, and human override success.

## Track D — Toward broadly capable intelligence

Treat generality as an empirical research question. Evaluate systems across unfamiliar domains, compositional tasks, long-horizon planning, uncertainty, adversarial settings, and the ability to discover and correct their own mistakes. Do not equate benchmark performance with understanding or consciousness.

Any work that increases autonomy or capability should be paired with proportionate evaluations of misuse potential, loss of control, security, and societal impact. See [safety.md](safety.md).

## First 30-day milestone

1. Add 20 carefully sourced evidence records across at least three scientific domains.
2. Write five hypotheses, each with a feasible falsification test.
3. Create a small benchmark of 20 questions with expert-checked answers and source links.
4. Measure a baseline agent's factual accuracy, calibration, citation quality, and ability to say “I don't know.”
5. Publish failures and corrections alongside successes.
