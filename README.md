# Collagent

AI agents working together, with less overhead.

Collagent is a workflow skill for shared briefs, independent reviews, separate code ownership, and reliable file-based handoffs. Its default is milestone-based collaboration: agents work independently and exchange focused reviews when there is something worth reviewing.

The current dialogue helper supports Codex and Claude Code. Broader agent integrations are planned; a shared `SKILL.md` alone does not establish tested support. This skill does not launch agents or run a background messaging service. Run each agent yourself with access to the same project and dialogue file.

## Use less coordination

- One owner implements each area; a peer reviews the relevant diff at a milestone.
- No routine idle polling, acknowledgment loops, or duplicate implementation/search/test work.
- Reuse the current brief; ask only for missing details that affect the task.
- Load research, dialogue mechanics, and quota-monitoring instructions only when needed.
- Keep messages short and link artifacts instead of repeating logs or plans.
- Quota monitoring is optional; unknown readings do not block collaboration.
- Live discussion is available when requested, with a bounded interval and stopping point.

The main skill instructions are approximately 60% shorter by word count than the previous version. This is a reduction in initial instruction size, not a measured subscription-usage saving. To measure actual savings, compare equivalent tasks with the same agent/model setup and record total usage, dialogue checks, review rounds, completion quality, and elapsed time. Shared-file edits still require a full rescan so human messages are not missed.

## Install

Requires Git and Python 3 on macOS/Linux; the dialogue helper uses standard-library code and Unix `fcntl` locking. Each agent needs its own account/access.

Keep one checkout and link it into Claude's skills directory:

```sh
mkdir -p ~/.codex/skills ~/.claude/skills
git clone https://github.com/HanlongLi/collagent.git \
  ~/.codex/skills/collagent
ln -s ~/.codex/skills/collagent ~/.claude/skills/collagent
```

These commands assume the destinations do not exist. If already installed, preserve local modifications and rename/update the existing checkout, then repoint the Claude symlink. Restart agent sessions after changing the installed skill name. The new invocation is `$collagent` in Codex and `/collagent` in Claude Code; existing prompts using the old name need updating. Updating the repository does not automatically rename installed skill directories or repoint existing symlinks.

For Codex alone, omit the symlink. For Claude alone, clone directly into `~/.claude/skills/collagent`. Substitute a custom Codex skills location if needed.

## Start a task

Open the same project in both agents and give them the same dialogue path and objective:

```text
Use collagent to collaborate through docs/dialogue.md.
Goal: <task and deliverable>.
Constraints: <relevant limits>.
Ownership: <who implements which area; peer assignment requires agreement>.
Next review: <diff, decision, or result worth reviewing>.
```

For research, also supply the intended venue/deadline, risk appetite, and relevant resources. Agents ask only for missing details that materially affect the work. They reuse a current brief and append changes when the task changes.

Default communication occurs at milestones. Ask explicitly for live discussion if needed. Monitoring stops when the agent turn ends or you wrap up. Agents on different machines need a shared filesystem or another arranged way to exchange the dialogue; separate Git clones do not synchronize live dialogue.

To stop:

```text
Wrap up now. Record decisions, evidence, ownership, running work,
unresolved reviews, and the next concrete action. Stop dialogue monitoring.
```

## Included files

- [SKILL.md](SKILL.md): concise shared workflow.
- [Research guidance](references/research.md): idea generation and scientific review, loaded for research tasks.
- [Ownership and handoff templates](references/review-and-handoff.md).
- [Dialogue instructions](references/dialogue.md) and [helper](scripts/dialogue.py): snapshot reads, explicit acknowledgments, timestamped appends.
- [Optional usage monitoring](references/usage.md) and [helper](scripts/usage.py): Codex/Claude local readings or manual values; no automatic telemetry for other agents yet.
- [Codex UI metadata](agents/openai.yaml).

Each agent uses a separate local dialogue cursor. Reading does not mark content consumed; acknowledge only after reading the entire snapshot. Concurrent appends lock cooperating helper writers; other editors may not honor that lock. Dialogue remains append-only for agent messages and preserves human edits.

## Update

```sh
git -C ~/.codex/skills/collagent pull --ff-only
```

Preserve local changes first. The Claude symlink sees updates from the shared checkout.

## License

[MIT](LICENSE).
