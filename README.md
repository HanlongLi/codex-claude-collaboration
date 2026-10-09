# Codex–Claude Collaboration

A shared skill for Codex and Claude Code: review important decisions independently, compare evidence, then implement with clear ownership.

## What it does

- Starts from a shared brief: the user's purpose (new ideas, review, experiments, implementation, or other), target problem, venue, risk appetite, and resources. Agents ask for missing fields in one question and do not start work until the brief is complete.
- Separates idea generation from filtering, so candidates are not just the residue that survives prior-art review.
- Reviews research novelty, generality, value, and contribution separately.
- Encourages independent judgments and explicit disagreements before consensus.
- Assigns separate code ownership to avoid conflicting edits.
- Coordinates through a shared Markdown dialogue, including human messages.
- Detects appended text, insertions, edits, and truncation without relying on speaker headings.
- Preserves decisions, evidence, and unfinished work when either agent becomes unavailable.

This is a workflow skill, not an agent launcher or background messaging service. You run each agent yourself and give both access to the same project and dialogue file. Each agent needs its own account/access; this repository does not provide either product.

## Install

The commands below target macOS or Linux. You need Git and Python 3. The dialogue helper uses only Python's standard library; its append locking uses Unix `fcntl`.

### Both Codex and Claude Code

Keep one checkout and link it into Claude's skills directory:

```sh
mkdir -p ~/.codex/skills ~/.claude/skills
git clone https://github.com/HanlongLi/codex-claude-collaboration.git \
  ~/.codex/skills/codex-claude-collaboration
ln -s ~/.codex/skills/codex-claude-collaboration \
  ~/.claude/skills/codex-claude-collaboration
```

These commands assume the destination skill directories do not already exist. If you already installed the skill, update the existing checkout instead. If your Codex installation uses a custom skills location, substitute that location and point the symlink to it.

### One agent only

For Codex alone, run the `mkdir` and `git clone` commands above and omit the symlink. For Claude Code alone:

```sh
mkdir -p ~/.claude/skills
git clone https://github.com/HanlongLi/codex-claude-collaboration.git \
  ~/.claude/skills/codex-claude-collaboration
```

## Use

Open the same project in both agents. Invoke the skill in each agent with the same dialogue path and objective.

**Codex:**

```text
$codex-claude-collaboration
Collaborate with Claude Code on this project using docs/dialogue.md.
Purpose: generate new research directions (or: review these ideas / design
experiments / implement the accepted direction).
Target: <problem or capability, and what success looks like>.
Venue and timeline: <venue, deadline>. Risk: <safe empirical / high-novelty bet>.
Resources: <exact hardware, compute, data, staff time>.
```

**Claude Code:**

```text
/codex-claude-collaboration
Collaborate with Codex on this project using docs/dialogue.md.
Purpose: generate new research directions (or: review these ideas / design
experiments / implement the accepted direction).
Target: <problem or capability, and what success looks like>.
Venue and timeline: <venue, deadline>. Risk: <safe empirical / high-novelty bet>.
Resources: <exact hardware, compute, data, staff time>.
```

Any brief fields you leave out, the agents will ask for in a single question before starting. They record the brief in the dialogue so both agents work from the same one; if you correct something later, they append an updated brief.

If the newly installed skill is not visible, start a new agent session. The skill defaults to `docs/dialogue.md` when no existing path is specified. Ask both agents to watch that file during an active discussion; monitoring stops when their turns end or you wrap up. Agents on different machines need a shared filesystem or another explicitly arranged way to exchange the file. Separate Git clones alone do not synchronize live dialogue.

For wrap-up, say:

```text
Wrap up now. Record decisions, evidence, ownership, running jobs, and the next
concrete step in a handoff. Stop monitoring the dialogue.
```

## Included files

- [SKILL.md](SKILL.md): instructions loaded by either agent.
- [Review and handoff templates](references/review-and-handoff.md): research review, ownership, and session handoff.
- [Dialogue helper](scripts/dialogue.py): snapshot reads, explicit acknowledgments, and timestamped appends. Usage examples are in the skill.
- [Codex metadata](agents/openai.yaml): display name and default prompt.

The helper requires a separate local cursor for each agent. Reading does not mark content as consumed; the agent acknowledges a snapshot only after reading it. Concurrent appends are protected among writers using the helper; unrelated editors do not necessarily honor its lock.

## Update

For the shared installation:

```sh
git -C ~/.codex/skills/codex-claude-collaboration pull --ff-only
```

The Claude symlink sees the same updated files. Preserve any local modifications before updating. For a Claude-only installation, substitute its directory.

## License

[MIT](LICENSE).
