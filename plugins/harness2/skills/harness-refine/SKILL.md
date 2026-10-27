---
name: harness-refine
description: Run one Harness² Propose–Probe–Compose step on a concrete task, producing a refined harness plus evidence notes. Use when the user wants a harness improved, adapted, or created for a specific task or workspace, or asks to "apply Harness²", "do a harness step", or "fix the harness so the agent stops failing".
---

# Refine a harness for one task

Run the full step. Do not stop after writing prose: the output is a harness tree
plus notes that name the moment each edit answers.

## 0. Establish the base

Collect, and state back to the user in one short block:

- the **task** and the exact shape of the deliverable it asks for;
- the **workspace** — the inputs, their filenames, and any verified facts you
  can already see (columns, units, join keys);
- the **base harness** — its files and the component layout of the runtime
  (OpenCode-style or Codex-style, see `harness-components`);
- the **budget** — one step, or `k` steps; sequential or parallel.

If the workspace is unavailable, say which claims are unverified and keep them
out of the harness. Do not encode guesses.

## 1. Read the evidence and locate divergence

For each run you have, walk the trajectory in order and name the **earliest**
moment where the run stopped matching the request. Classify it:

| Signature | Usual cheapest fix |
|---|---|
| Tool error: bad input, timeout, missing capability, permission, unread output | one bounded fallback + stop condition; a script if the operation repeats |
| Wrote the artifact with the wrong shape (added columns, renamed fields, restated a derivation inside the file) | a short, always-on statement of the deliverable contract, or a skill if it is type-specific |
| Long mechanical loop the agent hand-rolled | a `scripts/` helper |
| Same multi-step procedure rediscovered on every run | a skill with a trigger line |
| Large input, small answer, explored in the main context | a subagent |
| Same warning ignored repeatedly | a hook in the tool loop (Codex `.codex/hooks.json`, OpenCode `plugin/`) |
| Ran out of budget and delivered nothing | cut always-on prose; move procedure into on-demand components |

If there are no trajectories, propose a probe plan before proposing edits, and
label every edit as a hypothesis.

## 2. Propose (two scopes)

Produce candidate harnesses as **complete files**, not as instructions about
files. Work in two scopes and keep them separate:

- **INV candidate(s)** — procedure, tool use, completion, artifact safety. No
  subject-matter rules.
- **DOM candidate(s)** — practitioner knowledge: the artifact contract, the
  controlling sources, the checks a professional applies, the analytic moves.
  No process rules.

For a parallel step with budget `k`, produce `k` candidates per scope. For a
sequential step, produce one per scope and carry the previous step's result.

Rules: files you do not touch are inherited unchanged; deleting a file removes
that component; `KEEP_BASE` is allowed if the evidence argues for nothing.

## 3. Probe

State exactly how each candidate will be exercised on the *same* task, and what
you will compare between runs: where the trajectory diverges, what the artifact
contains, how much context and budget were consumed, whether a deliverable
exists at all.

- If you can execute (a sandbox with bash/files), actually run the task under
  each candidate and compare the results.
- If you cannot execute, mark the probe **not run** and present the proposals as
  a plan. Never present a predicted outcome as an observation.

## 4. Compose

Look at the pool as behavioural contrasts, not as a ranking. Some candidates are
unmodified baselines; ids are arbitrary. Pick an unmodified base if it is as good
— there is no credit for choosing the more elaborate harness.

Adopt only components whose effect you can point at. When combining, re-verify
every workspace fact you copy from another candidate against the evidence in
front of you.

## 5. Deliver

1. **The harness tree**, complete, with paths and full file contents. If you have
   filesystem tools, write the files instead and show the tree.
2. **A `<notes>` block** — one line per change: the file, what changed, and the
   trajectory moment that motivated it. Readable by a person, not applied by a
   machine.
3. **Probe status** — what ran, what did not, and what remains uncertain.
4. **What you deliberately did not add**, and why (context budget paid elsewhere).

Then hand the adopted harness to `harness-reflect` if the user is working
through more than one task.
