---
description: Run one Harness² Propose–Probe–Compose step on the current task and deliver a refined harness plus evidence notes
---

Apply the `harness-refine` skill to the task in this conversation.

Start by restating, in four lines: the task and the exact shape of the
deliverable; the workspace inputs you can actually see; the base harness and its
component layout; the budget (`k`, and `parallel` or `sequential`).

Then:

1. Name the earliest point of divergence for each run you have evidence for, or
   say that no trajectory exists and propose a probe plan first.
2. Propose INV and DOM candidates as complete files, not as descriptions of
   files. Touch only what the evidence requires; `KEEP_BASE` is allowed.
3. State exactly how each candidate gets probed and what you compare. If you
   cannot execute, label the probe as not run.
4. Compose from behavioural contrasts and deliver the complete harness tree, a
   `<notes>` block naming the trajectory moment behind each edit, probe status,
   and what you deliberately did not add.

Never invent a score, rubric, or grader, and never change the shape of what the
task asks the agent to deliver.
