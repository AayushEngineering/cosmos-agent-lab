# Architecture

## Current data flow

```text
Research question
      |
      v
Learning journal <----> lexical recall
      |
      v
Evidence records -----> hypothesis notebook
      |                         |
      +---- source IDs ----------+
                                v
                    falsifiable experiment plan

Agent request -> relevant memory -> model decision -> registered tool -> caller allowlist
                                               |-> human approval -> handler -> observation --+
                                               +-----------------------------------------------+
                                      final answer -> learning journal
```

## Components

### Learning journal

`MemoryStore` appends `LearningEpisode` records to JSONL. Each record preserves the original question, lesson, uncertainty, concepts, outcome, identifier, and timestamp. Recall uses a transparent token-overlap baseline; it is not semantic retrieval and does not establish truth. A future embedding or hybrid index should be evaluated against this baseline rather than replacing it without measurement.

### Evidence notebook

`Evidence` records a claim, a source locator, source type, notes, and a confidence estimate. `Hypothesis` records a proposed explanation, rationale, an explicit falsification test, and IDs of supporting evidence. The notebook rejects hypotheses that point to unknown evidence IDs. It does not automatically verify the contents or quality of a cited source.

### Research-agent loop

`ResearchAgent` asks an injected `AgentModel` for one decision at a time. A decision is either a tool request or a final answer. The agent can make at most `max_steps` decisions; tool output becomes an observation for the next decision. A final answer and its uncertainty are written to the learning journal. The repository provides the adapter contract, not a hosted model implementation, so users can select and evaluate their own provider without coupling the core project to one vendor.

## Tool boundary

`ToolRegistry` starts empty. A tool must be registered, named by the caller's allowlist, and approved by an explicit callback before its handler runs. This is a policy boundary, not a security sandbox. Any real tool integration must additionally validate arguments, constrain resource use, isolate execution, log actions, and protect secrets.

## Proposed model-provider adapter

A future model adapter should implement a narrow interface and receive only the minimum context needed for a task. Keep provider-specific code outside the core package. Read API keys from environment variables or a secrets manager; never commit them, include them in prompts, or store them in memory records. Log provider, model identifier, timestamp, token/cost metadata where available, and evaluation configuration—but not secret values.

## Continual-learning loop

1. Receive a question or task.
2. Retrieve relevant prior episodes and source-linked evidence.
3. Produce a plan with assumptions and uncertainty made explicit.
4. Request approval for any tool action with external side effects.
5. Record the observation, result, and failure modes.
6. Evaluate whether the result is reliable and whether it changes a prior belief.
7. Store a learning episode; promote it to durable knowledge only after review.

This loop improves the agent's context and procedures. It does not update model weights. Weight updates, fine-tuning, or persistent policy changes require a separate, versioned, evaluated process.
