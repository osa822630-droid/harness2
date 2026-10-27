---
name: harness-audit
description: Review an existing agent harness for wasted context, dead components, validation failures, deliverable-shape risks, and missing triggers. Use when the user pastes or points at a harness (system prompt, guardrails, skills, subagents, hooks) and asks whether it is good, too long, redundant, safe, or why a skill never activates.
---

# Audit a harness

Produce a findings list ordered by cost, then a minimal patch. Do not rewrite
the harness wholesale — an audit's output is the smallest set of edits that
removes a real defect.

## Read in this order

1. **The always-on file(s).** Estimate their share of the context budget. Flag
   procedure that only matters in a minority of runs; it belongs in a skill.
2. **Every skill.** Does its directory name appear verbatim in the always-on
   text? No trigger line means the skill is dead weight — it is never opened.
   Is the `description` a trigger, or a summary of the file?
3. **Every subagent.** Is its input large and its answer small? If not, it is a
   context tax with no payoff.
4. **Every script and hook.** Is the named file present, on the editable surface,
   and non-interactive? Does a blocking hook have a way out?
5. **Validation.** Walk
   `../harness-components/references/validation-checklist.md`; any failure there
   means the harness never runs at all.
6. **Deliverable risk.** Anything that changes the shape of what the agent
   produces — extra columns, renamed headers, derivations restated inside the
   artifact, a requested value delivered as a formula or placeholder.
7. **Facts.** Are claimed workspace facts anchored and verifiable, or asserted?
   An unverified fact is worse than no fact.

## Report

```text
FINDINGS (highest cost first)
1. <file> — <defect> — <evidence> — <fix>

PATCH
<only the files that change, complete>

RISKS ACCEPTED
<what you left alone and why>
```

Rules:

- Cite the sentence, skill, or hook you are judging. Vague findings get ignored.
- Prefer deletion and relocation over addition. Most over-long harnesses are
  fixed by moving procedure into skills, not by trimming adjectives.
- Never "improve" a harness by adding always-on prose without naming what it
  replaces.
- If the harness is sound, say so and stop. Manufacturing findings to look useful
  is a failure.
