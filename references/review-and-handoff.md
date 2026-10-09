# Review and handoff templates

Use the relevant fields, not a mandatory form for every message. Keep routine updates short.

## Brief

Record it in the dialogue with status `BRIEF` before substantive work. Append a new `BRIEF` record to supersede it; never edit the old one.

- **Purpose:** generate ideas, review ideas or a direction, design experiments, implement, interpret results, review claims, or other (state it).
- **Target and goal:** the problem, task, or capability, and what a successful outcome or deliverable looks like.
- **Venue and timeline:** intended venue or audience, and deadline.
- **Risk appetite:** safe and well-supported, a higher-novelty bet, or a stated mix.
- **Resources:** exact hardware variants, compute, data, staff time, and budget. Mark each item as user-stated or unverified.
- **Existing material and constraints:** current ideas, prior handoffs, lab strengths, and exclusions.
- **Usage limits:** each agent's known cap, window, and reset time; which agent tends to run out first; any custom warn/wrap thresholds.
- **Defaults chosen by the user:** fields the user declined to specify, and the default recorded for each.

Example request to the user, sent as one message: "Before we start, please tell us: (1) whether you want new ideas, a review of existing ideas, or something else; (2) the problem or capability you care about and what success looks like; (3) target venue and deadline; (4) whether you prefer a safe result or a riskier, more novel bet; (5) exact hardware, compute, data, and staff time; (6) if you know them, each agent's usage limits and reset times."

## Independent research review

- **Problem:** Who needs what capability, under which assumptions and constraints? What observable failure is being addressed?
- **Novelty:** Closest primary sources, publication dates, actual mechanisms, and the exact proposed difference. Read the closest methods before giving a strong verdict; use both established and current literature. Mark unverified comparisons.
- **Generality:** Which tasks, embodiments, data regimes, and conditions should benefit? Which assumptions limit transfer? What second setting could test this?
- **Value:** Who benefits, and is the gain worth the data, computation, engineering, or deployment cost?
- **Contribution:** State the smallest defensible scientific or engineering claim. Distinguish a useful implementation from a research contribution.
- **Method:** Inputs, outputs, learned components, objective, training data, inference procedure, and deployment assumptions.
- **Decisive experiment:** Strongest reasonable baselines; matched data/compute; ablations; evaluation metrics and aggregation; independent trials; expected uncertainty; failure criterion. Specify a success threshold before inspecting results where feasible.
- **Strongest objection:** What existing method or simpler explanation could eliminate the contribution?
- **Verdict:** Pursue, investigate one remaining uncertainty, or stop. Include confidence, evidence gaps, and what would change the verdict. The user retains the final direction decision.

For a pair review, preserve each initial verdict and disagreements before recording any joint conclusion. Independent reviews should not become two paraphrases of the same initial proposal.

## Implementation ownership

| Owner | Deliverable | Owned files/modules | Interface/dependency | Machine/job if relevant | Review point |
|---|---|---|---|---|---|
| Codex | ... | ... | ... | ... | ... |
| Claude | ... | ... | ... | ... | ... |

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
- **Availability:** Latest `scripts/usage.py` reading or user-reported limit (percent used, reset time, source, and age); when you expect to return; whether dialogue monitoring is active or stopped.
