# OpenSCAD

Read this when the chosen tool is OpenSCAD.

## File layout

```scad
// models/part-name.scad — one-line description of the part
/* [Size] */
W = 60;      // outer width, mm
D = 40;      // outer depth, mm
H = 25;      // outer height, mm
WALL = 2.0;  // wall and floor thickness, mm

/* [Fit] */
FIT = 0.2;        // slip clearance per side, mm
HOLE_COMP = 0.2;  // added to vertical hole diameters, mm

/* [Hidden] */
eps = 0.01;  // overlap so cuts and joins never share a face
$fa = $preview ? 6 : 1;    // coarse while previewing, fine for export
$fs = $preview ? 1 : 0.4;

// Open-top box: base body sits on Z=0 with a floor of WALL.
difference() {
    cube([W, D, H]);
    translate([WALL, WALL, WALL]) cube([W - 2*WALL, D - 2*WALL, H]);
}
```

- Keep every dimension as a named parameter at the top with a units comment.
  The `/* [Group] */` comments make the OpenSCAD Customizer show them as sliders.
- Place the part on Z=0 in its print orientation.
- Cutters must pass through the surfaces they cut by `eps` (the inner cube above is
  taller than needed for that reason). Additions must overlap the body by `eps`.
- Use `assert()` for impossible parameter combinations, e.g.
  `assert(WALL * 2 < W, "WALL too thick for W");`.
- For multi-part designs add `part = "base"; // [base, lid]` and select with
  `-D 'part="lid"'` at export, so each STL is a single solid.

## Curves and holes

OpenSCAD builds circles from straight segments placed inside the true circle, so a
coarse circle prints small. Keep `$fs` ≤ 0.4 and `$fa` ≤ 2 for export (above). For
fitted holes add `HOLE_COMP` to the diameter.

Horizontal hole that prints without support:
```scad
module teardrop(d, h) {
    rotate([90, 0, 0]) linear_extrude(height = h, center = true)
        union() {
            circle(d = d);
            rotate(45) square(d / 2);   // 45° pointed roof
        }
}
```

Bottom chamfer to hide elephant's foot (use instead of a plain `cube` for the base):
```scad
module chamfered_box(size, c = 0.5) {
    hull() {
        translate([c, c, 0]) cube([size.x - 2*c, size.y - 2*c, eps]);
        translate([0, 0, c]) cube([size.x, size.y, size.z - c]);
    }
}
```

## Build, check, preview

```bash
# Export STL (also catches syntax errors)
openscad -o out/part.stl models/part.scad

# Mesh and size check (scripts/ is next to this file)
python3 <skill-dir>/scripts/check_stl.py out/part.stl --expect 60x40x25

# Preview images to look at: one angled, one from above
openscad -o out/part-iso.png --render --imgsize=900,700 --autocenter --viewall \
  --colorscheme=Tomorrow models/part.scad
openscad -o out/part-top.png --render --imgsize=900,700 --autocenter --viewall \
  --camera=0,0,0,0,0,0,200 --projection=o --colorscheme=Tomorrow models/part.scad
```

- Read OpenSCAD's console output: `WARNING:` lines (undefined variables, unknown
  modules) mean the model is not what the code looks like, even if export succeeded.
- Newer builds offer `--backend=manifold`, which renders much faster. Use it if
  `openscad --help` lists `--backend`.
- Headless servers need `xvfb-run -a` in front of the PNG commands.

## Libraries

Only use a library (BOSL2, NopSCADlib) when the project already does, or the user
agrees; it adds a dependency anyone opening the file must install.
