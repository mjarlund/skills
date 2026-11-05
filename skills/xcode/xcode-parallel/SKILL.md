---
name: xcode-parallel
description: Build, test, run and debug Xcode / Swift / iOS projects safely when several coding agents or git worktrees work on the same project at once. Use this skill whenever you are about to run xcodebuild, run tests that need an iOS simulator, use xcrun simctl, boot or pick a simulator, or call the Xcode MCP tools (BuildProject, RunAllTests, RunSomeTests, RunProject, XcodeSwitchRunDestination) - especially in a git worktree session or when other agents may be running. Prevents simulator clobbering, "database is locked" build errors, flaky tests from CPU starvation, and leaked simulators. Use it even if the user does not mention parallel work; a plain "run the tests" or "build the app" in an Xcode project qualifies.
compatibility: macOS with Xcode 16+ and python3 (stdlib only). Not for Linux or CI runners without Xcode.
---

# Parallel-safe Xcode work

**Do this first:** before running `xcodebuild`, `xcrun simctl`, or an Xcode MCP build/run tool (`BuildProject`, `RunAllTests`, `RunSomeTests`, `RunProject`, `XcodeSwitchRunDestination`) in this repo, route it through `xc` instead, even for a single plain "build the app" or "run the tests" with no other agents visible - you cannot tell from inside your own session whether other agents or worktrees are active on the same machine.

Several agents share one Mac, one CoreSimulator service and (if the MCP is used) one Xcode GUI. Measured on 4 concurrent worktrees running the same simulator test against one shared simulator: 3 of 4 failed (state clobbered, "test runner exited before establishing connection"). Through `xc` all passed.

`scripts/xc` (in this skill's directory) gives each git worktree its own DerivedData, its own simulator and its own result bundles, and queues only what truly cannot overlap. It needs no project configuration: it finds the workspace/project/scheme itself and remembers it.

## Default workflow

Invoke the script by its literal path inside this skill's directory (the base directory shown when the skill loaded) with `python3`, from anywhere inside the worktree. Below, `xc` is shorthand for `python3 <skill-dir>/scripts/xc`: write the full path out in every command, for example `python3 ~/.claude/skills/xcode-parallel/scripts/xc test`.

For your own interactive shell only (not for agent tool calls, which must keep using the literal path above - see the harness rules below), put `xc` on `PATH` once: `ln -s <skill-dir>/scripts/xc ~/bin/xc` (create `~/bin` and add it to `PATH` if needed), or add `export PATH="$PATH:<skill-dir>/scripts"` to your shell profile. Without this, `xc` is not found by name; it only exists under `scripts/`.

Worktree-isolated agents run under a harness that refuses commands it cannot prove safe. Parallel runs hit these refusals constantly, so follow all of these from the first call:

- Literal path only: no shell variable for the script (`XC=...; $XC test`), no command substitution in the command name.
- One plain command per call: no `cd dir && ...`, no `;`, no `&&`/`||` chains, no heredocs. Run from the worktree as-is; `xc` finds the repo from any subdirectory.
- Redirect with `> /tmp/x.log 2>&1` and read the log in a second call rather than chaining, but make the path unique to your own run (embed your worktree name or `$$`, e.g. `/tmp/xc-$(git rev-parse --show-toplevel | xargs basename)-$$.log` written out literally, not as a shell variable). A generic name like `/tmp/x.log` or `t1.log` in a shared scratchpad will be overwritten or interleaved by another agent using the same name. `xc` itself never has this problem - every `xc` call writes its own log to a path unique to that worktree and that run, and prints the path at both the start and the end of the run; prefer reading that path over your own redirect when you can.
- Quote globs for zsh (`--include='*.swift'`), or an unmatched glob aborts the command.
- Never delete DerivedData or simulators yourself, and never `pkill`/`killall` (the harness denies it, and the target may be another agent's): `xc gc` cleans up safely and `xc stop` stops your own run.
- `--project`/`--scheme` on `build`/`test`/`run` are one-off for that single call only; they never change the remembered default (even if the call fails), so a wrong guess cannot poison other worktrees. To actually change what every worktree of this repo gets by default, use `xc config set --target build|test --project P --scheme S` (see below).

```bash
xc test                                  # build-for-testing + test, failures summarised
xc test --only MyTests/FooTests/testBar  # narrow runs; repeatable
xc build                                 # compile check
xc run                                   # build, install and launch on the private simulator
xc sim                                   # prints this worktree's simulator UDID (booted)
```

Project docs (AGENTS.md, testing guides) often say to run `xcodebuild test -destination id=<booted simulator>`. Those commands were written for one agent. Keep their scheme and scope but run them through `xc` (`-only-testing:A/B` becomes `--only A/B`, `-scheme X` becomes `--scheme X`), because a booted simulator is shared by every agent on the machine.

Do not call `xcodebuild ... -destination` or `simctl boot booted` yourself, and do not pick a simulator from `simctl list`. Those are the shared resources other agents are using; `xc` hands you a private one. For raw xcodebuild flags, pass them after `--`: `xc build -- -configuration Release`.

Add `--json` to `build`/`test` for a final parseable `XC_RESULT {...}` line (use it when you coordinate other agents); `xc status --all` shows which worktrees are busy.

Builds take minutes and many agent shells time out around 10 minutes, so run anything expected to take over 30 seconds in the background and read the log path it prints instead of re-running. Start it once, then wait for it to finish and report once; ending a turn with a run still going produces repeated "waiting" notices and duplicate reports. Output is already reduced to errors, test failures and a result summary; the full log path is printed at the end.

First use in a worktree creates its simulator by cloning a warmed template (about 5 s). The first use on the whole machine warms that template once (about 65 s; other agents wait for it and are told so). A brand-new simulator would otherwise take about 65 s to boot every time.

## Project map: write it down once

Which scheme runs what is project knowledge that every agent otherwise rediscovers (for example: tests may live in an aggregate scheme rather than per-package schemes, the app scheme may build but have no test action, app tests may run from a different project than package tests, and some code may have no CI). `xc` remembers the project and scheme per repo, but not that map. If the repo's `AGENTS.md`/`CLAUDE.md` has none, add a short one the first time you work it out: for each of "package tests", "app build", "app tests", the exact `xc` command, `--project` and `--scheme`, and which code has no CI. A scheme with no test action fails with a hint saying so.

`xc` remembers the project and scheme separately for `build` (used by `build`/`run`/`sim`/`env`) and `test`, so a package-centric repo's test scheme (e.g. a `*-Package` scheme in `Package.swift`) does not inherit the app's build default, or vice versa. If `xc test` says no test bundles ran, it names the project/scheme it used and lists schemes that look test-shaped; pick one with `--scheme` for that call, or lock it in for every worktree with `xc config set --target test --scheme <name>` (add `--project` too if it lives in a different project/package than the build default). `xc config show` prints what is currently remembered.

**Env vars for the test process:** `xc test`'s own environment reaches `xcodebuild`, but `xcodebuild` only forwards vars prefixed `TEST_RUNNER_` into the simulator test host's environment - anything else (e.g. `UPDATE_SCHEMA_SNAPSHOT=1`) is silently dropped before it reaches the test. Prefix it yourself: `TEST_RUNNER_UPDATE_SCHEMA_SNAPSHOT=1 xc test ...`.

## Before opening a PR

Prove the change compiles with everything else, not just its own scheme. Two PRs that each built alone have broken `main` together, because a package scheme does not build the app target. One call each, in order:

1. `xc test` for the package/library the change lives in.
2. Find the schemes that consume the changed code with `xcodebuild -list` (read-only, allowed) and build each in Debug: `xc build --scheme <app or feature scheme>`.
3. Run the test targets CI skips, for example tests that live in the app project rather than a package: `xc test --scheme <app scheme>` (or `--plan <name>`).

State in the PR which suites you could not run (previews, device-only tests) instead of leaving the reader to assume everything ran.

## Stopping a bad run

Use `xc stop` from the worktree: it stops that worktree's running `xc` command and its `xcodebuild` (SIGTERM, then SIGKILL after 20 s if a hung test ignores it). Do not use `pkill`, which is denied and could hit other agents' builds. If you started the run as a background task, `TaskStop` also works. A crash-looping or hung test is a reason to stop, read the log, and fix, not to re-run.

## Using the private simulator for debugging

Get the UDID with `xc sim`, then pass it explicitly everywhere:

```bash
UDID=$(xc sim)
xcrun simctl io "$UDID" screenshot /tmp/shot-$UDID.png
xcrun simctl spawn "$UDID" log stream --predicate 'process == "MyApp"'
xcrun simctl openurl "$UDID" myapp://deeplink
```

Other simulator tooling (including any simulator MCP or app-integrated simulator tool) usually defaults to "the booted device" and will grab someone else's. Always give it your UDID. Never `simctl shutdown all`, `erase all` or `delete unavailable`.

Use `xc reset-sim` to erase only your own simulator.

## What is isolated, what is coordinated

| Resource | Treatment | Why |
|---|---|---|
| DerivedData, result bundles, logs | per worktree (`~/Library/Caches/xc-parallel/<name>-<hash>/`) | a shared build database errors with "database is locked"; separate dirs make builds truly parallel |
| Simulator | per worktree (clone of a warmed template) | app containers, UserDefaults, keychain and the test runner are per device, so sharing means clobbering |
| Two `xc` commands in the *same* worktree | queued (flock) | same DerivedData and same simulator |
| Compile phase across worktrees | at most `max(2, ncpu/3)` at once (`XC_BUILD_SLOTS`) | N builds each spawning ncpu jobs starve running tests into timeouts; test execution itself is not throttled |
| SwiftPM package cache, module cache | shared, untouched | SwiftPM and clang lock these themselves |
| Xcode parallel testing | off unless `--parallel` | it clones extra simulators per run; leaks them if killed |

Locks are `flock`s, so a crashed or killed agent releases them automatically. SIGTERM/SIGINT are forwarded to xcodebuild, so a cancelled run does not leave an orphan build holding a slot.

## The Xcode MCP server: use sparingly

Findings from investigating `xcrun mcpbridge`:

- It drives the one running Xcode GUI. Builds go through that app's own build queue, DerivedData and run destination, so concurrent agents are not isolated from each other.
- Every agent must be approved per project folder through a dialog in Xcode before any tool works (`XcodeListWorkspaces` fails until `XcodeOpenWorkspace` is approved). Unattended parallel sessions stall on this.
- Active scheme, test plan and run destination (`XcodeSwitchScheme`, `XcodeSwitchRunDestination`) are per workspace in the GUI, not per agent. Two agents on one workspace overwrite each other's choice.
- Opening many worktrees in one Xcode costs memory and indexing time.

So build, test and run with `xc`. Unattended agents cannot use `RenderPreview` (it needs GUI approval in Xcode) and stall on it. For UI changes compile the target that contains the `#Preview` with `xc build`, and report previews as "compiled, not rendered"; a snapshot test is the way to get pixels. Reach for the MCP only for things the CLI cannot do: `RenderPreview` when a human is watching, `DocumentationSearch`, `XcodeRefreshCodeIssuesInFile`, `GetBuildLog` diagnostics. Pass an explicit `workspaceIdentifier` and never rely on the active scheme or destination. If the user insists on MCP builds, one agent per workspace is the safe limit.

## Maintenance and failure modes

- `xc status`: identity, simulator state, compile-slot usage, disk use, and a count of other state dirs that look stale (worktree gone, or idle 45+ min) with a pointer to `xc gc`. `xc status --all` lists every known worktree the same way, each marked `STALE` when applicable.
- `xc gc`: dry-run by default - it only logs what it would reclaim or shut down. Add `--yes` to actually act. It also runs automatically (acting for real, not dry-run) at most every 6 h as part of any `xc` command. Reclaims simulators and state of removed worktrees, shuts down simulators idle 45+ min (a booted simulator costs about 1 GB RAM), drops DerivedData unused for 14 days. It never touches a state dir whose worktree lock is held (an active `xcodebuild` or a held compile slot) and never touches the `xcp-template-*` warm simulator. `xc` only ever creates and deletes simulators named `xcp-*`; the user's own are untouched. After removing a worktree with `git worktree remove`, run `xc gc --yes` (or just wait for the automatic sweep) to reclaim its simulator and DerivedData immediately rather than leaving it for another agent's `xc` call to trigger.
- Disk, if `xc` refuses to start (under 3 GiB free): run `xc gc --yes` first, it is safe and usually frees enough (removed worktrees' state, stale DerivedData, idle simulators); then retry. The only directory safe to delete by hand is `~/Library/Caches/xc-parallel`, and that is the user's call. Background: each worktree holds a DerivedData (2-3 GB) plus a simulator. `xc` caps its own DerivedData at 30 GiB (`XC_CACHE_BUDGET_GB`): when a worktree starts its first build it drops the least recently used DerivedData of idle worktrees until under the cap, and `xc gc --yes` enforces it too. Size the cap at about 3 GB per concurrent worktree. Free space is only a hard stop (refuse below 3 GiB, warn below 10 GiB); if `xc gc` does not help, something else is using the disk or other agents hold it: wait or tell the user.
- Cold builds: the first `xc` build in a new worktree takes minutes (4-5 on a large project), later ones about a minute. That is expected: start the worktree's first build early and in the background rather than waiting on it. Coordinators: keep to about 4-6 concurrent agents; compile slots queue the rest, but with 5-6 agents runs and CI waits stretched to 20-40 minutes. Reusing a worktree for the next task keeps its warm DerivedData; a fresh worktree always pays the cold build.
- Ambiguity: several projects or schemes make `xc` stop and list them. Pick with `--project` / `--scheme` for that call. If the same ambiguity will come up on every worktree of this repo (the normal case), make it permanent once with `xc config set --target build --project P --scheme S` (and `--target test` separately if the test scheme differs - see "Project map" above); otherwise you will need to pass the flag again on your next call. `--device "iPhone 17"`, `--runtime 18.5`, `--platform tvos|watchos|visionos|macos` work the same way and are remembered automatically (env: `XC_DEVICE`, `XC_RUNTIME`).
- `waiting for ...` lines mean another agent holds a lock or all compile slots. Wait; it is cheaper than a conflict. Do not kill other agents' processes.
- A hung or crashed test host (no output for 10 min by default) aborts the run instead of hanging forever, with a hint to narrow with `xc test --only <one target>` and the log path. Tune the limit with `XC_HANG_TIMEOUT` (seconds). A simulator that fails to boot under load is retried once after a reset before `xc` gives up.
- Not isolatable by `xc`: fixed TCP ports used by tests or local servers, shared on-disk fixture paths outside the repo, shared remote test accounts. Make those per-worktree, for example by deriving them from the simulator UDID (`xc env` prints `XC_SIM_UDID`).
- For Swift packages that do not need a simulator, plain `swift test` in the worktree is already isolated by its own `.build`; no wrapper needed.

If a hook denies a raw `xcodebuild`/`simctl` command, that is this skill's guard (`scripts/xc-guard`): rerun it through `xc` as the message says rather than looking for a way around it.

Design notes, all flags, the guard hook setup and the concurrency self-test (`tests/selftest.sh`) are in [REFERENCE.md](REFERENCE.md).
