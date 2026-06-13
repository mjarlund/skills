// ============================================================
// Greenhouse 90° Corner Rail Brace
// Snaps onto aluminium glazing bar junction from above.
// Material: PETG recommended (UV + weather resistant).
// Print orientation: base plate face-down, no supports needed.
// ============================================================

// ---- PARAMETERS (measure your bars and adjust) -------------
bar_width     = 22.15;  // mm — glazing bar width
bar_height    = 20.15;  // mm — glazing bar profile height (wall grip depth)
arm_length    = 75;     // mm — how far each arm extends along bar
base_thick    = 2;      // mm — base plate thickness
wall_thick    = 2.5;    // mm — wall thickness
clearance     = 0.2;    // mm — press fit tolerance (increase to 0.3 for looser)

// ---- DERIVED (do not edit) ---------------------------------
chan_w  = bar_width + clearance * 2;
outer_w = chan_w + wall_thick * 2;

// ============================================================
module l_brace() {
    // L-shaped base plate
    union() {
        cube([arm_length + outer_w, outer_w, base_thick]);
        cube([outer_w, arm_length + outer_w, base_thick]);
    }

    // Outer walls — full L perimeter
    translate([0, 0, base_thick]) {
        cube([arm_length + outer_w, wall_thick, bar_height]);  // arm 1 outer
        cube([wall_thick, arm_length + outer_w, bar_height]);  // arm 2 outer
    }

    // Inner walls — arms only, open junction
    translate([outer_w, outer_w - wall_thick, base_thick])
        cube([arm_length, wall_thick, bar_height]);  // arm 1 inner

    translate([outer_w - wall_thick, outer_w, base_thick])
        cube([wall_thick, arm_length, bar_height]);  // arm 2 inner

    // Corner pillar — bridges gap between inner walls
    translate([outer_w - wall_thick, outer_w - wall_thick, base_thick])
        cube([wall_thick, wall_thick, bar_height]);
}

l_brace();
