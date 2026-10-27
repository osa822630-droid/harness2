---
name: harness-reflect
description: Carry harness lessons across tasks — extract evidence-supported lessons from an adopted harness, maintain a per-domain library, and update the improvement harness. Use when the user is refining a harness over several tasks, asks what was learned, wants to reuse a previous harness, or wants experience to carry into the next task.
---

# Reflect and carry experience forward

Task-level recursion ends by *adopting* a harness. Harnessing-level recursion
turns that adoption into reusable experience for the next task. Do this only
after a step has actually been adopted or rejected — reflection needs an outcome.

## 1. Reflection

Answer four questions from the evidence, not from the story you told yourself:

1. **What was adopted, and what does the evidence say it bought?** Name the
   trajectory moment or the artifact difference.
2. **What was proposed and rejected?** A rejected candidate is the most reusable
   lesson: it marks a lever that looked right and did not pay.
3. **Which edits were form mistakes rather than content mistakes?** (Wrong
   component: prose where a skill belonged, a subagent for a large output, a hook
   for a one-off.)
4. **Which facts are true of this task only** and must not travel? Label them and
   keep them out of memory.

Write lessons as sentences a future editor can act on:

- Good: "Deliverable-shape failures were fixed by naming the exact column order
  in an on-demand skill, not in always-on text."
- Bad: "Be more careful with structure."

## 2. Library

Store the adopted harness with its lessons in the **per-domain library**. Semantics
that matter:

- A task reads only entries from **earlier tasks in the same domain**, so
  experience accumulates without leaking a task's answers forward.
- Library entries are **examples, not files on disk** where the next harness runs.
  To reuse a component, copy the file into the new harness and **re-verify its
  workspace facts** — an earlier task's mapping or threshold is a hypothesis here.
- Copying a skill without copying its helper script produces a harness that fails
  validation and is thrown away.
- Keep libraries separated by benchmark/executor/mode/budget/seed when you are
  comparing configurations; mixing them destroys reproducibility.

If the user is working in this repository, runs are organized under
`HARNESS2_RUNS_DIR` with per-domain libraries; `harness2-cli` covers the layout.

## 3. Improvement harness

Keep a short, durable **improvement harness**: the lessons that have held across
more than one task, phrased as rules for the next proposer. Cap it. If a lesson
has not paid off twice, it does not belong there — keep it as a note on the
library entry instead.

Typical durable lessons:

- prefer an on-demand skill over always-on prose for anything with a trigger;
- encode verified workspace facts, never guesses;
- never change the deliverable's shape;
- when the evidence is thin, keep the base harness.

## Output

```text
ADOPTED     <harness id> — evidence for it
REJECTED    <candidate> — the lever it tested, and why it did not pay
LESSONS     <1-5 sentences a future editor can act on>
LIBRARY     <domain> ← <entry name> (what a later task should copy, what to re-verify)
IMPROVEMENT HARNESS DELTA
<what you added, what you removed to keep it capped>
```
