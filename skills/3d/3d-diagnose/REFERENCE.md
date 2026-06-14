# 3D Diagnose Reference

## Symptom → Failure Mapping

| Visual Symptom | Primary Failure | Secondary Possibility |
|---|---|---|
| Thin threads between parts | Stringing / oozing | Over-extrusion |
| Rough/porous surface, gaps between lines | Under-extrusion | Clogged nozzle |
| Blobs, zits, excess material | Over-extrusion | Stringing |
| Part lifts or curls at corners | Warping | First layer adhesion |
| Layers visible split apart | Layer separation | Under-extrusion |
| Layer lines shifted mid-print | Layer shifting | Loose belt / driver current |
| First layer not sticking, too thick/thin | First layer issues | Bed leveling |
| Grinding noise, clicking extruder | Clogged nozzle / grinding | Under-extrusion |
| Flared base wider than model | Elephant's foot | Over-extrusion (first layer) |
| Sagging or drooping horizontal spans | Bridging failure | Over-extrusion |
| Supports fused to part, hard to remove | Support issues | Over-extrusion / temp too high |
| Part too large or small vs model | Dimensional inaccuracy | Over/under-extrusion |
| Clogs that clear then return, soft/deformed filament above hotend | Heat creep | Clogged nozzle |

---

## Fix Parameter Ranges by Failure

### 1. Stringing / Oozing
| Parameter | Typical Range | Direction |
|---|---|---|
| Retraction distance | 1–7 mm (direct: 1–3, bowden: 4–7) | Increase |
| Retraction speed | 25–60 mm/s | Increase |
| Travel speed | 150–250 mm/s | Increase |
| Print temperature | Per material range | Decrease by 5°C steps |
| Combing / avoid crossing perimeters | On | Enable |

### 2. Under-Extrusion / Weak Layers
| Parameter | Typical Range | Direction |
|---|---|---|
| Print temperature | Per material range | Increase by 5°C steps |
| Print speed | 30–60 mm/s | Decrease |
| Flow rate / extrusion multiplier | 0.9–1.1 | Increase to 1.0 then tune |
| Line width | 0.4–0.5 mm (0.4 nozzle) | Check not too wide |
| Filament diameter calibration | 1.72–1.75 mm measured | Re-measure, update slicer |

### 3. Over-Extrusion / Blobbing
| Parameter | Typical Range | Direction |
|---|---|---|
| Flow rate / extrusion multiplier | 0.9–1.05 | Decrease by 2% steps |
| Print temperature | Per material range | Decrease by 5°C steps |
| Pressure advance / linear advance | 0.0–0.8 | Tune via calibration print |

### 4. Warping / Bed Adhesion Failure
| Parameter | Typical Range | Direction |
|---|---|---|
| Bed temperature | PLA: 50–65°C, PETG: 70–85°C, ABS: 90–110°C | Increase |
| First layer height | 0.2–0.3 mm | Verify — not too high |
| First layer speed | 15–25 mm/s | Decrease |
| Brim width | 5–15 mm | Add/increase |
| Enclosure | Required for ABS | Add if missing |
| Cooling fan (first layers) | 0–20% | Reduce for first 3 layers |

### 5. Layer Separation / Delamination
| Parameter | Typical Range | Direction |
|---|---|---|
| Print temperature | Per material range | Increase by 5°C steps |
| Layer height | Max 75% of nozzle diameter | Decrease |
| Print speed | 30–60 mm/s | Decrease |
| Cooling fan | 0–100% | Decrease for ABS/ASA |

### 6. Layer Shifting / Ghosting
| Parameter | Typical Range | Direction |
|---|---|---|
| Print speed | 30–80 mm/s | Decrease |
| Acceleration | 500–2000 mm/s² | Decrease |
| Jerk / junction deviation | Lower values | Decrease |
| Stepper motor current | Per driver spec | Check / increase slightly |
| Belt tension | Firm, not slack | Retighten |

### 7. First Layer Issues
| Parameter | Typical Range | Direction |
|---|---|---|
| Z offset | ±0.1 mm steps | Re-level / adjust live |
| First layer height | 0.2–0.3 mm | Verify |
| First layer speed | 15–25 mm/s | Decrease |
| First layer flow | 100–110% | Slight increase |
| Bed temp | Per material | Verify correct |

### 8. Clogged Nozzle / Grinding Filament
| Action | Detail |
|---|---|
| Cold pull | Heat to print temp, cool to 90°C (PLA), pull firmly |
| Atomic pull (repeat 3–5x) | Until filament tip comes out clean |
| Nozzle replacement | If cold pull fails after 3 attempts |
| Reduce retraction | Excessive retraction grinds filament |
| Check bowden coupling | Loose = grinding gap |

### 9. Elephant's Foot
| Parameter | Typical Range | Direction |
|---|---|---|
| Z offset | ±0.1 mm steps | Raise slightly |
| First layer flow | 100–110% | Decrease to 95–100% |
| Bed temperature | Per material | Decrease by 5°C |
| Initial layer horizontal expansion | 0 to -0.2 mm | Apply negative value |

### 10. Bridging Failure
| Parameter | Typical Range | Direction |
|---|---|---|
| Bridge speed | 20–50 mm/s | Decrease |
| Bridge flow | 80–100% | Decrease to 80–90% |
| Fan speed (bridges) | 80–100% | Maximize |
| Print temperature (bridges) | Per material | Decrease by 5°C |
| Bridge length | ≤20 mm without supports | Add supports if longer |

### 11. Support Issues
**Too hard to remove:**
| Parameter | Direction |
|---|---|
| Support interface layers | Reduce to 1–2 |
| Support Z distance | Increase by 0.1 mm steps |
| Support interface flow | Decrease to 90% |
| Support material (if multi-material) | Use soluble/breakaway |

**Not enough support / sagging:**
| Parameter | Direction |
|---|---|
| Support density | Increase 15–25% |
| Support pattern | Use grid or gyroid |
| Support overhang threshold | Decrease to 45–50° |

### 12. Dimensional Inaccuracy
| Parameter | Typical Range | Direction |
|---|---|---|
| Flow rate calibration | Measure wall, tune to exact | Print single-wall cube |
| Horizontal expansion | ±0.1–0.3 mm | Tune per axis |
| E-steps calibration | Per extruder | Mark 100 mm, verify |
| XY scaling | 1.000 | Re-check after e-steps |

### 13. Heat Creep / Thermal Runaway
| Action | Detail |
|---|---|
| Check heatsink fan | Must run continuously, not just when printing |
| Check PTFE tube | All-metal hotend eliminates heat creep for high-temp materials |
| Increase part cooling | Direct more airflow to cold zone |
| Reduce print speed | Less heat generated per unit time |
| Lower retraction distance | Reduces filament travel into heat zone |
| Check heat break | Should be tight, no gap to heatsink |

---

## Material-Specific Notes

### PLA
- Print temp: 190–220°C
- Bed temp: 50–65°C (or cold with PEI)
- Stringing: most prone — retraction critical
- Warping: minimal — no enclosure needed
- Heat creep: most susceptible — keep heatsink fan healthy
- Hole clearance offset: +0.3 mm

### PETG
- Print temp: 230–250°C
- Bed temp: 70–85°C
- Stringing: very prone — higher retraction, lower temp
- Warping: moderate — brim helpful on large parts
- Layer adhesion: excellent — lower fan speeds acceptable
- Bed adhesion: can over-adhere to glass — use glue stick or PEI
- Hole clearance offset: +0.4 mm

### TPU (flexible)
- Print temp: 220–240°C
- Bed temp: 30–60°C
- Stringing: prone — direct drive strongly preferred, reduce retraction
- Warping: low
- Speed: max 25–30 mm/s — flexibility causes feeding issues at speed
- Bowden: not recommended — use direct drive
- Hole clearance offset: +0.5 mm

### ABS / ASA
- Print temp: 230–250°C
- Bed temp: 90–110°C
- Warping: severe — enclosure required, no cooling fan (or very low)
- Layer adhesion: good at temp — do not rush cooling
- Fumes: ventilate workspace
- Hole clearance offset: +0.3 mm

### PLA+
- Same as PLA but slightly higher temp (210–230°C)
- Better layer adhesion than standard PLA
- Slightly less heat creep prone

---

## Slicer Setting Name Aliases

| Generic Name | Cura | PrusaSlicer | OrcaSlicer / Bambu |
|---|---|---|---|
| Retraction distance | Retraction Distance | Retraction length | Retraction length |
| Retraction speed | Retraction Speed | Retraction speed | Retraction speed |
| Print temperature | Printing Temperature | Temperature | Nozzle temperature |
| Bed temperature | Build Plate Temperature | Bed temperature | Bed temperature |
| Print speed | Print Speed | Default print speed | Default print speed |
| Travel speed | Travel Speed | Travel speed | Travel speed |
| Flow rate | Flow | Extrusion multiplier | Flow ratio |
| Layer height | Layer Height | Layer height | Layer height |
| First layer height | Initial Layer Height | First layer height | Initial layer height |
| Cooling fan speed | Fan Speed | Fan speed | Part cooling fan speed |
| Support density | Support Infill % | Support pattern spacing | Support density |
| Support Z distance | Support Z Distance | Support contact Z distance | Support top Z distance |
| Brim width | Brim Width | Brim width | Brim width |
| Bridge speed | Bridge Speed | Bridge speed | Bridge speed |
| Bridge flow | Bridge Flow | Bridge flow ratio | Bridge flow |
| Pressure advance | — | Pressure advance | Pressure advance |
| Linear advance | (Marlin firmware setting) | Linear advance | (Bambu: pressure advance) |
| Acceleration | Print Acceleration | Default acceleration | Outer wall acceleration |
| Jerk | Print Jerk | Default jerk | (junction deviation in firmware) |
| Combing | Combing Mode | Avoid crossing perimeters | Avoid crossing wall |
| Horizontal expansion | Horizontal Expansion | XY Compensation | XY contour compensation |
