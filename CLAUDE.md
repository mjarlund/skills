# Repository Rules

This repository contains installable skills.

## Scope

- Production skills live under `skills/`.
- Every production skill must include a `SKILL.md` file with frontmatter.

## Root Docs Consistency

- Every production skill must have a reference entry in the top-level `README.md`.
- Each README entry should link directly to that skill's `SKILL.md`.
- If examples exist for a skill, include at least one example link in `README.md`.

## Style

- Prefer tool-agnostic guidance unless a tool is explicitly required.
- Keep workflows checkpointed and testable.
- Keep language concise, imperative, and outcome-focused.

## Agent skills

### Issue tracker

Issues live in GitHub Issues (`gh` CLI). See `docs/agents/issue-tracker.md`.

### Triage labels

Default label vocabulary — no overrides. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context — `CONTEXT.md` + `docs/adr/` at repo root. See `docs/agents/domain.md`.
