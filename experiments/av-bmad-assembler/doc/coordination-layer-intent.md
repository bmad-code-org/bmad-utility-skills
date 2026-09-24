# Coordination Layer — Statement of Intent

## Project Name (working): TaskVault (or AgentQueueLite – simple, descriptive)

We are building **TaskVault**: a minimal, local-first task coordination layer for parallel LLM-agent coding streams. It enables multiple autonomous agents (Claude Code, similar tools, custom loops) to claim discrete work units from a shared bucket without races, duplicates, or machine thrashing—especially for expensive ops (builds, tests, heavy analysis) or items with loose dependencies.

Work items are simple payloads (JSON-serialized dicts: section_id, markdown-ish content, metadata, optional prereq IDs/statuses). SQLite is the sole persistent store for atomic claiming, status, and basic queuing. We vendor the single-file `litequeue.py` (MIT, zero deps beyond stdlib sqlite3, ~5 years hardened) as the queue core—keeping runtime footprint tiny and installation-free.

### Core principles
- **Safe atomic claiming** — Agents invoke a tool/CLI to claim next READY task (or wait). SQLite transactions + explicit done() ensure no double-claims under concurrency.
- **Dual exposure modes**:
  - Non-blocking CLI (`claim-task --non-blocking`): Instant return (task or "none available") — safe against agent-host Bash timeouts.
  - Blocking via MCP wrapper (`wait-and-claim` tool): Persistent connection holds indefinitely until task ready/executes — no client-side kill.
  - Warnings/docs on Bash realities (default 2-min cap, hard 10-min in some agents); push MCP for reliable long waits.
- **Minimal viable plumbing** — FIFO + status (READY → LOCKED → DONE). Optional later: priority, SQL-filtered deps, metrics (litequeue timings), log rotation/pruning.
- **MIT purity** — Everything (vendored litequeue + our code) stays MIT. No riders or restrictions.
- **Non-goals** — Distributed/multi-node, fancy UI/auth/cloud, full orchestration. Single-machine local file is the feature.

### Inspiration sources & gotchas to avoid (lessons from the two closest analogs)
- **agent-task-queue** (Apache 2.0, MCP-focused queue for expensive-op serialization):
  - **Gotcha #1: Shell timeouts kill waiting tasks** — Original CLI version failed because agent Bash tools enforce short timeouts (30–120 s default); queued waits > timeout → abort → agents bypass queue → chaos.
    **Solution we adopt**: MCP-first for blocking to keep connection alive indefinitely (execution timeout only, configurable).
  - **Gotcha #2: Zombie/orphan processes & stale locks** — Agent crashes leave running tasks dangling.
    **Mitigation**: Use litequeue's done() + our own periodic cleanup (or simple timeout on LOCKED → stale).
  - **Gotcha #3: Data-dir volatility** — Default /tmp loses everything on reboot.
    **Mitigation**: Configurable persistent path from day one; warn on /tmp usage.
  - **Other notes**: Good FIFO serialization, multiple queues for isolation, but we skip Gradle/IntelliJ extras—keep it pure Python.

- **mcp_agent_mail** (MIT + OpenAI/Anthropic Rider, coordination with leases/identities/inboxes):
  - **Gotcha #1: Advisory-only leases → conflict chaos** — File reservations warn but don't fully prevent overwrites without hooks; multi-agent still steps on files.
    **Avoidance**: We focus purely on task claiming (not file-level); if deps needed, use status checks—no advisory mess.
  - **Gotcha #2: License rider baggage** — Added ideological restrictions (anti-Anthropic/OpenAI clauses) after starting unlicensed → adoption friction, legal hesitation.
    **Avoidance**: Strict MIT, no riders—max reuse.
  - **Gotcha #3: Hook/install pitfalls** — Pre-commit guards bypassable (--no-verify, env vars); Windows shims fragile; migration pains between versions.
    **Avoidance**: No Git hooks in core; keep install trivial (single script/server).
  - **Gotcha #4: Overlap with task management** — Warnings against using it for queues/tasks (pair with separate tool).
    **Alignment**: We are the separate queue layer—simple, focused.

### Success criteria
A boring, reliable script/server agents call to coordinate without drama. Runs anywhere Python 3.8+ exists (no pip forced), survives restarts, handles dozens of streams on one box. We borrow blocking insights from agent-task-queue, coordination patterns from mcp_agent_mail, but sidestep their gotchas via litequeue simplicity + MIT freedom + explicit timeout awareness.

Built for fast iteration and easy forking—plumbing first, politics zero.
