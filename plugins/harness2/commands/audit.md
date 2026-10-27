---
description: Audit the harness in this conversation for wasted context, dead components, validation failures, and deliverable-shape risks
---

Apply the `harness-audit` skill to the harness in this conversation.

Read in this order: the always-on file(s) and their share of the context
budget; every skill and whether its name appears verbatim as a trigger; every
subagent and whether its input is large with a small answer; every script and
hook for existence, surface, and escape hatches; the validation checklist; any
edit that changes the shape of the deliverable; any workspace fact that is
asserted rather than verified.

Report `FINDINGS` (highest cost first, each citing the exact sentence or file),
then a `PATCH` containing only the files that change, then `RISKS ACCEPTED`. If
the harness is sound, say so and stop — do not manufacture findings.
