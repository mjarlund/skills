# xcode-parallel reference

## Verify on your machine

```bash
tests/selftest.sh --naive   # N worktrees share one simulator: expect failures (the problem)
tests/selftest.sh           # same through xc: expect N/N PASS
```

Both take 3 worktrees by default (`selftest.sh [--naive] [N]`), build a throwaway Swift package fixture in a temp dir, and clean up their worktrees and simulators. First run is slower because the simulator template is warmed once (about 65 s). Needs Xcode 16+ and python3.

## Commands

`xc test | build | run | sim | env | status | reset-sim | gc`. Flags (remembered per worktree): `--project`, `--scheme`, `--platform ios|tvos|watchos|visionos|macos`, `--device`, `--runtime`, `--configuration`. `test` also takes `--only Target/Class/test`, `--plan`, `--parallel`. Extra xcodebuild flags go after `--`. Env: `XC_BUILD_SLOTS`, `XC_DEVICE`, `XC_RUNTIME`.

## Enforce it: the guard hook (recommended)

A skill is only a suggestion. In a trigger test (20 realistic prompts, 3 runs each) the description alone made agents consult the skill in just 4 of 30 runs where it should apply, so an agent in a hurry will often call `xcodebuild` directly. `scripts/xc-guard` is a Claude Code PreToolUse hook that closes that gap:

```bash
python3 scripts/xc guard-snippet     # prints the settings.json hook with the right path; merge into ~/.claude/settings.json
```

When the repo has 2+ git worktrees it denies raw `xcodebuild build|test|archive|...`, `simctl boot|shutdown|erase|delete|clone|create` on anything but the worktree's own simulator, and any `simctl` use of `booted`, and tells the agent to use `xc` instead. Read-only commands (`xcodebuild -list`, `-showBuildSettings`, `simctl list|io|spawn|openurl`) and `simctl install|launch <own UDID>` pass. `XC_GUARD=warn` only warns, `off` disables, `always` also blocks in a single worktree. It fails open on any parse error. Other agents (Cursor, Codex, ...) ignore the hook; for them put one line in the repo's `AGENTS.md`/`CLAUDE.md`: "Build, test and run with the xcode-parallel skill (`xc`); never call xcodebuild or simctl directly."

## Design notes

- Worktree identity is the real path of `git rev-parse --show-toplevel`; state is `~/Library/Caches/xc-parallel/<name>-<hash>/`. Deleting that folder is always safe.
- Locks are `flock` (kernel releases them when a process dies): one per worktree, a machine-wide pool of compile slots, one for template warm-up, one that makes "create simulator then record it" atomic against gc.
- Simulators are cloned from a warmed, shut-down template per device type and runtime (`xcp-template-*`). Per-worktree simulators are named `xcp-<worktree>-<hash>-<platform>`. gc only ever deletes `xcp-*` devices.
- `test` runs `build-for-testing` under a compile slot, then `test-without-building` outside it, so queued builds do not wait on slow test execution.
- Result bundles are summarised with `xcresulttool get test-results summary`.

## Trade-offs and limits

- Each worktree keeps its own DerivedData and simulator: more disk, one cold build per worktree.
- Parallel testing is off by default; Xcode clones simulators for it and leaks them if killed.
- Not isolated: fixed TCP ports, shared paths outside the repo, shared remote test accounts.
- The Xcode MCP server is not isolated either (one Xcode GUI, shared scheme and destination, per-agent approval dialogs); the skill steers agents to the CLI path.
- macOS with a local Xcode only.
