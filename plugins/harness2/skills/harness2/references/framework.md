# The Harness² framework

Harness² (Xu et al., 2026, arXiv:2610.14224) is a plug-and-play framework for
recursive agent harnessing in an open world. It connects two levels of
recursion while keeping model weights fixed.

## Task-level recursion: Propose–Probe–Compose

For one task, refine the execution harness through a contrastive step:

1. **Propose.** A harness editor reads the task, the base harness, and execution
   evidence, then edits the harness tree in place. Two dimensions are proposed
   separately:
   - **INV (invariant)** — procedure, tool use, completion, artifact safety. No
     subject-matter rules.
   - **DOM (domain)** — the practitioner model: the deliverable and its audience,
     controlling sources, required structure, consistency relationships, expert
     omissions. No procedure rules.
2. **Probe.** Each candidate harness executes the *same* task. Nothing is graded;
   the comparison is between behaviours and outputs.
3. **Compose.** From the contrasts across the pool (often a mixed pool of
   unmodified and adapted harnesses, ids shuffled), produce the refined harness.

The loop is repeated with a budget `k`:

- **Sequential recursion** — `k` successive steps; each carries the refined
  harness and accumulated evidence forward. Refines deeper.
- **Parallel recursion** — probe `k` general and `k` domain-specific candidates,
  then produce `k` compositions from the shared evidence. Explores wider.

If the evidence argues for no change, the base harness is kept. That is an
outcome, not a failure: an unsupported adaptation is a regression.

## Harnessing-level recursion: experience reflection

After a task, a reflector looks at what was adopted and why, extracts
evidence-supported lessons, and updates a persistent **improvement harness**.
The adopted harness and lessons are stored in a per-domain **library**. Tasks in
one domain run in order and read only earlier entries, so later tasks inherit
experience without leaking a task's answers. Libraries are separated by
benchmark, executor, mode, budget, and seed.

## The eight components

| # | Component | Role | Runtime cost |
|---|---|---|---|
| c1 | system prompt | role and procedure | always on |
| c2 | context policy | context assembly / compaction | framework-owned, usually not editable |
| c3 | long-term memory | durable domain facts | always on |
| c4 | tool guidance | how to use the toolset | always on |
| c5 | subagents | delegated, context-isolated work | own context, returns text |
| c6 | guardrails | standing rules | always on |
| c7 | skills | reusable workflows | name+description only, body on demand |
| c8 | scripts / plugins / hooks | deterministic helpers; middleware inside the tool loop | registered, acts inside the loop |

Two families of runtime differ only in where these files live: OpenCode-style
workspaces (`systemprompt.md`, `guardrails.md`, `LongTermMEMORY.md`,
`tool_descriptions/tool_guidance.md`, `skills/`, `sub_agents/`, `scripts/`,
`plugin/`) and Codex-style workspaces (`AGENTS.md`, `.agents/skills/`,
`sub_agents/`, `scripts/`, `.codex/hooks.json`). `harness-components` explains
how to choose between them.

## What stays frozen

The model, its provider, the agent CLI's own tool implementations, and the
runtime's context assembly are infrastructure — not editable components. The
harness is the set of files an evolve loop may edit, declared in a manifest
(`harness.yaml` in this repository).

## Why no scores

The method is designed to work in an open world where tasks are unseen during
harness design, so no grading signal is available at refinement time. Evidence
is the execution itself: what the agent tried, what failed, what the artifact
looks like. Benchmarks, rubrics, and judges exist in this repository (`harness2`,
`harness2-judge`, `harness2-report`) to *measure* a harness after the fact — they
are never visible to the parts that produce one.
