---
description: Explain the eight harness components and recommend the cheapest form for a specific fix
---

Apply the `harness-components` skill.

Given the problem described in this conversation, state which of the eight
components (system prompt, context policy, memory, tool guidance, subagents,
guardrails, skills, scripts/plugins) is the cheapest form that actually fixes
it, and why the alternatives are more expensive or less reliable.

Include: the runtime layout the fix belongs in (OpenCode-style or Codex-style),
the exact files to add or edit, the trigger line the always-on file needs, which
helper scripts must ship with it, and which validation rules could discard the
proposal. If the honest answer is "no change is justified", say that.
