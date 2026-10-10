# Changelog

Changes are grouped by publication milestone, using the repository's commit history. No numbered releases have been assigned.

## 2026-10-10 — Collagent and reduced coordination overhead

[Implementation commit](https://github.com/HanlongLi/collagent/commit/333a56aa495e4be6b8c6155a4b316ccd45c8923d)

- Renamed the project, skill, UI metadata, and invocation to Collagent. Updated installation and migration instructions.
- Made milestone-based collaboration the explicit default. Agents work within assigned ownership, exchange focused reviews, and avoid idle polling or duplicate implementation, searches, and tests by default.
- Reuse current briefs without reconfirming unchanged facts. Small coding tasks no longer need irrelevant research fields.
- Moved research guidance, dialogue mechanics, and quota-monitoring details into references loaded only when needed.
- Keep routine messages short, batch questions, and link artifacts instead of repeating logs or plans. A focused review usually needs one request and one response; new evidence and unresolved disagreements can justify more.
- For requested live discussion, changed the typical check interval from 15–45 seconds to 2–5 minutes. Faster exchange remains available when needed and requested.
- Made quota monitoring optional and tied checks to useful checkpoints. Unknown readings do not block collaboration or cause repeated requests for usage values.

The dialogue and usage helper implementations were not changed in this milestone. Speaker labels still support Codex and Claude; other-agent integrations remain planned. Append locking, explicit snapshot acknowledgment, full rescans after older-text edits, independent review, and ownership safeguards are preserved.

## 2026-10-09 — Quota monitoring and early handoffs

[Implementation commit](https://github.com/HanlongLi/collagent/commit/267c76b21820e75c24ed7fb746b030f118fc4dab)

- Added `scripts/usage.py` with Codex local session readings, Claude status-line/cache readings, and a manual fallback.
- Added configurable warning and wrap-up thresholds, known reset times, and estimated time to cap.
- Added early warning and handoff instructions so a constrained agent can preserve work before becoming unavailable.
- Expanded the brief and handoff templates to record known limits, their source, and availability.

## 2026-10-09 — First published version

[Initial commit](https://github.com/HanlongLi/collagent/commit/6e3026867c84ce722c9a8ac92cadd0bd2758f2e6)

- Published the shared Codex–Claude workflow: shared briefs, independent idea generation and reviews, separate implementation ownership, evidence tracking, and handoffs.
- Included `scripts/dialogue.py` for timestamped appends, locked writes, complete snapshot reads, separate participant cursors, and explicit acknowledgment.
- Included research review and handoff templates, shared installation instructions, and Codex UI metadata.

## Instruction-size comparison

Counts include the complete `SKILL.md` file, including frontmatter, using Python's whitespace-based `len(text.split())` count.

| Published milestone | Commit | Words | Change from first release |
|---|---|---:|---:|
| First release | `6e30268` | 1,496 | Baseline |
| Quota monitoring | `267c76b` | 1,893 | +26.5% |
| Collagent optimization | `333a56a` | 760 | −49.2% |

The optimized entrypoint is also 59.9% smaller than the quota-monitoring version. This measures initial instruction size, not token counts, total package size, task quality, or subscription-quota savings. Loading references adds context when their guidance is needed. Actual usage savings have not been benchmarked.

[Compare first release with the optimization](https://github.com/HanlongLi/collagent/compare/6e3026867c84ce722c9a8ac92cadd0bd2758f2e6...333a56aa495e4be6b8c6155a4b316ccd45c8923d).
