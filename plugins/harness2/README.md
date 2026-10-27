# Harness² plugin for Claude

Harness² is a framework for **recursive agent harnessing**: improving everything
around a model — system prompt, guardrails, memory, tool guidance, skills,
subagents, scripts, and plugins — while the model weights stay fixed. This plugin
brings that method into Claude chat, Cowork, and Claude Code as skills, commands,
and agents.

## Use it

Describe the task an agent keeps failing, paste its harness, or attach the
trajectories and artifacts from a run, and ask Claude to improve, refine, or
audit the harness. Claude picks the matching skill:

| Skill | What it does |
|---|---|
| `harness2` | Framework overview and router |
| `harness-refine` | One full Propose–Probe–Compose step for a concrete task |
| `harness-components` | Which component to edit, and what validation will reject |
| `harness-audit` | Review an existing harness for wasted context and dead components |
| `harness-reflect` | Carry lessons across tasks through a domain library |
| `harness2-cli` | Run the reference implementation and benchmarks locally |

Commands, runnable as `/harness2:refine`, `/harness2:audit`, and
`/harness2:components` in Cowork and Claude Code (in chat they load as skills):
`refine`, `audit`, `components`. Agents `harness-proposer` and
`harness-composer` are available in Cowork and Claude Code.

## Data

The plugin is Markdown and JSON only. It sends nothing anywhere, starts no
process, and bundles no connector or MCP server: what you paste or attach is read
in the conversation, and nothing is stored outside it. The reference
implementation in the repository is separate: you install and run it yourself,
and any model calls it makes go from your machine with your own credentials.

## License

Apache-2.0. Harness² is described in arXiv:2610.14224.
