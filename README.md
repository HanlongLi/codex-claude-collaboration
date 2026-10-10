# Collagent

AI agents working together, with less overhead.

Collagent is a workflow skill for shared briefs, independent reviews, separate code ownership, and reliable file-based handoffs. Its default is milestone-based collaboration: agents work independently and exchange focused reviews when there is something worth reviewing.

The dialogue helper accepts distinct participant identities for Codex, Claude Code, Gemini CLI, and DeepSeek through OpenCode. Gemini/OpenCode setup is documented and the shared-file protocol is tested locally; live sessions with those applications have not yet been verified. Run each agent yourself with access to the same project and dialogue file. Collagent does not launch or authenticate agents.

## Use less coordination

- One owner implements each area; a peer reviews the relevant diff at a milestone.
- No routine idle polling, acknowledgment loops, or duplicate implementation/search/test work.
- Reuse the current brief; ask only for missing details that affect the task.
- Load research, dialogue mechanics, and quota-monitoring instructions only when needed.
- Keep messages short and link artifacts instead of repeating logs or plans.
- Quota monitoring is optional; unknown readings do not block collaboration.
- Live discussion is available when requested, with a bounded interval and stopping point.

## Latest update · October 10, 2026

- **Gemini CLI setup:** share the same skill and dialogue with a distinct Gemini identity.
- **DeepSeek through OpenCode:** use DeepSeek models in an agent application that loads skills and runs file tools.
- **Flexible identities:** separate participants and cursors, including multiple sessions of the same agent.
- **Verification:** shared-file tests passed; Gemini/OpenCode live-session checks are still pending.

[Read the full update log →](CHANGELOG.md)

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

## Gemini CLI and DeepSeek

See the [agent setup guide](references/agents.md) for Gemini CLI installation, DeepSeek provider setup in OpenCode, participant identities, and a short live check. Gemini and DeepSeek/OpenCode use manual usage values or unknown status; automatic quota monitoring remains limited to Codex/Claude.

DeepSeek is the model provider; OpenCode supplies the agent tools needed for this workflow. [OpenCode supports DeepSeek](https://opencode.ai/docs/providers/#deepseek) and [skill loading](https://opencode.ai/docs/skills/). [Gemini CLI supports skills](https://geminicli.com/docs/cli/using-agent-skills/).

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
- [Agent setup](references/agents.md): Gemini CLI and DeepSeek through OpenCode.
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
