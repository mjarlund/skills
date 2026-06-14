---
name: 3d-diagnose
description: Diagnose FDM 3D print failures from text description or photo. Identifies root causes, prescribes slicer and hardware fixes, and iterates until resolved. Use when user describes a failed print, shares a photo of a print failure, asks why their print looks wrong, or mentions stringing, warping, layer issues, under-extrusion, shifting, or any other print defect.
references: [REFERENCE.md]
---

# 3D Diagnose Skill

<what-to-do>

Diagnose FDM print failures and prescribe actionable fixes. Do not run an intake form — diagnose immediately from the first description. Ask follow-up questions only when confidence on a specific finding is low.

## Diagnosis flow

1. User describes failure (text) or shares photo.
2. Diagnose immediately. Produce ranked findings table + fix steps.
3. Ask targeted follow-ups only when a finding is uncertain (flag confidence as "Low" in table).
4. Ask hardware questions (bed surface, extruder type, hotend) lazily — only when diagnosis requires it.
5. If root cause is geometry or design: cross-link to `3d-print` skill. Do not attempt CAD fixes here.
6. After delivering fixes: ask user to reprint and report result.
   - Same failure persists → escalate to hardware/calibration checks.
   - New failure appears → treat as fresh diagnosis.
   - Resolved → close loop.

## Multi-failure handling

- Triage by severity (print-stopping > quality > cosmetic).
- Flag fix conflicts explicitly: e.g. "Fix 1 raises temp — this may worsen stringing from Fix 2. Apply Fix 2 first."

## Output format

Always structure output as:

```
| # | Failure | Confidence | Priority |
|---|---------|------------|----------|
| 1 | <name>  | High/Med/Low | Fix first/after/last |

## Fix 1: <Failure name>
- <Setting>: <current→target> (Cura: <name>, PrusaSlicer: <name>, OrcaSlicer/Bambu: <name>)
- <Hardware action if needed>

**Conflict note:** <if this fix conflicts with another>
**If fix does not resolve:** <escalation step>
```

Use generic setting names. Always include slicer aliases for Cura, PrusaSlicer, and OrcaSlicer/Bambu in parentheses.

## Failure taxonomy

Cover all 13 failure modes. See REFERENCE.md for symptom signatures, fix ranges, and material notes.

1. Stringing / oozing
2. Under-extrusion / weak layers
3. Over-extrusion / blobbing
4. Warping / bed adhesion failure
5. Layer separation / delamination
6. Layer shifting / ghosting
7. First layer issues
8. Clogged nozzle / grinding filament
9. Elephant's foot
10. Bridging failure
11. Support issues
12. Dimensional inaccuracy
13. Heat creep / thermal runaway

</what-to-do>

<supporting-info>

## When to cross-link to 3d-print skill

Cross-link when:
- Overhangs too steep for bridging failure → redesign geometry
- Wall thickness too thin for under-extrusion → increase wall count in model
- No flat bottom face → reorient or add brim in model

Say: "Root cause is geometry. Use the `3d-print` skill to fix: [specific parameter]."

## Verification loop

After fixes delivered:

> "Apply these changes and run another print. Report back with what changed — same issue, resolved, or new problem."

- Same issue → ask for hardware details, check calibration (e-steps, PID, belt tension).
- New issue → fresh diagnosis pass on new failure.
- Resolved → confirm and close.

## Escalation triggers

Escalate to hardware/calibration when:
- Fix applied correctly but failure persists across 2+ reprints
- Multiple conflicting symptoms with no clear slicer root cause
- Heat creep suspected → check PTFE tube, cooling fan, heat break

For detailed fix ranges and material-specific notes, see REFERENCE.md.

</supporting-info>
