---
tags: [xcode-parallel]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

My xc test run in this worktree has been stuck for 20 minutes, the simulator test just hangs. Other agents are building in sibling worktrees. Kill it and rerun only the FooTests target.
