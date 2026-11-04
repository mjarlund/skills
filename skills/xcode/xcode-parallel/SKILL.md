---
name: xcode-parallel
description: Build, test, run and debug Xcode / Swift / iOS projects safely when several coding agents or git worktrees work on the same project at once. Use this skill whenever you are about to run xcodebuild, run tests that need an iOS simulator, use xcrun simctl, boot or pick a simulator, or call the Xcode MCP tools (BuildProject, RunAllTests, RunSomeTests, RunProject, XcodeSwitchRunDestination) - especially in a git worktree session or when other agents may be running. Prevents simulator clobbering, "database is locked" build errors, flaky tests from CPU starvation, and leaked simulators. Use it even if the user does not mention parallel work; a plain "run the tests" or "build the app" in an Xcode project qualifies.
compatibility: macOS with Xcode 16+ and python3 (stdlib only). Not for Linux or CI runners without Xcode.
---

# Parallel-safe Xcode work

Several agents share one Mac, one CoreSimulator service and (if the MCP is used) one Xcode GUI. Measured on 4 concurrent worktrees running the same simulator test against one shared simulator: 3 of 4 failed (state clobbered, "test runner exited before establishing connection"). Through `xc` all passed.

`scripts/xc` (in this skill's directory) gives each git worktree its own DerivedData, its own simulator and its own result bundles, and queues only what truly cannot overlap. It needs no project configuration: it finds the workspace/project/scheme itself and remembers it.

## Default workflow

Invoke the script by its path inside this skill's directory (the base directory shown when the skill loaded) with `python3`, from anywhere inside the worktree. Below, `xc` stands for `python3 <skill-dir>/scripts/xc`. Set it once per shell command, for example `XC="python3 /path/to/xcode-parallel/scripts/xc"`.

```bash
xc test                                  # build-for-testing + test, failures summarised
xc test --only MyTests/FooTests/testBar  # narrow runs; repeatable
xc build                                 # compile check
xc run                                   # build, install and launch on the private simulator
xc sim                                   # prints this worktree's simulator UDID (booted)
```

Do not call `xcodebuild ... -destination` or `simctl boot booted` yourself, and do not pick a simulator from `simctl list`. Those are the shared resources other agents are using; `xc` hands you a private one. For raw xcodebuild flags, pass them after `--`: `xc build -- -configuration Release`.

Builds take minutes and many agent shells time out around 10 minutes, so run `xc test` in the background when the project is large and read the log path it prints instead of re-running. Output is already reduced to errors, test failures and a result summary; the full log path is printed at the end.

First use in a worktree creates its simulator by cloning a warmed template (about 5 s). The first use on the whole machine warms that template once (about 65 s; other agents wait for it and are told so). A brand-new simulator would otherwise take about 65 s to boot every time.

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

So build, test and run with `xc`. Reach for the MCP only for things the CLI cannot do: `RenderPreview`, `DocumentationSearch`, `XcodeRefreshCodeIssuesInFile`, `GetBuildLog` diagnostics. Pass an explicit `workspaceIdentifier` and never rely on the active scheme or destination. If the user insists on MCP builds, one agent per workspace is the safe limit.

## Maintenance and failure modes

- `xc status`: identity, simulator state, compile-slot usage, disk use.
- `xc gc`: also runs automatically at most every 6 h. Reclaims simulators and state of removed worktrees, shuts down simulators idle 45+ min (a booted simulator costs about 1 GB RAM), drops DerivedData unused for 14 days. `xc` only ever creates and deletes simulators named `xcp-*`; the user's own are untouched.
- Disk: each worktree holds a DerivedData plus a simulator. `xc` refuses to start below 3 GiB free and warns below 10 GiB. If the disk fills, delete `~/Library/Caches/xc-parallel`; the next run rebuilds and `xc` recovers by itself.
- Ambiguity: several projects or schemes make `xc` stop and list them. Pick with `--project` / `--scheme`; the choice is remembered per worktree. `--device "iPhone 17"`, `--runtime 18.5`, `--platform tvos|watchos|visionos|macos` work the same way (env: `XC_DEVICE`, `XC_RUNTIME`).
- `waiting for ...` lines mean another agent holds a lock or all compile slots. Wait; it is cheaper than a conflict. Do not kill other agents' processes.
- Not isolatable by `xc`: fixed TCP ports used by tests or local servers, shared on-disk fixture paths outside the repo, shared remote test accounts. Make those per-worktree, for example by deriving them from the simulator UDID (`xc env` prints `XC_SIM_UDID`).
- For Swift packages that do not need a simulator, plain `swift test` in the worktree is already isolated by its own `.build`; no wrapper needed.

Design notes, all flags and the concurrency self-test (`tests/selftest.sh`) are in [REFERENCE.md](REFERENCE.md).
