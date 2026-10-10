# Ownership and handoff templates

Use the relevant fields, not a mandatory form for every message. Keep routine updates short.

## Brief

For a small task, record objective, deliverable, constraints, participants, and next review point in a few sentences. Use the research fields below only when relevant. Reuse a current brief without reconfirming unchanged facts. Append a superseding `BRIEF` for material changes.

- **Purpose:** generate ideas, review ideas or a direction, design experiments, implement, interpret results, review claims, or other (state it).
- **Target and goal:** the problem, task, or capability, and what a successful outcome or deliverable looks like.
- **Venue and timeline:** intended venue or audience, and deadline.
- **Risk appetite:** safe and well-supported, a higher-novelty bet, or a stated mix.
- **Resources:** exact hardware variants, compute, data, staff time, and budget. Mark each item as user-stated or unverified.
- **Existing material and constraints:** current ideas, prior handoffs, lab strengths, and exclusions.
- **Usage limits:** each agent's known cap, window, and reset time; which agent tends to run out first; any custom warn/wrap thresholds.
- **Defaults chosen by the user:** fields the user declined to specify, and the default recorded for each.


## Implementation ownership

| Owner | Deliverable | Owned files/modules | Interface/dependency | Machine/job if relevant | Review point |
|---|---|---|---|---|---|
| Actual agent | ... | ... | ... | ... | ... |
| Actual peer | ... | ... | ... | ... | ... |

Use actual agreements. Do not assign the other agent work and report it as accepted without evidence. Prefer explicit, small ownership boundaries; record transfers when needed.

## Handoff

- **As of:** Actual timestamp and timezone; author.
- **Brief:** Location of the latest `BRIEF` record, and any fields still missing.
- **Latest user decision:** Current objective, scope changes, and stopping instructions, with source location if useful.
- **Direction status:** Accepted, rejected, or unresolved hypotheses; reasons and decisive sources.
- **Evidence:** Observed results with artifact paths, metrics/definitions, commands, and validation status. Identify peer-reported versus reproduced findings.
- **Ownership:** Each agent's current responsibility, modified files or branch, and dependencies.
- **Running work:** Host/job identifiers, outputs, current status as last checked, and whether work should continue. No secrets.
- **Next action:** The smallest concrete step, its owner, and prerequisites.
- **Unresolved review:** Specific question requiring independent judgment; do not imply consensus.
- **Availability:** Known usage reading or user-reported limit with source and age if relevant; return time only if known; whether dialogue monitoring is active or stopped.
