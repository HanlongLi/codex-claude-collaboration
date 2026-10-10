# Agent setup

Use the same project and dialogue file in both participants. Each needs file access, a shell with Python 3, its own identity, and its own local cursor. Start with a pair and agree on ownership and the next review point. This skill does not launch or authenticate agents.

## Gemini CLI

Gemini CLI discovers user skills in `~/.gemini/skills/`. With Collagent already installed for Codex, link the same copy:

```sh
mkdir -p ~/.gemini/skills
ln -s ~/.codex/skills/collagent ~/.gemini/skills/collagent
```

Use this only if the destination does not already exist; preserve existing installations. Substitute the actual checkout path if different. In Gemini CLI, run `/skills reload` and `/skills list`, then ask:

```text
Use the collagent skill to collaborate with Codex through docs/dialogue.md.
Your identity is Gemini; use your own cursor.
Goal: <deliverable>. Ownership: <agreed scope>. Next review: <milestone>.
```

Follow Gemini CLI's skill-activation prompt. Use `--speaker Gemini` when appending through the helper. Do not assume the Codex `$collagent` or Claude `/collagent` invocation works in Gemini CLI.

Source: [Gemini CLI skill management](https://geminicli.com/docs/cli/using-agent-skills/).

## DeepSeek through OpenCode

DeepSeek supplies the model; OpenCode supplies skill loading, file tools, and shell execution. A plain chat session or an API endpoint alone does not perform the shared-file workflow.

OpenCode can discover the existing `~/.claude/skills/collagent` installation. Alternatively, link the checkout at its native user skill path:

```sh
mkdir -p ~/.config/opencode/skills
ln -s ~/.codex/skills/collagent ~/.config/opencode/skills/collagent
```

Use one installation path and preserve existing destinations. In OpenCode, use `/connect` to configure the DeepSeek provider with your API key, then `/models` to select a DeepSeek model available to your account. Enter credentials in the application's provider flow, never the shared dialogue. Ask:

```text
Use the collagent skill to collaborate with Codex through docs/dialogue.md.
Your identity is OpenCode-DeepSeek; use your own cursor.
Goal: <deliverable>. Ownership: <agreed scope>. Next review: <milestone>.
```

Use `--speaker OpenCode-DeepSeek` when appending. The host is OpenCode; record the selected model in the brief rather than presenting DeepSeek as a separately launched agent.

Sources: [OpenCode skills](https://opencode.ai/docs/skills/), [DeepSeek provider setup](https://opencode.ai/docs/providers/#deepseek).

## Verification and limits

The helper is locally tested with Codex, Claude, Gemini, and OpenCode-DeepSeek identities, including separate cursors, concurrent writes, and human-edit rescans. This verifies the shared-file protocol, not each model's behavior. Gemini CLI and OpenCode live sessions have not been tested in the development environment.

For a live check, ask each participant to read a short human note, acknowledge the complete snapshot, append one response using its identity, and read the peer's reply. Confirm separate cursors and no duplicated or overwritten text. Then try one small owned change and a focused review before depending on the integration for larger work.

Automatic quota readers remain limited to Codex/Claude. For Gemini and DeepSeek/OpenCode, use supplied manual limits or mark usage unknown; collaboration continues without telemetry.
