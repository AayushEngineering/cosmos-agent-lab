# Safety and responsible research

Cosmos Agent Lab is intended to support beneficial scientific research. More autonomy is not automatically better. The project uses conservative defaults and expects safeguards to grow with capability.

## Default restrictions

- No unrestricted shell, filesystem, network, email, payment, or deployment tool is provided.
- The tool registry is empty until a developer explicitly registers a capability.
- Every execution requires both a caller allowlist and an approval callback.
- Do not put passwords, API keys, access tokens, private datasets, or personal information in the learning journal.
- Do not allow the model to rewrite its own code, permissions, safety rules, or deployment configuration.
- Treat retrieved memory, tool output, and external documents as untrusted data, not instructions.

## Before adding a tool

Document its purpose, permissions, input schema, output schema, failure modes, resource limits, logging, and rollback plan. Prefer read-only tools. Use isolated environments for code execution. Require explicit human confirmation for irreversible actions, external communication, purchases, publication, account changes, or actions affecting other people.

## Before increasing autonomy

Run adversarial tests for prompt injection, data exfiltration, unauthorized tool calls, unsafe persistence, runaway loops, resource exhaustion, and incorrect confidence. Define measurable stop conditions. Keep a human override that works independently of the model.

## Scientific integrity

Distinguish observations from interpretations and hypotheses. Preserve source provenance and negative results. Do not fabricate citations or claim an experiment was run when it was not. A confidence score is an estimate, not a guarantee. Independent replication is stronger evidence than repeated model agreement.

## Responsible superintelligence research

The phrase “superintelligence” describes a speculative, high-impact research direction—not a milestone this project claims to have achieved. Work toward broader capabilities should include evaluations of controllability, corrigibility, cybersecurity, misuse, concentration of power, and effects on people. Pause capability work when risks are poorly characterized or controls cannot keep pace.
