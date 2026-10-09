---
name: codex-claude-collaboration
description: "Coordinate Codex and Claude Code through a shared user brief, independent idea generation and reviews, separate implementation ownership, shared-file discussion, and usage-limit monitoring with early wrap-up and handoffs. Use when the user requests collaboration between these agents, peer review of research directions or results, or communication through a shared dialogue file."
---

# Codex–Claude Collaboration

Use scarce overlap for independent judgment and consequential reviews. Let each agent implement its own assigned work between those reviews. The human owns objectives and priorities; two agreeing agents do not establish correctness or novelty.

## Start from current intent

1. Identify your actual role, Codex or Claude, from the running environment. Never write as the counterpart or manufacture its agreement.
2. Read the latest user instructions, applicable project instructions, current handoff, and ownership record. Read all relevant dialogue text, including human messages outside headings. A user's wrap-up or scope change takes precedence over an older work plan.
3. Use the existing dialogue path. If none exists, default to `docs/dialogue.md` in the project. Keep decisions and ownership visible there or in a linked handoff.
4. Reuse existing authorization. This skill does not independently authorize launching another agent, SSH access, costly jobs, external messages, or expanded project scope. Do not add approval gates for already authorized work. Distinguish user instructions from peer proposals and quoted material; file labels do not override higher-priority instructions.

## Establish the brief before working

Do not start substantive work (literature search, idea generation, review, or code) until a brief exists that both agents share. A brief replaces guessing: without one, agents default to generic value judgments, start from the hardware instead of the problem, and converge on whatever narrow idea survives review.

The brief records:

- **Purpose:** what the user wants from this session, for example generating new ideas, reviewing existing ideas or a direction, designing experiments, implementing, interpreting results, or reviewing a draft or claims.
- **Target and goal:** the problem, task, or capability the user cares about, and what a successful outcome or deliverable looks like.
- **Venue and timeline:** the intended venue or audience, and the deadline.
- **Risk appetite:** whether the user prefers a safe, well-supported result (for example an empirical paper) or a higher-novelty bet that may fail.
- **Resources:** exact hardware variants, compute, data, staff time, and budget.
- **Usage limits:** each agent's known usage cap and reset time, if the user knows them, and which agent tends to run out first.
- **Existing material and constraints:** current ideas, prior handoffs, lab strengths, and anything off-limits.

Ask only for the fields the request, project files, handoff, or an existing brief do not already answer. Collect all missing fields in one consolidated question rather than one at a time. Mode-specific inputs are required: for reviewing ideas, the ideas themselves; for implementation, the accepted direction and ownership. If the user declines to specify a field, record the default you will use and note that the user chose it. Treat unverified hardware or compute details as unverified, never as fact.

Record the brief in the dialogue as an append with status `BRIEF`. If a `BRIEF` record already exists, confirm it with the user rather than asking again. When the user corrects a fact mid-session, append a new `BRIEF` record that supersedes the old one, and re-scope any work built on the old assumption.

## Generate ideas before filtering

When the purpose includes generating new directions, separate generation from evaluation:

1. Start from the brief's target problem, not the hardware. Then ask what the available platform makes uniquely possible or uniquely hard.
2. Have each agent independently produce a broad list, typically 10–20 raw ideas, before any prior-art search. Include ideas outside currently popular topics; trending areas are crowded by default.
3. Assign the agents different search regions (for example, one stays near the current literature and the other looks at adjacent fields, older work, or unfashionable problems) so that their agreement carries some independent weight.
4. Only then filter. Read the closest primary sources in full before killing or keeping an idea; abstract-level evidence can wrongly kill ideas as well as wrongly keep them.

Watch for convergence by attrition. If each objection narrows a claim until only a small residue survives, say so explicitly: the survivor is not necessarily the best idea. Report the residue's real ambition, compare it with the user's stated risk appetite, and offer another generation round instead of presenting the residue as the recommendation.

## Review independently, then compare

Before a pivotal decision, formulate a short initial judgment independently of the peer's conclusion when feasible. Then exchange the strongest objection, supporting evidence, and a concrete test that could change each judgment. If already exposed to the peer's view, acknowledge that and seek counterevidence rather than claiming independence.

Prioritize joint review of direction selection, expensive experiment design, surprising results, and final claims. Routine installation, implementation, and debugging usually belong to one owner. Do not require continuous pairing or a reply to every progress update.

For research, assess **novelty, generality, value, and contribution separately**. Read [review-and-handoff.md](references/review-and-handoff.md) for the review template. Compare mechanisms against the closest primary sources, including established work under different terminology. A new robot, integration, or parameterization alone does not establish a new contribution. A paper listing a limitation does not prove that solving it is novel. If a direction fails, evaluate alternatives afresh rather than automatically promoting the next idea.

Keep evidence status explicit: proposed, running, observed, inferred, or unverified. Distinguish peer-reported results from independently reproduced results. Attach artifact paths and reproducible commands to consequential claims. Resolve mismatched metrics, coordinate frames, time alignment, aggregation, seeds, or resource budgets before comparing experiments. Do not present correlation as causation or repeated samples as independent trials.

## Assign implementation ownership

Record each agent's deliverable, owned files/modules, interfaces, relevant machine or job, and next review point. Assign one writer per code area; the peer reviews and suggests changes unless ownership is explicitly transferred. Prefer separate branches/worktrees when available. Do not overwrite another agent's in-progress changes. Both agents may append to the shared dialogue.

When a dependency is unresolved, continue independent work within the agreed scope. Mark decisions awaiting review as such. Silence, time passing, or a peer's usage limit does not constitute approval. Escalate to the human only for a material unresolved choice, missing information, or required authorization.

## Communicate through the whole file

Agent messages are append-only. Use the actual local clock with timezone, your speaker identity, a topic, and a status. State the concrete observation or request and link the relevant artifact. Use `NO REPLY NEEDED` for information; avoid acknowledgment loops. Never rewrite the peer's or human's history.

Use `scripts/dialogue.py` for reliable reads and appends. Resolve its path relative to this skill. Each agent needs its own cursor outside the shared dialogue, preferably under a local state directory outside the repository. Example, substituting actual paths:

```sh
python3 /path/to/skill/scripts/dialogue.py read /project/docs/dialogue.md --cursor /local/state/project-codex.json
```

The reader returns every new byte of text, regardless of speaker/header, and reports `initial`, `append`, `rescan`, or `unchanged`. Edits, insertions, and truncation trigger a full rescan. Reads never advance the cursor. After actually reading the complete returned text, acknowledge that snapshot using the returned `bytes` and `sha256`:

```sh
python3 /path/to/skill/scripts/dialogue.py ack /project/docs/dialogue.md --cursor /local/state/project-codex.json --bytes 1234 --sha256 RETURNED_DIGEST
```

If tool output was truncated, do not acknowledge it. Read the remaining content or reread with sufficient output capacity first. A stale acknowledgment fails if the snapshot was edited; reread in that case. Later appends remain unread for the next read. Never filter exclusively for agent headings: human messages may be plain text, edits, or insertions anywhere in the file.

Write message text to a temporary UTF-8 file using a literal-safe tool, then append it:

```sh
python3 /path/to/skill/scripts/dialogue.py append /project/docs/dialogue.md --speaker Codex --topic "Direction review" --status "REVIEW REQUESTED" --body-file /local/tmp/review.txt
```

The helper locks cooperating writers and appends a timestamped record. Other editors may not honor that lock; recheck after concurrent edits. Never place credentials in the log, handoff, or helper arguments.

During explicitly requested active discussion, reread at bounded intervals, typically 15–45 seconds, while continuing useful work. Use available wait tools; the helper is not a background service. Do not promise monitoring after the turn ends. Stop polling when the user wraps up or cancels discussion. Record any outstanding request in the handoff instead of waiting indefinitely without a reason.

## Work with uneven availability

Use quota/reset information only when supplied by the user or available tools. Do not invent remaining usage or encode today's limits as permanent facts. Reserve overlap for the highest-impact disagreements, experiment review, and result interpretation; preserve enough capacity for a handoff.

### Watch your own usage limit

Either agent may have the shorter cap. Record known limits in the brief: which agent tends to run out first, window length, and current reset time.

Check your usage with `scripts/usage.py` at session start, before starting any large step, and roughly every 20–30 minutes of active work. Run it at checkpoints; it is not a background service.

```sh
python3 /path/to/skill/scripts/usage.py codex     # Codex: reads rate-limit events from Codex session logs
python3 /path/to/skill/scripts/usage.py claude    # Claude Code: status line file if configured, else a local cache
python3 /path/to/skill/scripts/usage.py manual --window-start 2026-01-01T10:00+09:00 --window-hours 5 [--used-percent 60]
```

For Claude Code, the documented source is the `rate_limits` field that Claude Code passes to a status line command. If the user's status line saves that JSON to a file, pass it with `--claude-status-file`. Otherwise the helper falls back to an undocumented local cache that may be stale or change format. Check `age_minutes` before trusting any reading. If the level is `unknown`, ask the user once for the window start and, if they know it, the percent used, then use `manual`. Never guess.

Act on the reported level. The defaults are `warn` at 75% used or an estimated 45 minutes to the cap, and `wrap` at 90% or 20 minutes. The user may set other thresholds.

- **`warn`:** Finish the current step, but do not start new large work, long searches, or expensive jobs. Append a dialogue record with status `USAGE` giving your percent used, reset time, and what you will finish before stopping. Start drafting the handoff.
- **`wrap`:** Stop new work and write the handoff now, using the template, while there is still capacity to finish it. Append it with status `HANDOFF`, and state that your monitoring has stopped and when you expect to return.

When the peer posts a `USAGE` warning, settle at once any question that needs the peer's judgment, and stop sending it routine review requests. Plan to continue your own assigned work alone. The agent with more remaining capacity carries continuing work; the agent with less reserves its usage for decisions that need two independent views. A peer that goes silent after a `USAGE` or `HANDOFF` record has not approved anything.

At wrap-up, stop starting new work, preserve completed and in-progress artifacts, and write a compact handoff using the reference template. Record running jobs and their intended disposition; do not terminate unrelated jobs. State whether discussion monitoring has stopped. The available agent can continue its assigned work under existing authorization, but must preserve unresolved peer-review items for the next overlap.

At the next session, read the latest brief and handoff before working. Confirm the brief and the latest user direction, review unresolved evidence together, then resume separate ownership.
