# Update log

What's new and improved in Collagent, newest first.

## October 10, 2026 — Less overhead, smoother teamwork

**New**

- Meet **Collagent**: the new name for Codex–Claude Collaboration. Use `$collagent` in Codex or `/collagent` in Claude Code.

**Improved**

- Agents check in when work is ready for review, keeping routine coordination quieter.
- Shorter messages and focused reviews help avoid repeated discussions and duplicate work.
- Existing task briefs carry forward, so you spend less time reconfirming the same details.
- Small coding tasks use a simpler brief; detailed research guidance loads when needed.
- Main instructions are 49% shorter than the first release, reducing initial instruction context. Actual quota savings have not been measured.
- Live discussions usually check for replies every 2–5 minutes; faster exchange is available when requested.

**Changed**

- Usage monitoring is optional. Missing usage information no longer holds up collaboration.
- Existing installations need the new `collagent` folder name and an updated Claude symlink. Restart agent sessions after updating.

## October 9, 2026 — Earlier warnings, better handoffs

**New**

- Optional usage readings for Codex and Claude Code, with manual values available when needed.
- Configurable warnings as an agent approaches its usage limit.
- Early wrap-up guidance helps save decisions and unfinished work before capacity runs out.

**Improved**

- Handoffs can include known reset times and availability, helping the other agent continue its assigned work.

## October 9, 2026 — First release

**New**

- Collaboration between Codex and Claude Code through a shared dialogue file.
- A shared task brief, independent reviews, and clear ownership of code changes.
- Research idea generation and review templates.
- Reliable dialogue updates and handoffs that preserve decisions and unfinished work.

[View the project history](https://github.com/HanlongLi/collagent/commits/main/).
