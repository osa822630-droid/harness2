# Use Harness² in Claude (web, desktop, and Claude Code)

This repository is also a **Claude plugin marketplace**. Adding it makes the
Harness² method — Propose–Probe–Compose harness refinement, component selection,
harness audits, and experience reflection — available as skills, commands, and
agents inside Claude, with no Python install and no API keys.

## Add the marketplace

**Claude web / desktop app** (no Claude Code, no Python install):

1. Open [Customize → Plugins](https://claude.ai/customize/plugins).
2. Select **Add → Add marketplace**.
3. Choose **Add from a repository** and enter `osa822630-droid/harness2`, or the
   full URL `https://github.com/osa822630-droid/harness2`.
4. Select **Sync** / **Add**. The `harness2` plugin appears under your personal
   marketplaces — open it and select **Add**.

**Claude Code** (optional, same plugin):

```text
/plugin marketplace add osa822630-droid/harness2
/plugin install harness2@harness2
```

If you forked this repository, replace `osa822630-droid` with your own owner.

## What you get

| Component | Name | Use it for |
|---|---|---|
| Skill | `harness2` | Framework overview; the router for everything else |
| Skill | `harness-refine` | One full Propose–Probe–Compose step on a concrete task |
| Skill | `harness-components` | Which of the eight components to edit, and what validation rejects |
| Skill | `harness-audit` | Reviewing an existing harness for waste, dead components, and risk |
| Skill | `harness-reflect` | Carrying lessons across tasks through a domain library |
| Skill | `harness2-cli` | Running the reference implementation and benchmarks locally |
| Command | `/harness2:refine` | Refine the harness for the task in the conversation |
| Command | `/harness2:audit` | Audit the harness in the conversation |
| Command | `/harness2:components` | Recommend the cheapest component for a fix |
| Agent | `harness-proposer` | Writing INV/DOM candidate harnesses from evidence (Cowork and Claude Code) |
| Agent | `harness-composer` | Composing one harness from a candidate pool (Cowork and Claude Code) |

In chat, commands load as skills and Claude applies them when the task fits.
Agents load only in Cowork and Claude Code; chat ignores them without an error.

## Using it

The skills work on whatever you put in the conversation:

- **Paste a harness** (system prompt, guardrails, skills, hooks) and ask what is
  wrong with it — `harness-audit` reports findings ordered by cost, then a
  minimal patch.
- **Describe a task an agent keeps failing**, with the deliverable it should
  produce, and ask for a harness — `harness-refine` runs one full step and
  returns a complete harness tree plus notes.
- **Attach trajectories or artifacts** from a run to ground the edits in
  evidence. With no evidence, the skills label proposals as hypotheses and never
  present a prediction as an observation.
- **Working across several tasks?** Ask for reflection; `harness-reflect` turns
  the adopted harness into lessons and a domain library the next task can read.

The skills follow the paper's rules: no rubric, score, or answer key is used to
choose an edit, `KEEP_BASE` is a valid outcome, and a harness never changes the
shape of what the task asks the agent to deliver.

## Local reference implementation

The plugin does not run Python. To execute real rollouts, judge them, and report
results, install the package from the repository root — see the
[quick start](../README.md#install) and the [setup guide](SETUP.md). The
`harness2-cli` skill summarises the commands:

```bash
uv pip install -e '.[render]'
harness2-demo --output runs/demo --k 2
harness2-setup lab && harness2-check --bench lab
```

## Layout in this repository

```text
.claude-plugin/marketplace.json   # marketplace catalog (name, owner, plugins)
plugins/harness2/
├── .claude-plugin/plugin.json    # plugin manifest — the only file in that folder
├── skills/<name>/SKILL.md        # one folder per skill, name == folder
├── commands/<name>.md            # flat slash commands
├── agents/<name>.md              # subagents (Cowork and Claude Code only)
├── references/ inside a skill    # detail loaded only when needed
├── README.md
└── LICENSE
```

Keep component folders at the plugin root: anything placed inside
`.claude-plugin/` other than `plugin.json` is silently ignored, and a top-level
`bin/` directory stops claude.ai from installing the plugin at all.

## Validate before publishing

```bash
python3 scripts/check_plugin.py          # layout, manifests, frontmatter, README, license
python3 -m unittest tests.test_plugin    # the same check as a regression test
```

If you have Claude Code installed, the upstream validator is stricter about
Claude Code-only fields:

```bash
claude plugin validate ./plugins/harness2
claude plugin validate .
```

## Updating the plugin

Bump `version` in **both** `.claude-plugin/marketplace.json` (the plugin entry)
and `plugins/harness2/.claude-plugin/plugin.json` whenever skills, commands, or
agents change — a marketplace added from a Git repository serves the new version
only after the version changes. Then commit and push; users re-sync the
marketplace from **Customize → Plugins**.
