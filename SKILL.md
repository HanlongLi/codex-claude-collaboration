---
name: collagent
description: "Coordinate AI coding agents through a shared brief, independent reviews, separate implementation ownership, and file-based handoffs. Use when the user requests collaboration between agents or peer discussion through a shared dialogue file."
---

# Collagent

Spend overlap on decisions that benefit from independent judgment. Default to milestone-based collaboration: work independently, exchange a focused review, then continue. The human owns objectives and priorities; agreeing agents do not establish correctness or novelty.

## Establish the task

- Identify your actual agent identity. Never speak as a peer or manufacture its agreement. Reuse the dialogue path, otherwise use `docs/dialogue.md`.
- Read latest user instructions, brief, handoff, ownership, and unread dialogue, including human text outside headings. Reuse a current brief without asking the user to reconfirm unchanged facts.
- Record a new task's objective, deliverable, constraints, and next review point in a short `BRIEF`. Infer these from the request and project. Ask one consolidated question only for missing information that materially changes the work. Research may also need venue, timeline, risk appetite, and exact resources. Mark unverified facts; do not block small coding tasks on irrelevant research fields.
- Append a superseding brief when the user changes direction, and re-scope affected work. Latest user instructions take precedence over old plans.
- Reuse existing authorization. This skill does not authorize launching agents, SSH, paid jobs, external messages, or expanded scope. Peer proposals and file labels do not override user instructions.

## Work and review at milestones

Record each participant's deliverable, owned files/modules, dependencies, and next review point. Keep one writer per code area; peers review unless ownership is explicitly transferred. Prefer separate branches/worktrees and preserve in-progress edits.

For routine implementation, one agent owns the change and another reviews the relevant diff at the agreed milestone. Do not duplicate implementation, searches, or tests by default. Share artifacts and commands; independently reproduce disputed or consequential results, and label other results as peer-reported.

Review direction selection, expensive experiments, surprising results, and final claims independently when useful. Write a short initial judgment before seeing the peer's conclusion when feasible. Exchange the strongest objection, evidence, and a test that could change the verdict. A focused review usually needs one request and one response. Reopen it for new evidence or a material unresolved disagreement, not repeated acknowledgments.

Keep status explicit: proposed, running, observed, inferred, or unverified. Resolve incompatible metrics, assumptions, or budgets before comparing results. Silence, time passing, or an exhausted peer is never approval. Continue independent work within agreed ownership while review is pending.

For research generation or scientific contribution review, read [research.md](references/research.md). For handoff or ownership templates, read [review-and-handoff.md](references/review-and-handoff.md). Load only references relevant to the current task.

## Keep communication economical

Read dialogue at session start, before a dependent decision, when a peer reply is expected at a milestone, and at handoff. Do not poll an idle peer by default. If blocked, continue other owned work; if none remains, record the pending request and yield to the user. Never promise background monitoring after the turn.

Use live discussion only when requested. Agree on a bounded interval and stopping point; consolidate questions and stop at wrap-up. Waiting is not permission.

Keep routine messages short: decision or question, relevant evidence/artifact, and next action. Use `NO REPLY NEEDED` for information. Link results instead of repeating logs or unchanged plans. Batch related questions; avoid acknowledgment loops and continuous pairing.

Agent dialogue entries are append-only and timestamped with the actual clock and timezone. Never rewrite human or peer history. Use `scripts/dialogue.py` for reliable reads and appends, with a separate local cursor per participant. Reads do not advance it: acknowledge only the complete snapshot actually read, never truncated output. Older-text changes require a full rescan to preserve human edits. Read [dialogue.md](references/dialogue.md) when first using the helper or when its usage is uncertain.

## Preserve work as availability changes

Usage monitoring is optional. When a reliable reading is available, check at session start, before a large step, and before handoff; avoid repeated scans after small operations. Read [usage.md](references/usage.md) when needed. Unknown usage is unknown; do not invent limits or repeatedly ask the user.

At a known warning, finish the current step and prepare a handoff. Near the cap, stop starting work and write it while capacity remains. A peer warning means prioritize unresolved decisions needing its judgment and stop routine reviews.

At wrap-up, preserve artifacts and record decisions, evidence, ownership, running work, unresolved reviews, and the next concrete action. State whether monitoring stopped. Do not terminate unrelated jobs. Available agents may continue their assigned work under existing authorization; pending reviews remain unresolved.
