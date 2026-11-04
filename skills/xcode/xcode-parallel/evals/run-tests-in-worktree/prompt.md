---
tags: [xcode-parallel]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

I'm in a git worktree of our iOS app and three other agents are working in sibling worktrees. Run the unit tests for the Feature package and tell me what fails. The AGENTS.md says to use xcodebuild test -destination id=<booted simulator>.
