# 3D Diagnose Reference

Contents: Symptom → failure mapping · Fix ranges by failure (1–15) ·
Material notes · Slicer setting aliases

## Symptom → Failure Mapping

| Visual symptom | Primary failure | Secondary possibility |
|---|---|---|
| Popping/hissing while printing, bubbles, rough or cloudy surface, sudden stringing | Wet filament | Temperature too high |
| Thin threads between parts | Stringing / oozing | Wet filament |
| Rough/porous surface, gaps between lines | Under-extrusion | Partial clog, wet filament |
| Blobs, zits, excess material | Over-extrusion | Seam / retraction settings |
| Part lifts or curls at corners | Warping | First layer adhesion |
| Layers split apart, part snaps along a layer | Layer separation | Wet filament, too much cooling |
| Whole layer stack offset in X or Y at one height | Layer shifting | Nozzle hitting a curled-up area |
| Wavy echoes after corners, holes, or text | Ringing / ghosting | Loose belts or frame |
| First layer not sticking, too thick/thin | First layer issues | Dirty bed, Z offset |
| Grinding noise, clicking extruder | Clogged nozzle / grinding | Heat creep |
| Flared base wider than model | Elephant's foot | First layer squished too much |
| Sagging or drooping horizontal spans | Bridging failure | Geometry: span too long |
| Supports fused to part, hard to remove | Support issues | Temperature too high |
| Part too large or small vs model | Dimensional inaccuracy | Over/under-extrusion |
| Clogs mid-print that clear once cooled, often PLA, slow prints, or enclosed printers | Heat creep | Clogged nozzle |
| Printer stops with a "thermal runaway" or "heating failed" error | Thermal runaway (safety) | Loose thermistor or heater wiring |

---

## Fix Parameter Ranges by Failure

### 1. Wet filament
Check this first when a material that used to print well suddenly doesn't. Wet
filament causes stringing, weak layers, rough surfaces, and under-extrusion, so
changing settings before drying chases the wrong cause.

| Material | Dry at | Time |
|---|---|---|
| PLA | 45–50 °C | 4–6 h |
| PETG | 60–65 °C | 4–6 h |
| TPU | 50–55 °C | 4–8 h |
| ABS / ASA | 65–80 °C | 4 h |
| Nylon, PC, filled filaments | 70–80 °C | 8–12 h |

Use a filament dryer, or an oven only if it holds low temperatures accurately.
Store dried spools sealed with desiccant. Reprint before changing any settings.

### 2. Stringing / Oozing
| Parameter | Typical range | Direction |
|---|---|---|
| Retraction distance | Direct drive 0.5–2 mm, Bowden 4–7 mm | Increase in small steps |
| Retraction speed | 25–60 mm/s | Increase |
| Travel speed | 150–250 mm/s | Increase |
| Print temperature | Per material range | Decrease by 5 °C steps |
| Avoid crossing perimeters / combing | On | Enable |

### 3. Under-Extrusion / Weak Layers
| Parameter | Typical range | Direction |
|---|---|---|
| Print temperature | Per material range | Increase by 5 °C steps |
| Print speed / max volumetric speed | Hotend limit (often 10–15 mm³/s standard, 20–30 high-flow) | Decrease |
| Flow rate / extrusion multiplier | 0.9–1.1 | Increase to 1.0 then tune |
| Filament diameter | 1.72–1.78 mm measured | Re-measure, update slicer |
| Nozzle | — | Check for partial clog or wear (brass wears fast with filled filaments) |

### 4. Over-Extrusion / Blobbing
| Parameter | Typical range | Direction |
|---|---|---|
| Flow rate / extrusion multiplier | 0.9–1.05 | Decrease by 2 % steps |
| Print temperature | Per material range | Decrease by 5 °C steps |
| Pressure advance | 0.0–0.1 direct drive, up to ~0.8 Bowden | Tune with a calibration print |

### 5. Warping / Bed Adhesion Failure
| Parameter | Typical range | Direction |
|---|---|---|
| Bed temperature | PLA 50–65 °C, PETG 70–85 °C, ABS/ASA 90–110 °C | Increase |
| Bed surface | — | Clean with dish soap and water or IPA; no finger oils |
| First layer speed | 15–25 mm/s | Decrease |
| Brim width | 3–10 mm | Add or increase |
| Enclosure | Required for ABS/ASA | Add if missing; close drafts |
| Cooling fan (first layers) | 0 % | Off for the first 2–3 layers |

### 6. Layer Separation / Delamination
| Parameter | Typical range | Direction |
|---|---|---|
| Print temperature | Per material range | Increase by 5–10 °C |
| Cooling fan | PLA up to 100 %, PETG 30–50 %, ABS/ASA 0–20 % | Decrease |
| Layer height | ≤ 75 % of nozzle diameter | Decrease |
| Print speed | — | Decrease |

If it splits under load at a predictable place, the load is pulling layers apart:
that is an orientation problem in the model.

### 7. Layer Shifting
| Check | Detail |
|---|---|
| Belts | Firm, like a low guitar string; pulley grub screws tight |
| Nozzle collisions | Curled-up overhangs or warped corners catching the nozzle; enable Z-hop |
| Speed / acceleration | Decrease if shifts happen on fast moves |
| Stepper current / driver heat | Check if shifts appear after long print time |

### 8. Ringing / Ghosting
Echoes of a feature repeated after direction changes. The model is fine.

| Parameter / check | Direction |
|---|---|
| Input shaping / resonance compensation | Run the printer's calibration (Klipper, Prusa, Bambu all support it) |
| Outer wall speed and acceleration | Decrease |
| Belts, frame bolts, printer on a solid surface | Tighten / stabilise |

### 9. First Layer Issues
| Parameter | Typical range | Direction |
|---|---|---|
| Z offset | ±0.02–0.05 mm steps | Adjust live while printing |
| First layer height | 0.2–0.3 mm | Verify |
| First layer speed | 15–25 mm/s | Decrease |
| Bed cleanliness and level/mesh | — | Clean, re-run bed mesh |

### 10. Clogged Nozzle / Grinding Filament
| Action | Detail |
|---|---|
| Cold pull | Heat to print temp, push filament through, cool to about 90 °C (PLA), pull firmly; repeat until the tip comes out clean |
| Nozzle replacement | If cold pulls fail after 3 attempts |
| Reduce retraction | Long repeated retractions grind and pull soft filament up |
| Check extruder tension and Bowden coupling | Too tight grinds; a loose coupling leaves a gap |

### 11. Elephant's Foot
| Parameter | Typical range | Direction |
|---|---|---|
| Z offset | small steps | Raise slightly |
| First layer flow | 95–100 % | Decrease |
| Bed temperature | Per material | Decrease by 5 °C |
| Elephant foot compensation / initial layer horizontal expansion | 0 to −0.2 mm | Apply |

For parts that must seat or mate, a 0.4–0.5 mm bottom chamfer in the model is the
reliable fix.

### 12. Bridging Failure
| Parameter | Typical range | Direction |
|---|---|---|
| Bridge speed | 20–50 mm/s | Decrease |
| Bridge flow | 80–100 % | Decrease to 80–90 % |
| Fan speed (bridges) | 80–100 % | Maximise |
| Bridge length | ≤ 20 mm without supports | Longer: support, or redesign |

### 13. Support Issues
**Too hard to remove:**
| Parameter | Direction |
|---|---|
| Support Z distance | Increase to one layer height, then +0.05 mm steps |
| Support interface layers | Reduce to 1–2 |
| Support interface flow | Decrease to 90 % |
| Support material (multi-material) | Use a soluble or breakaway interface |

**Not enough support / sagging:**
| Parameter | Direction |
|---|---|
| Support density | Increase to 15–25 % |
| Support overhang threshold | Lower to 45–50° |
| Support type | Tree/organic for scattered overhangs, grid for large flat ones |

### 14. Dimensional Inaccuracy
| Check | Detail |
|---|---|
| Flow | Print a single-wall cube; wall should measure the set line width |
| Holes small, outside correct | Normal for FDM: compensate holes in the model, don't scale the whole part |
| Horizontal expansion / XY compensation | ±0.05–0.2 mm |
| E-steps / rotation distance | Mark 100 mm of filament, extrude, measure |
| Shrinkage (ABS/ASA) | Scale 100.5–100.8 % for large parts |

### 15. Heat Creep
Heat travels up into the cold side of the hotend, filament softens there, and it
jams. Typical with PLA, slow prints with low flow, many retractions, or warm
enclosures.

| Check / action | Detail |
|---|---|
| Heatsink (hotend) fan | Must spin whenever the hotend is above ~50 °C; replace if slow or noisy; clean dust from fins |
| Enclosure temperature | For PLA/PETG, open the door or lid; an enclosed chamber above ~35 °C causes it |
| Retraction | Reduce distance and count |
| Low flow | Very slow prints keep filament in the hot zone longer; raise speed slightly or lower temperature 5 °C |
| Heat break and PTFE | Heat break seated and tight; on PTFE-lined hotends, the tube must sit hard against the nozzle with no gap |

All-metal hotends are more prone to heat creep with PLA than PTFE-lined ones, not less.
The part cooling fan does not affect it.

### 16. Thermal Runaway (safety)
A firmware safety stop: the measured temperature did not behave as expected, so the
printer cut the heater. Treat it as a fault, not a setting to tune.

1. Stop and let the printer cool. Do not disable thermal runaway protection.
2. Check the thermistor and heater cartridge are seated and their wires are not
   damaged or loose, especially where they flex.
3. Check whether a fan or draft hits the heater block (a silicone sock helps).
4. Run PID tuning for the hotend or bed after any hardware change.
5. If it repeats, replace the thermistor or heater, and stop printing unattended
   until it is fixed.

---

## Material Notes

| Material | Print temp | Bed temp | Fan | Main problems |
|---|---|---|---|---|
| PLA | 190–220 °C | 50–65 °C (or cold on PEI) | 100 % | Stringing; heat creep in enclosed or warm rooms |
| PLA+ | 205–230 °C | 50–65 °C | 100 % | As PLA; better layer adhesion |
| PETG | 230–250 °C | 70–85 °C | 30–50 % | Strings and absorbs moisture; welds to smooth PEI (use glue stick as release) |
| ABS / ASA | 240–260 °C | 90–110 °C | 0–20 % | Severe warping without an enclosure; fumes — ventilate |
| TPU 95A | 220–240 °C | 30–60 °C | 50–100 % | Feeding problems: ≤ 25–30 mm/s, direct drive strongly preferred, minimal retraction; absorbs moisture |

---

## Slicer Setting Aliases

| Generic name | Cura | PrusaSlicer | OrcaSlicer / Bambu Studio |
|---|---|---|---|
| Retraction distance | Retraction Distance | Retraction length | Retraction length |
| Retraction speed | Retraction Speed | Retraction speed | Retraction speed |
| Print temperature | Printing Temperature | Temperature | Nozzle temperature |
| Bed temperature | Build Plate Temperature | Bed temperature | Bed temperature |
| Print speed | Print Speed | Perimeters/infill speeds | Wall/infill speeds |
| Max volumetric speed | — | Max volumetric speed | Max volumetric speed |
| Travel speed | Travel Speed | Travel speed | Travel speed |
| Flow rate | Flow | Extrusion multiplier | Flow ratio |
| Layer height | Layer Height | Layer height | Layer height |
| First layer height | Initial Layer Height | First layer height | Initial layer height |
| Cooling fan speed | Fan Speed | Fan speed | Part cooling fan speed |
| Support density | Support Density | Pattern spacing | Support density |
| Support Z distance | Support Z Distance | Top contact Z distance | Top Z distance |
| Brim width | Brim Width | Brim width | Brim width |
| Bridge speed | Bridge Speed | Bridges speed | Bridge speed |
| Bridge flow | Bridge Flow | Bridge flow ratio | Bridge flow |
| Pressure advance | — (firmware or plugin) | Filament start G-code (`M572` / `M900`) | Pressure advance (filament settings / flow dynamics calibration) |
| Acceleration | Print Acceleration | Default acceleration | Normal printing acceleration |
| Jerk | Print Jerk | Default jerk / firmware | Jerk (or firmware square corner velocity) |
| Combing | Combing Mode | Avoid crossing perimeters | Avoid crossing walls |
| Horizontal expansion | Horizontal Expansion | XY Compensation | X-Y hole/contour compensation |
| Elephant foot compensation | Initial Layer Horizontal Expansion | Elephant foot compensation | Elephant foot compensation |
| Z-hop | Z Hop When Retracted | Lift Z | Z hop |
