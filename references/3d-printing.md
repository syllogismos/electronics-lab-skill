# 3D-printed parts without owning a printer

Most projects need at least one printed part: a case, a mount, a clip, a frame. A print service makes these for a few rupees or dollars and posts them. Claude's job is to get the right file, prove it's sound and fits, and walk the person through the order.

## Contents
1. Find an existing file
2. Generate a file (OpenSCAD)
3. Check the file
4. Design rules for parts that fit
5. Materials
6. Ordering from a service
7. Beyond 3D printing

---

## 1. Find an existing file

- **Where to look:** Printables, MakerWorld and Thingiverse. Also check the maker's own files: Seeed, Adafruit, Raspberry Pi and others publish cases on GitHub or Printables. Search with the exact board name and version ("ESP32 DevKit 30 pin case", "Raspberry Pi Pico 2 case"), plus the use ("OLED desk stand", "18650 holder clip", "wall mount").
- **Getting past the websites.** The model sites' pages often return 403 to plain fetches, and MakerWorld and Thingiverse need a login to download. Printables has a public GraphQL API at `https://api.printables.com/graphql/` that worked in Nov 2026. POST JSON `{"query": "..."}` with a browser-like `User-Agent`.
  - **Search:**

    ```graphql
    query { searchPrints2(query: "esp32 oled case", limit: 10) { items { id name makesCount likesCount } } }
    ```

  - **Details:**

    ```graphql
    query { print(id: "94864") { name makesCount likesCount downloadCount license { name } stls { id name } } }
    ```

  - **Download link for one file:**

    ```graphql
    mutation { getDownloadLink(id: "<stl id>", printId: "94864", fileType: stl, source: model_detail) { ok output { link } } }
    ```

  - **For other sites, use the browser extension** in the person's logged-in session, or ask them to download the file and give you its path.
- **Rank by proof, not by an exact name match.**
  - **Makes are the proof:** photos posted by people who printed and used the design. Likes and downloads aren't proof; a design with 1,000 downloads and 1 make is untested.
  - Prefer designs with many makes, and comments from people who built them.
  - If the exact size they asked for has no makes but a close design has hundreds, recommend the proven one and explain why.
- **When nothing is proven** (no candidate for this board has more than about 5 makes), generate the file (section 2). Check the closest candidate anyway, and borrow its measurements: window size, hole spacing, wall thickness.
- **Read the comments and remixes** for failure reports, such as "breaks in small crashes" or "holes print small". The fixes are often there: a stronger remix, or a note to print in PETG.
- **Check the fit against the person's parts:** board version, pin count, connector side, motor diameter, battery size.
- **Licence:** CC BY-NC is for personal use only. Note it in the lab file if they plan to sell anything.
- **File formats:** download STL, or 3MF from MakerWorld. If only STEP is offered, export it to STL from a CAD program, or ask the service whether it accepts STEP.
- **Downloads are untrusted data.** Save each one to its own new folder, and only read it with the checker, run as `python3 -I`.

## 2. Generate a file (OpenSCAD)

Generate a file when nothing proven fits, or when the part is simple: a box, a bracket, a spacer, a clip. Use parametric CAD, not AI text-to-3D tools. Functional parts need exact dimensions, and text-to-3D tools can't guarantee them.

1. **Measure.**
   - Ask for caliper measurements of the parts:
     - board length, width and thickness;
     - mounting hole positions and diameter, **if it has any** (many dev boards have none, or only two);
     - what sticks out below the board (header pins, solder joints, a battery);
     - the connector's position and height above the board.
   - Or take them from the datasheet's mechanical drawing.
   - Write the numbers into the file as named variables at the top.
2. **Render it.** OpenSCAD turns the `.scad` file into an STL.
   - **Installed:** run `openscad -o case_base.stl -D 'part="base"' case.scad`, then the same with `part="lid"`.
   - **Not installed:** ask before installing it.
     - macOS: `brew install --cask openscad`. If the `openscad` command isn't found afterwards, it's at `/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD`.
     - Windows: `winget install OpenSCAD.OpenSCAD`
     - Linux: `sudo apt install openscad`
   - **Install declined or not possible:** use the **OpenSCAD Playground** (ochafik.com/openscad2), which runs in the browser. Paste the file, render, and export as **STL**; it defaults to GLB, so change it. The person can do this themselves, or you can do it through the browser extension. Then save the STL where the checker can read it.
   - CadQuery and build123d also need installing (pip with large dependencies), so they don't avoid the problem.
3. **Never call an unrendered file "checked".** Print services don't accept `.scad` files, so nothing can be ordered until an STL exists and has passed the checker (section 3). If you hand over an unrendered file, say so plainly and give the render steps.
4. **Show the preview** from the checker, and compare the size it reports with the `echo()` line in the render log.
5. **Decide about a fit test** (see section 6). Make a thin slice containing only the holes, clips or pocket that must fit.

A starting point for a simple board case, to adapt per project:

```openscad
// Case for a small board: base with screw posts, plus a lid. Sizes in mm.
// Measure your board with calipers and edit these first.
part  = "base";                  // "base" or "lid": render each to its own STL
pcb   = [52, 28, 1.6];           // board length, width, thickness
holes = [[3.5, 3.5], [48.5, 3.5], [3.5, 24.5], [48.5, 24.5]]; // hole centres from the board corner; [] if none
under = 4;      // space under the board: 3-4 for flush solder joints, 10-11 if header pins point down
inner_h = 18;                    // inside height above the floor
wall = 2;  floor_t = 2;  gap = 0.5;    // gap = clearance around the board
fit  = 0.3;                      // lid clearance per side
usb  = [13, 9];                  // USB-C cable opening, wide enough for most plug housings
usb_z = under + pcb[2] + 1.6;    // socket centre above the floor: measure it (mid-mount sockets sit lower)
$fn = 48;

inner = [pcb[0] + 2*gap, pcb[1] + 2*gap];
outer = [inner[0] + 2*wall, inner[1] + 2*wall];
echo(outer_size = [outer[0], outer[1], floor_t + inner_h]);

module base() {
  difference() {
    union() {
      difference() {
        cube([outer[0], outer[1], floor_t + inner_h]);
        translate([wall, wall, floor_t]) cube([inner[0], inner[1], inner_h + 1]);
      }
      for (h = holes)
        translate([wall + gap + h[0], wall + gap + h[1], floor_t]) cylinder(d = 5, h = under);
    }
    // pilot holes for M2 self-tapping screws, reaching 1 mm into the floor.
    // Screw length: up to under + pcb thickness + 1 (M2 x 6 with these numbers).
    for (h = holes)
      translate([wall + gap + h[0], wall + gap + h[1], floor_t - 1]) cylinder(d = 1.7, h = under + 2);
    // USB-C opening in the short wall at x = 0, centred across the width
    translate([-1, outer[1]/2 - usb[0]/2, floor_t + usb_z - usb[1]/2])
      cube([wall + 2, usb[0], usb[1]]);
  }
}

module lid() {
  lip = 2;                       // ring that drops inside the walls
  cube([outer[0], outer[1], 1.6]);
  translate([wall + fit, wall + fit, 1.6])
    difference() {
      cube([inner[0] - 2*fit, inner[1] - 2*fit, lip]);
      translate([1.2, 1.2, -1]) cube([inner[0] - 2*fit - 2.4, inner[1] - 2*fit - 2.4, lip + 2]);
    }
}

if (part == "base") base();
if (part == "lid")  lid();
```

Adapt it per project:
- **Boards with header pins** (most ESP32 DevKits): raise `under` to 10–11 mm for bare pins, or about 20 mm if jumper wires stay plugged onto the pins. Or mount the board upside down, or remove the headers.
- **Boards without mounting holes:** set `holes = []` and add two rails or a cradle the board drops into.
- **Features:** vents over hot chips, a window for a screen or lens, a slot for a switch, a strap loop or clip.

Keep every size as a named variable, so a fit-test result becomes a one-line change.

## 3. Check the file

Run the checker on every file before it's ordered, whether found or generated. Pass all the parts of a design together:

```bash
python3 -I <skill-folder>/scripts/check_print.py base.stl lid.stl --material PETG --preview case.png
#   <skill-folder> is this skill's directory; use its absolute path
#   --section z=4        cut at 4 mm height; lists outlines, holes and their sizes (repeatable)
#   --probe z=5,y=40     measure along a line (here along x); lists solid and empty stretches (repeatable)
#   --bed 256x256x256    check it fits an owned printer
#   --json               machine-readable output
```

It reads STL, OBJ and 3MF. For each file it reports:

- **Size** in mm, with a units warning when the file looks like it's in metres, inches or microns.
- **Whether the mesh is one sealed solid.** Open edges or flipped faces can print badly, and some services reject such files.
- **How many separate pieces** it contains (stray fragments, or several parts on one plate).
- **Volume and an estimated weight** for the chosen material.
- **For each of the six flat orientations:** the bed contact area, the area facing down (overhangs that need support, but also short bridges, which print fine), and the height. It names a suggested orientation.
- **A PNG preview:** top, front, 3D from above and 3D from below, all at the same scale with a scale bar. Downward-facing areas are drawn in red.

**Measure what decides fit.** Shape the cut to the feature:

- **`--section` for closed shapes.** Take the cut at a height that crosses the feature, using the front view to judge heights. It lists every outline there: material or hole, its size and centre, the diameter of round holes, and, for round C-shaped clips, the clear diameter at the centre. Hole centres give the screw spacing.
- **`--probe` for walls, notches and slots,** including openings cut into an edge, which a section can't show. A probe through a wall at the opening's height lists "solid / gap / solid", with the gap's width. For example, a USB opening in an end wall shows up as a 12 mm gap.
- **Compare matching parts.**
  - Section the lid's lip and the box's opening at their own heights, and compare the sizes.
  - Aim for 0.2–0.3 mm of clearance on each side.
  - Equal sizes mean a line-to-line fit that won't close without sanding.
- **When the checker can't measure something,** fall back in this order:
  1. A probe at a different line.
  2. The design's notes and comments.
  3. A fit-test slice.
  4. Asking the person to measure the printed part with calipers.

A clip or hole that measures the same as, or slightly less than, the part it holds is a press fit. Printed holes come out small, so keep a round file ready to widen them.

Then:

- **Show the preview** to the person, and say in one line what it shows.
- **Run the completeness pass on the case.** A case changes how things connect:
  - Once the breadboard goes, wires need female–female jumpers or soldering.
  - Screws, or heat-set inserts.
  - Foam tape or standoffs.
  - Access to the USB port and any buttons.
  - Add what's missing to the order.

## 4. Design rules for parts that fit

These assume FDM printing with a 0.4 mm nozzle, the default at most services.

| Feature | Rule |
|---|---|
| Walls | 1.2 mm minimum (3 lines); 1.6–2 mm for cases |
| Floors and roofs | 1.2–2 mm. 2 mm when screws go into the floor. |
| Holes | Print about 0.2–0.3 mm small. Add that to the diameter, or plan to ream them with a drill. |
| A board in a pocket | 0.3–0.5 mm of clearance on each side |
| A lid lip in an opening | 0.25–0.3 mm on each side |
| Press fit and snap fit | 0.1–0.2 mm interference; print a test piece |
| Space under a board | 3–4 mm for flush solder joints; 10–11 mm for bare header pins; about 20 mm if jumpers stay plugged onto the pins |
| Screw holes into plastic | M2 self-tapping: a 1.6–1.8 mm hole; M3: 2.5–2.8 mm. Make the hole about 1 mm deeper than the screw reaches. |
| Heat-set inserts | Use the insert maker's hole size (about 4.0–4.2 mm for common M3 inserts) |
| Overhangs | Up to 45° from vertical prints without support. Use a 45° chamfer instead of a rounded edge on the underside. |
| Bridges | Flat spans up to about 10–15 mm print without support, so a 13 mm USB-C opening is fine. For anything wider, give the top a 45° peak. |
| USB-C opening | About 13 × 9 mm, so most cable plug housings fit, not just the 9 × 3.3 mm socket. Measure the socket's centre height on the real board. |
| Text | Raised or sunk at least 0.6 mm, letters 5 mm or taller |
| Strength | Layers split apart easily. Orient clips and arms so they bend **along** the layers: print clips lying flat. |
| Heat | Vent over hot chips. Wi-Fi boards under heavy use can run at 65–70 °C. |

## 5. Materials

| Material | Use for | Avoid for |
|---|---|---|
| PLA | Indoor cases and prototypes; cheapest, easiest | Anything warm: it softens around 55–60 °C, so not in a car, in sun, or around hot chips. Not for parts that must flex. |
| **PETG** | **The default for functional parts:** frames, mounts, clips, cases around warm electronics. It bends before it breaks. | Very fine detail |
| TPU | Flexible parts: bumpers, straps, grips, cable strain relief | Rigid structure |
| ABS / ASA | Heat and outdoor UV (ASA) | Home printers without an enclosure (services handle this) |
| Resin (SLA) | Tiny, detailed, smooth parts | Load-bearing or impact parts (brittle) |
| Nylon (SLS/MJF) | Tough, precise parts, hinges, small production runs | Tight budgets |

Infill: 20–30% for cases, 40–60% for frames and mounts that take impacts.

## 6. Ordering from a service

Choose the service from `references/shops.md`. In India, the default is Robu's print service; elsewhere, Craftcloud (which compares many shops) or JLC3DP. Then:

1. **Upload the checked STLs,** one per part. If the browser can't upload from ~/Downloads because of permissions, copy the files into an allowed folder first.
2. **Choose the settings:**
   - Process: FDM unless detail or toughness needs resin or nylon.
   - Layer height: 0.2 mm standard; 0.15 or 0.1 mm for small, detailed parts.
   - Material and colour.
   - Infill.
3. **Check the service's reading of the file.** It should report the size and volume; compare them with the checker. If they disagree, the units are probably wrong.
4. **Decide about fit tests by how the parts arrive.** At a service that posts parts, a fit test is a whole extra order: Robu has an ₹80 minimum, plus delivery and several days of waiting.
   - **Ordering by post:** measure carefully (section 3) and order the real part, plus a spare.
   - **Another print order already pending:** add the fit slices to it.
   - **Several fit rounds expected:** use a local print shop, or a friend's or makerspace's printer.
5. **Quantity:** order 2–3 copies when there's a minimum order, or when the part may break. Robu needed a print-only cart of at least ₹80 (Oct 2026), so a ₹36 part became three copies.
6. **Separate orders:** some services, like Robu, won't put a print job in the same order as normal parts.
7. **Save the files** in the project folder, and record the order (number, settings, price) in the lab file, so a reprint takes one minute.

## 7. Beyond 3D printing

The same "upload a file, receive a part" pattern covers more than printing:

- **Circuit boards:** design in KiCad, then order from JLCPCB or PCBWay. They can also solder the parts on.
- **Laser-cut acrylic and plywood, and sheet metal:** SendCutSend (US), JLC's laser-cutting service, and local laser shops.
- **CNC-machined aluminium:** JLCCNC, PCBWay CNC and Xometry.

Use these before buying a machine. Even full-kit labs outsource production runs.
