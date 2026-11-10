// Fit test piece: measures clearances on ONE printer + material + nozzle combo.
// Print it once per combo with the same settings as real parts, then replace the
// default fit values in your models with what you measured.
//
// Export (two separate STLs):
//   openscad -D 'part="plate"' -o fit-coupon-plate.stl fit-coupon.scad
//   openscad -D 'part="pin"'   -o fit-coupon-pin.stl   fit-coupon.scad
// Print the plate flat and the pin standing up. No supports.
//
// How to read it, in this order:
//   Row B (middle) - hole compensation. All holes are 3.0 mm nominal plus the
//     labelled extra diameter. The first one a 3 mm drill bit shank (or M3 screw)
//     slides into by hand is your HOLE_COMP: add it to every vertical hole diameter.
//   Row A (back) - fit between two printed parts. Labels are clearance PER SIDE.
//     Push the printed pin in from the top face. Pick the label that gives the
//     fit you want: press (needs force), slip (slides, no wobble), loose (wobbles).
//   Row C (front) - heat-set insert bores (labelled diameter). Install an insert in
//     each. The smallest bore that takes it flush without cracking the boss or
//     letting it spin is your insert bore.

part = "plate"; // [plate, pin]

/* [Row A: printed pin fits] */
pin_d = 6.0;
pin_h = 12.0;
clearances = [0.10, 0.15, 0.20, 0.25, 0.30, 0.40]; // per side, mm

/* [Row B: hole compensation] */
ref_d = 3.0;
comp_trials = [0.0, 0.1, 0.2, 0.3, 0.4]; // added to diameter, mm

/* [Row C: heat-set inserts] */
insert_bores = [3.8, 3.9, 4.0, 4.1, 4.2]; // typical M3 x 5.7 range
insert_depth = 6.7; // insert length + 1 mm relief
boss_od = 9.0;
boss_floor = 2.0;

/* [Layout] */
plate_t = 4.0;
pitch = 13;
margin = 7;
row_a = 48;
row_b = 30;
row_c = 12;
plate_d = 58;
corner_r = 3;
bed_chamfer = 0.4; // counters elephant's foot so the bottom of each hole is not tight
label_depth = 0.6;
label_size = 3;
eps = 0.01;

$fa = 1;
$fs = 0.3;

boss_h = insert_depth + boss_floor;
cols = max(len(clearances), max(len(comp_trials), len(insert_bores)));
plate_w = 2 * margin + (cols - 1) * pitch;

function col_x(i) = margin + i * pitch;

module label(s, x, y) {
    translate([x, y, plate_t - label_depth])
        linear_extrude(height = label_depth + eps)
            text(s, size = label_size, halign = "center", valign = "top");
}

module through_hole(d, x, y) {
    translate([x, y, -eps]) {
        cylinder(d = d, h = plate_t + 2 * eps);
        cylinder(d1 = d + 2 * bed_chamfer, d2 = d, h = bed_chamfer + eps);
    }
}

module plate_body() {
    linear_extrude(height = plate_t)
        offset(r = corner_r) offset(delta = -corner_r)
            square([plate_w, plate_d]);
    for (i = [0 : len(insert_bores) - 1])
        translate([col_x(i), row_c, 0])
            cylinder(d = boss_od, h = boss_h);
}

module plate() {
    difference() {
        plate_body();

        // Row A: holes for the printed pin
        for (i = [0 : len(clearances) - 1]) {
            d = pin_d + 2 * clearances[i];
            through_hole(d, col_x(i), row_a);
            label(str(clearances[i]), col_x(i), row_a - d / 2 - 1.2);
        }

        // Row B: 3 mm reference holes with diameter compensation
        for (i = [0 : len(comp_trials) - 1]) {
            d = ref_d + comp_trials[i];
            through_hole(d, col_x(i), row_b);
            label(str("+", comp_trials[i]), col_x(i), row_b - d / 2 - 1.2);
        }

        // Row C: blind bores in bosses for heat-set inserts
        for (i = [0 : len(insert_bores) - 1]) {
            translate([col_x(i), row_c, boss_h - insert_depth])
                cylinder(d = insert_bores[i], h = insert_depth + eps);
            label(str(insert_bores[i]), col_x(i), row_c - boss_od / 2 - 1);
        }
    }
}

module pin() {
    top_chamfer = 0.6;
    rotate_extrude()
        polygon([
            [0, 0],
            [pin_d / 2 - bed_chamfer, 0],
            [pin_d / 2, bed_chamfer],
            [pin_d / 2, pin_h - top_chamfer],
            [pin_d / 2 - top_chamfer, pin_h],
            [0, pin_h]
        ]);
}

if (part == "pin") pin();
else plate();
