# Reliable dialogue

The helper uses Python standard-library code and Unix locking (macOS/Linux). Read this when first using it or when usage is uncertain.

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

During explicitly requested active discussion, reread at bounded intervals, typically 2–5 minutes; use shorter intervals only when rapid exchange is needed and requested, while continuing useful work. Use available wait tools; the helper is not a background service. Do not promise monitoring after the turn ends. Stop polling when the user wraps up or cancels discussion. Record any outstanding request in the handoff instead of waiting indefinitely without a reason.

Default collaboration is milestone-based: do not poll an idle peer. The current helper accepts only Codex and Claude speaker labels; other integrations need an identity update and verification before claiming support.
