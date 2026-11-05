---
tags: [xcode-parallel]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Another agent already ran `xc build` in this repo, so `app/MyApp.xcodeproj` with scheme "MyApp Debug" is the remembered build default. The actual unit tests for the code I changed live in `packages/Package.swift` under scheme "MyApp-Package" - a completely different project from the app. Run the tests for my change and tell me if they pass.
