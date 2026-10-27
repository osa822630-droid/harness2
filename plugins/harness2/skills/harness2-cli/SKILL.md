---
name: harness2-cli
description: Install and run the Harness² CLI from this repository — uv install, harness2-setup, harness2, harness2-judge, harness2-report, harness2-check, harness2-demo, the JobBench/LAB/WorkBuddy benchmarks, recursion budgets, and environment variables. Use when the user wants to run Harness² locally, reproduce a paper experiment, resume a run, or wire it into a pipeline.
---

# Run Harness² from the repository

This plugin works inside Claude with no setup. Use this skill when the user wants
the reference implementation — real rollouts, judging, and reporting — on their
own machine or CI.

## Install

Linux, Python 3.12, and [uv](https://docs.astral.sh/uv/getting-started/installation/):

```bash
uv venv --python 3.12 .venv
source .venv/bin/activate
uv pip install -e '.[render]'
harness2-demo --output runs/demo --k 2
```

The demo runs both recursion modes with deterministic editors and real Python
executions, and needs no model credentials. Use it to confirm an install before
spending API budget.

Model-backed runs also need Node.js 20+, the Google Cloud CLI, and per-benchmark
dependencies (LAB: Pandoc + Poppler; WorkBuddy-Bench: Docker). Then:

```bash
cp .env.example .env            # Vertex AI project + model ids
gcloud auth application-default login
```

Key settings: `HARNESS2_SOLVER_MODEL` and `HARNESS2_IMPROVER_MODEL` (OpenCode
`provider/model` format), `HARNESS2_JUDGE_MODEL` (bare id), `HARNESS2_RUNS_DIR`
(default `runs/`). See `docs/SETUP.md` for authentication alternatives and the
Codex executor.

## One benchmark, end to end

```bash
harness2-setup lab
harness2-check --bench lab
harness2 --bench lab --k 1 --mode parallel \
  --only-domains antitrust-competition --max-tasks 1
harness2-judge --bench lab --k 1 --mode parallel
harness2-report --bench lab --k 1 --mode parallel
```

`--k` is the task-level recursion budget; `--mode` is `parallel` or
`sequential`; `--substrate cx` swaps OpenCode for Codex. Judging and reporting
must use the same benchmark, executor, subset, `--k`, `--mode`, and seed as the
refinement run. Add `--dry-run` to preview task selection without model calls.

| Benchmark | Setup | Notes |
|---|---|---|
| JobBench | `harness2-setup jb` | dataset revision is recorded at download time |
| LAB | `harness2-setup lab` | 1,143 tasks; start with `--only-domains` + `--max-tasks 1` |
| WorkBuddy-Bench | `harness2-setup wb` | also takes `--subset office\|web\|code` |

Helper scripts chain the whole sequence:
`bash scripts/run_lab.sh`, `scripts/run_jobbench.sh`, `scripts/run_workbuddy.sh`
(honour `SUBSTRATE`, `K`, `MODE`, `SUBSET`).

## Cost and safety

- Model-backed runs cost real money. Start with one domain and one task.
- Results land under `runs/` (or `HARNESS2_RUNS_DIR`) with task summaries,
  deliverables, adopted harnesses, reflection notes, and evaluation results.
  Repeat a command to resume; use a fresh output root when changing models or
  task selection, because the saved configuration blocks incompatible resumes.
- Executor network access is unrestricted and Codex runs with its sandbox
  disabled. Before evaluating on a public benchmark, restrict network access to
  the answers and grading criteria, or the measurement is meaningless.

More detail lives in the repository: `docs/SETUP.md`, `docs/BENCHMARKS.md`,
`docs/EXPERIMENTS.md`.
