---
name: harness-components
description: Choose which part of an agent harness to edit — system prompt, guardrails, memory, tool guidance, skills, subagents, scripts, or plugins/hooks — and validate the edit. Use when deciding where a fix belongs, when a skill "never gets used", when a proposed harness edit might be discarded by validation, or when comparing OpenCode-style and Codex-style layouts.
---

# Harness components: cost, reach, and validity

## The cost model

| Form | What it is | When it is in context |
|---|---|---|
| System prompt / guardrails / memory / tool guidance | always-on prose | **every turn** |
| Skill | `skills/<name>/SKILL.md` (OpenCode) or `.agents/skills/<name>/SKILL.md` (Codex) | name + description always; body on demand |
| Subagent | `sub_agents/<name>/AGENT.md` | own context; returns text |
| Script | `scripts/<name>.py` | run on demand via bash |
| Plugin / hook | `plugin/<name>.ts` (OpenCode) or `.codex/hooks.json` (Codex) | registered; acts inside the tool loop |

Always-on prose is the expensive option, and the costliest failure on long tasks
is a run that reasons until the budget is gone and delivers nothing. Prefer, in
this order:

1. **Skill** for anything with a recognisable trigger — the default home for new
   instruction.
2. **Script** for a deterministic operation the agent hand-rolled, got wrong, or
   did slowly.
3. **Subagent** for a bounded investigation whose input is large and whose answer
   is small. It is a bad trade when the output is as large as the input.
4. **Hook / plugin** when a mechanical, recurring problem in the tool loop must
   not be skippable: trimming noisy tool output, appending a hint after a
   recurring error signature, capping a runaway tool, verifying a write right
   after it happens.
5. **Always-on text last**, and only for a short rule that applies to every run.
   If you add some, cut some.

## Layouts

**OpenCode-style** (`harness.yaml` → `components:`):

```text
systemprompt.md                        # c1 role and procedure
guardrails.md                          # c6 standing rules
LongTermMEMORY.md                      # c3 durable domain facts
tool_descriptions/tool_guidance.md     # c4 toolset guidance
skills/<name>/SKILL.md                 # c7 workflow (+ skills/<name>/scripts/*)
sub_agents/<name>/AGENT.md             # c5 delegated role
scripts/<name>.py                      # c7 deterministic helper
plugin/<name>.ts                       # c8 plugin / middleware
```

**Codex-style**:

```text
AGENTS.md                              # the ONLY always-on file; injected whole
.agents/skills/<name>/SKILL.md         # + .agents/skills/<name>/scripts/*
sub_agents/<name>/AGENT.md
scripts/<name>.py
.codex/hooks.json                      # hook schema: PreToolUse, PostToolUse, SessionStart
```

`c2` (context policy) is usually owned by the runtime and is not editable.

## Validation — failures that discard the whole proposal

Validation runs before any rollout, and a harness that fails it is thrown away
entire:

1. **Every skill needs a trigger line.** The skill's directory name must appear
   verbatim in the always-on file, in the same edit:
   `When <the situation this skill handles>, load the \`<name>\` skill.`
   An unnamed skill is never opened — the line is what makes it exist.
2. **No template braces in always-on text.** Those files are rendered through
   Jinja with `StrictUndefined`; a doubled `{{` placeholder or a brace-percent
   statement kills the run before any work starts. Use single braces or words.
3. **Every script you name must ship.** A `scripts/<file>.py` invoked from a
   skill or from always-on text must be in the same proposal; a skill's own
   helper belongs at `skills/<name>/scripts/<file>.py`. A helper dropped loose in
   the skill directory is off the editable surface and silently discarded.
4. **Skill frontmatter.** `name:` matching the directory plus `description:`, or
   the skill is dropped silently at load.
5. **Subagent frontmatter.** OpenCode needs `mode: subagent` plus `description:`.
6. **Never empty the always-on file.** In Codex-style layouts `AGENTS.md` is the
   only always-on file; an empty one is rejected. To pay for a new rule, trim it.

`references/validation-checklist.md` is the copy to walk before returning a
harness.

## Anti-patterns

- A skill that restates the always-on text instead of carrying a procedure.
- A subagent that returns a document as long as its input.
- A hook that blocks a legitimate completion path.
- A "be thorough" rule, or any rule that changes no behaviour.
- Memory holding this task's facts — they are wrong anchors for the next task.
- A component that changes the deliverable's shape: added columns, renamed
  headers, restated derivations inside the artifact. A task's requested value
  must arrive *as a value*, not as a formula or a placeholder.
