---
tags: [xcode-parallel]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

We just finished a big batch of about 15 parallel agents, each in its own worktree. `xc status --all` shows a bunch of them as idle or gone. Clean up all the leftover simulators and caches from that batch so the machine isn't full of junk.
