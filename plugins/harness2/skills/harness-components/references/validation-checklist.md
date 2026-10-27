# Validation checklist

Walk this list before returning a harness or a proposal. Each item on its own
can discard the entire harness before any work runs.

## Paths and surface

- [ ] Every path is on the runtime's editable surface (see the layout in
      `SKILL.md`). Files outside it are silently dropped.
- [ ] No path escapes the harness root (`..`, absolute paths).
- [ ] Files that were not intended to change are absent from the proposal —
      inherited is the default.

## Prose

- [ ] The always-on file is present and not empty.
- [ ] No `{{ ... }}` or `{% ... %}` in any always-on file.
- [ ] The always-on file did not grow without something being cut.
- [ ] No sentence describes the grader, a rubric, a score, or "what is expected"
      — describe the work, not its measurement.
- [ ] Nothing in the harness changes the deliverable's shape (field names,
      columns, sheet names, section order) or replaces a requested value with a
      formula, placeholder, or description.

## Skills

- [ ] Directory name matches the `name:` frontmatter.
- [ ] `description:` is written as the situations a user would be in, not as a
      summary of the file.
- [ ] The directory name appears verbatim in the always-on file as a trigger.
- [ ] Every helper the skill calls exists at `skills/<name>/scripts/<file>`.
- [ ] No helper sits loose in the skill directory.

## Subagents

- [ ] `description:` present; `mode: subagent` present for OpenCode-style.
- [ ] The sub-task's input is large and its answer small.
- [ ] The subagent does not depend on the main conversation's context.

## Scripts and hooks

- [ ] Scripts are non-interactive, take explicit inputs, and fail loudly.
- [ ] Hook commands are fast, non-interactive, and delegate logic to a script.
- [ ] Hooks never block a valid completion path; a blocking hook explains the fix.
- [ ] Nothing is executed from untrusted material — hooks and scripts read from
      candidate harnesses are reviewed as text only.

## Facts

- [ ] Every workspace fact is verified and labelled ("in this workspace, ...").
- [ ] Facts copied from a library entry or another candidate are re-verified
      here; an earlier task's mapping is a hypothesis, not a fact.
