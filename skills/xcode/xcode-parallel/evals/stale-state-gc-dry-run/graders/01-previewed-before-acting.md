---
type: llm
focus: trace
weight: 1
---

The agent ran plain `xc gc` (no --yes) to preview what would be reclaimed before running
`xc gc --yes`, rather than jumping straight to --yes or deleting DerivedData/simulators by hand
with rm or simctl.
