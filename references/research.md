# Research generation and review

Read only for research directions, experiments, or scientific claims. Scale the effort to the requested scope; ordinary implementation does not require a literature survey.

## Generate before filtering

When the purpose includes generating new directions, separate generation from evaluation:

1. Start from the brief's target problem, not the hardware. Then ask what the available platform makes uniquely possible or uniquely hard.
2. Have each agent independently produce a broad list, typically 10–20 raw ideas, before any prior-art search. Include ideas outside currently popular topics; trending areas are crowded by default.
3. Assign the agents different search regions (for example, one stays near the current literature and the other looks at adjacent fields, older work, or unfashionable problems) so that their agreement carries some independent weight.
4. Only then filter. Read the closest primary sources in full before killing or keeping an idea; abstract-level evidence can wrongly kill ideas as well as wrongly keep them.

Watch for convergence by attrition. If each objection narrows a claim until only a small residue survives, say so explicitly: the survivor is not necessarily the best idea. Report the residue's real ambition, compare it with the user's stated risk appetite, and offer another generation round instead of presenting the residue as the recommendation.

## Review independently

Before a pivotal decision, formulate a short initial judgment independently of the peer's conclusion when feasible. Then exchange the strongest objection, supporting evidence, and a concrete test that could change each judgment. If already exposed to the peer's view, acknowledge that and seek counterevidence rather than claiming independence.

Prioritize joint review of direction selection, expensive experiment design, surprising results, and final claims. Routine installation, implementation, and debugging usually belong to one owner. Do not require continuous pairing or a reply to every progress update.

For research, assess **novelty, generality, value, and contribution separately**. Use the research review template below when relevant. Compare mechanisms against the closest primary sources, including established work under different terminology. A new robot, integration, or parameterization alone does not establish a new contribution. A paper listing a limitation does not prove that solving it is novel. If a direction fails, evaluate alternatives afresh rather than automatically promoting the next idea.

Keep evidence status explicit: proposed, running, observed, inferred, or unverified. Distinguish peer-reported results from independently reproduced results. Attach artifact paths and reproducible commands to consequential claims. Resolve mismatched metrics, coordinate frames, time alignment, aggregation, seeds, or resource budgets before comparing experiments. Do not present correlation as causation or repeated samples as independent trials.

## Research review template


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

