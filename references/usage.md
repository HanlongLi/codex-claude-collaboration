# Optional usage monitoring

Collaboration works without quota telemetry. If a reading is unavailable, record unknown and continue. Ask for manual values only if a decision depends on them or the user requests monitoring. Never guess. Gemini CLI and DeepSeek through OpenCode currently use manual values or unknown status; do not pass their identities to the Codex/Claude usage readers. Subscription quotas and API spending are different limits; never infer one from the other.

Use quota/reset information only when supplied by the user or available tools. Do not invent remaining usage or encode today's limits as permanent facts. Reserve overlap for the highest-impact disagreements, experiment review, and result interpretation; preserve enough capacity for a handoff.

### Watch your own usage limit

Either agent may have the shorter cap. Record known limits in the brief: which agent tends to run out first, window length, and current reset time.

Check your usage with `scripts/usage.py` at session start, before a large step, and before handoff when a reading is useful; do not scan after each small operation. Run it at checkpoints; it is not a background service.

```sh
python3 /path/to/skill/scripts/usage.py codex     # Codex: reads rate-limit events from Codex session logs
python3 /path/to/skill/scripts/usage.py claude    # Claude Code: status line file if configured, else a local cache
python3 /path/to/skill/scripts/usage.py manual --window-start 2026-01-01T10:00+09:00 --window-hours 5 [--used-percent 60]
```

For Claude Code, the documented source is the `rate_limits` field that Claude Code passes to a status line command. If the user's status line saves that JSON to a file, pass it with `--claude-status-file`. Otherwise the helper falls back to an undocumented local cache that may be stale or change format. Check `age_minutes` before trusting any reading. If the level is `unknown`, record that and continue. Use `manual` if values are already supplied, or ask once only when monitoring is requested or a decision depends on the reading. Never guess.

Act on the reported level. The defaults are `warn` at 75% used or an estimated 45 minutes to the cap, and `wrap` at 90% or 20 minutes. The user may set other thresholds.

- **`warn`:** Finish the current step, but do not start new large work, long searches, or expensive jobs. Append a dialogue record with status `USAGE` giving your percent used, reset time, and what you will finish before stopping. Start drafting the handoff.
- **`wrap`:** Stop new work and write the handoff now, using the template, while there is still capacity to finish it. Append it with status `HANDOFF`, and state that monitoring has stopped and give a return time only if known.

When the peer posts a `USAGE` warning, settle at once any question that needs the peer's judgment, and stop sending it routine review requests. Plan to continue your own assigned work alone. The agent with more remaining capacity carries continuing work; the agent with less reserves its usage for decisions that need two independent views. A peer that goes silent after a `USAGE` or `HANDOFF` record has not approved anything.

At wrap-up, stop starting new work, preserve completed and in-progress artifacts, and write a compact handoff using the reference template. Record running jobs and their intended disposition; do not terminate unrelated jobs. State whether discussion monitoring has stopped. The available agent can continue its assigned work under existing authorization, but must preserve unresolved peer-review items for the next overlap.

At the next session, read the latest brief and handoff before working. Confirm the brief and the latest user direction, review unresolved evidence together, then resume separate ownership.

Check whether the observed window has already reset; historical readings do not establish current usage. Time-to-cap estimates extrapolate observed burn rate and are not guarantees.
