---
name: electronics-lab
description: Set up a home electronics lab and get someone from zero to a working hardware project. Covers what to buy at three levels (beginner, expert, full kit wanker) as ready-to-order carts from shops in the user's country; safety basics for people new to electricity, batteries and soldering; wiring and soldering diagrams drawn as artifacts; flashing boards like ESP32 and Arduino; and getting parts 3D printed through a print service without owning a printer, including finding, checking or generating the model file. Use this whenever someone wants to start with electronics, Arduino, ESP32, Raspberry Pi, soldering or a hardware build (robot, sensor gadget, LED project, home automation, anything with a microcontroller); asks what tools or parts to buy or where to buy them; asks how to wire, solder, power or flash something; wants a case, mount or frame printed; or sends a photo of a board, a part or their wiring to check, even if they never say "lab".
---

# Home electronics lab

This skill turns "I want to build hardware" into a working bench and a first project that works. Judge your help by physical results: orders placed, parts that arrived, joints soldered, an LED blinking, a camera streaming, a case that fits. Advice the person doesn't act on doesn't count.

It grew out of real sessions where a complete beginner went from an empty desk to working ESP32 boards in about a week, with Claude doing the research, carts, diagrams, flashing and 3D-print checks. The mistakes from those sessions are in `references/pitfalls.md`; they are the most useful page in this folder.

## How to work with the person

- **End every reply with one next physical action** they can do today, and how they will know it worked. For example: "Put the black probe in COM and the red in VΩ, set the dial to the beep symbol, and touch the probes together. It should beep." Small, concrete steps beat a complete plan.
- **Give one pick per item.** Say which part to buy and why in one line. Offer alternatives only when asked, or when the pick is out of stock. A menu of three soldering irons stalls a beginner.
- **Use plain words.** The first time you name a part, say what it looks like and what it does: "a TP4056, a thumbnail-sized board that charges one lithium cell from USB-C". Never leave a part number, batch code or acronym unexplained ("U.FL" means nothing to a beginner; "the tiny round antenna socket, press the plug straight down until it clicks" does).
- **Check, don't assume.** Ask what they already own before you build a cart. Read labels in their photos instead of guessing. Check prices and stock live. Quote the maker's documentation for pinouts and polarity, not your memory. Label anything you infer as a guess.
- **Answer what was asked.** Don't lecture about scope, timelines or whether the project is wise unless there's a safety problem.
- **Don't let shopping become the project.** A cart is only a means to an end. Aim for parts ordered in the first session and a first project working within two days of delivery. Use the waiting time for software setup and a simulator (Step 4).

**The first reply to "what do I buy?"** Keep it to about 400 words; the detail lives in the cart page. Include:

1. The cart link, and whether it fits the budget, in the form "£X checked + N items not checked; delivery checked / not checked".
2. The five safety lines from Step 2 that matter for this project.
3. Three setup steps for the wait (Step 4).
4. One next physical action.

Diagrams come in a later turn, once the parts are ordered.

## Step 0: Keep a lab file

Hardware work spans many sessions, so keep a `LAB.md` that records what the person owns, what's on order, and where each project stands. Look for one first: in the current folder, or in the hardware notes folder if this is a notes or wiki repo. If the repo already has a hardware page or hub, or rules for its pages (frontmatter, an index, a log), keep the lab state there and follow those rules instead of adding a separate `LAB.md`. Otherwise, create one from `assets/LAB-template.md` after the intake. Update it whenever something is bought, arrives, breaks, or a project step works. Read it at the start of every hardware session, so you never recommend something they already own. That happened in real sessions with a multimeter and flux paste, and it costs trust.

## Step 1: Intake

Ask these in one message, and skip anything you already know from the lab file or the conversation:

1. **Country and city.** This decides the shops, delivery times, mains voltage, and whether there's a walk-in electronics market. Those are common in India and much of Asia; in most UK, European and US cities, online shops are the default.
2. **Level.** Show the three levels in one line each (see the table below). If they're unsure, use beginner.
3. **Budget.** A rough number is enough.
4. **First project.** If they have no idea, suggest one that fits what they care about (see "First projects" below).
5. **What they already own.** A photo of their desk or parts drawer is best.
6. **Their computer.** Mac (Apple chip or Intel), Windows or Linux. This decides drivers and flashing tools.

If there are small children or pets at home, mention lockable storage for batteries, button cells and magnets. Don't ask about it.

| Level | Who it's for | Rough cost |
|---|---|---|
| **Beginner** | Never soldered. Wants a working first project for the least money. | ₹5–9k · $150–300 · £120–250 |
| **Expert** | Builds regularly. Wants to measure and debug properly, and make their own boards and parts. | ₹1–2.5 lakh · $2–5k |
| **Full kit wanker** | Money isn't the limit. Wants a lab that can make almost anything, including machining metal and assembling circuit boards. | ₹15–50 lakh · $20–60k+ |

The full lists are in `references/kits.md`. Each level includes the one below it.

## Step 2: Safety briefing

Before the first power-up, and ideally before the parts arrive, give the short version below, tailored to the project. Read `references/safety.md` for the full rules, and use its sections on batteries, the soldering iron, and machines when they apply.

1. **Stay on the low-voltage side.** USB, batteries and a bench supply are fine. Never open, wire or modify anything that plugs into a wall socket (230 V in India, the UK and Europe; 120 V in North America). To switch a lamp or a fan, buy a certified smart plug and control that.
2. **Unplug before you move any wire.** Every time.
3. **Check before power.** With the power unplugged, the multimeter must *not* beep between + and GND. Check a battery's polarity with the meter before connecting it. Send a photo of the wiring for a check.
4. **Respect lithium batteries.** Never let the two leads touch. Cut and solder one lead at a time. Charge on a hard surface where you can see it, never overnight, and never a battery that is swollen, dented or hot.
5. **The iron is about 350 °C.** Keep it in its stand. Switch it off when you walk away. For a burn, hold it under cool running water for 20 minutes.
6. **Protect eyes and lungs.** Wear glasses when cutting leads. Use a fan that pulls the solder smoke away from your face. With leaded solder, wash your hands and keep food off the bench.
7. **Know the board's voltage.** Most modern boards run at 3.3 V, and 5 V on a signal pin can kill them. A pin can light one LED through a resistor, but it can't drive a motor, relay or LED strip directly.
8. **If something gets hot, smells or smokes, unplug first** and investigate after.

## Step 3: Build the cart

1. **Start from the level list** in `references/kits.md` and the country's shops in `references/shops.md`. Remove what they own. On a tight budget, buy only the beginner "first-project kit", and leave the "lab extras" for later.
2. **Add the first project's parts**, then do a **completeness pass**. For every part, ask four questions, and add whatever is missing:
   - How does it connect? Cables, connectors in matching pairs, header pins, wire, adapter boards for tiny surface-mount chips.
   - How is it powered? A battery, a charger board, a switch, the right USB cable.
   - How is it flashed? A USB data cable, or a programmer board for boards without USB.
   - How is it mounted? Foam tape, screws, a strap, a printed case.

   A real first-project cart missed adapter boards, battery plugs, the right USB cable, wire, headers, flux, tweezers, tape and a strap. This pass is what catches them.
3. **Check items live, most important first.** A beginner cart has 15–30 lines, and you may not be able to check them all. Go in this order:
   1. The board.
   2. The project's sensors and modules.
   3. The iron.
   4. The multimeter.
   5. Everything else.

   Where a shop has a search endpoint, use it to price many items per request; the fetch notes are in `references/shops.md`. For each item, record the price, stock and pack size, plus the shop's free-delivery threshold or minimum order. Show anything you couldn't check as "price not checked", with the spec and a search link. Never guess a price. Match the spec exactly:
   - USB-C or micro-USB
   - Pin count (the ESP32 DevKit comes with 30 or 38 pins)
   - Voltage, and 1-cell (3.7 V) or 2-cell (7.4 V) batteries
   - Connector family (JST-PH 2.0, JST-SH 1.0, Molex 1.25 and JST-XH all look alike)
   - Sensor model
   - Whether the listing is a "pack of 2"
4. **Put as much as possible in one shop** to reach free delivery. Split the cart only when a shop lacks an item.
5. **Show the cart as an artifact** (format below). If they're buying at a local market, also give a plain-text list to read out at the counter. Leave out checkboxes and dashes if they ask for that.
6. **If they ask you to fill their cart in the browser,** you may add the items. Never check out or pay; they do that. Before they pay, compare the shop's cart with your list, including quantities, pack sizes and anything that silently failed to add. After they order, compare the order confirmation with the list too. In one real order, an item that was in the cart never made it into the order.

**Cart artifact.** Publish it with the Artifact tool when available, after loading the `artifact-design` skill. Otherwise write a self-contained HTML file and open it. Include:

- **Header:** the checked total, the number of items not checked, whether delivery was checked, whether it fits the budget, the number of shops, and the date checked.
- **One section per shop**, in buying order:
  - The subtotal, and whether it reaches free delivery.
  - Two groups inside each shop: "Lab tools" and "For the first project".
  - For each item: the shop's own product photo, a plain name, one line on what it does, the spec to match, quantity × price, and a link.
  - Warnings where they apply, such as "pack of 2: set quantity 1".
- **Later (not in the total):** one collapsed list at the end, across all shops.
- **Already owned, don't buy:** a collapsed list, only if they own something.
- **Checkboxes** to mark items bought, saved in the browser.

If you filled a basket in the browser, check that its subtotal matches the page. Keep photos from overlapping text, and test the page at phone width by loading it inside a 375 px-wide iframe; headless Chrome won't lay out narrower than 500 px. A real cart page broke on both.

## Step 4: While parts are on the way

Spend the wait on things that make arrival day go smoothly:

- **Install the toolchain and test it.** That's Arduino IDE or `arduino-cli`, `esptool`, and the board package. Then compile an empty sketch for the target board. Fixing setup problems now means arrival day goes to hardware. `references/pitfalls.md` lists the setup problems hit on a Mac, such as Rosetta and drivers.
- **Build the first project in a simulator.** [Wokwi](https://wokwi.com) runs ESP32, Arduino and Raspberry Pi Pico circuits in the browser. The wiring and code carry straight over to the real parts.
- **Draw the wiring diagram** for the first project (Step 6), so it's ready when the box opens.

## Step 5: The first hour when the parts arrive

Go through these in order. Each one has a check:

1. **Unbox and compare against the cart.** Ask for a photo. Read the markings to catch substitutes. A camera sold as an OV2640 turned out to be a GC2145; the ribbon was marked "M21-45". A local shop handed over a different power module from the one asked for.
2. **Test the multimeter.** The probes touched together should beep. A battery should read about its rated voltage. Black probe in COM, red in VΩ.
3. **Prepare the iron.** Heat it to 330–350 °C for leaded solder, or 350–380 °C for lead-free. Melt a little solder onto the tip and wipe it on brass wool. The tip should look shiny and silver.
4. **Make the first joints** on a spare header strip or a scrap of perfboard, before touching a real board. Each joint should look like a small shiny cone, not a ball.
5. **Run the first program.** Use the blink sketch, or the board's built-in example. The LED should blink, or the expected text should appear in the serial monitor.
6. **Update `LAB.md`.**

## Step 6: A diagram for every connection

Before the person wires or solders anything, draw it. Read `references/diagrams.md`; it has the full rules, and load the `artifact-diagramming` skill as well. The essentials:

- Draw the board the way it looks in their photo, the same way round, with each pin labelled with the text printed on the board. Read the pin order off the board or the maker's pinout. Don't infer it from the layout. An inferred pin order had to be corrected in a real session.
- Number and colour every wire: red for +, black for GND. Under the drawing, add a table with the number, from, to, colour and why.
- Show the breadboard's real row numbers, which holes are joined inside, and any split in the power rails. A board placed one row off turned a 5 V wire into a GND wire. A photo caught it before power was applied.
- Spell out timing: what goes in before plugging in, and what comes out after uploading. For example, the "flash mode" wire.
- End with a check before power, done with the USB unplugged. List the pairs that must beep, and the pairs that must not beep (+ to GND). Then give the voltages expected after power-up.
- Then ask for a photo of the real wiring. Compare it wire by wire with the table, and say "matches" or name the exact wire that's wrong, before they power up.
- When something gets corrected, update the same artifact at the same link and say what changed.

For soldering, draw a close-up of the pads. Show which wire goes to which pad, how you know which pad is + when it isn't labelled (quote the maker's rule), and the order of steps.

## Step 7: 3D-printed parts without a printer

When a project needs a case, mount, clip or frame, read `references/3d-printing.md`. In short:

1. **Find a proven file.** Search Printables, MakerWorld and Thingiverse; Printables' API gets past the 403s. Prefer designs with many posted builds ("makes") over an exact size match with no builds. Likes and downloads don't count as builds. Read the comments and remixes for failure reports, and check the licence.
2. **Or generate it,** when nothing proven fits. Write a parametric OpenSCAD file from the parts' measured dimensions, using calipers or the datasheet, and render it to STL. If OpenSCAD can't be installed, use the browser-based OpenSCAD Playground. An unrendered file is never "checked", and services don't accept `.scad`.
3. **Check it** before anything is ordered, with all the parts of the design in one run:

   ```bash
   python3 -I <skill-folder>/scripts/check_print.py base.stl lid.stl --material PETG --preview case.png
   ```

   `<skill-folder>` is this skill's directory, as an absolute path. The script reports:
   - the size, and whether the mesh is one sealed solid;
   - the volume and weight;
   - the best orientation, and the area that faces down;
   - a preview, drawn to scale.

   Show the preview to the person. Then measure what decides fit:
   - `--section z=<height>` lists holes, clip openings and outlines.
   - `--probe z=<h>,y=<y>` measures along a line, which finds wall thicknesses and openings cut into an edge.

   Compare matching parts, such as a lid's lip against the box's opening (0.2–0.3 mm per side). Then run the completeness pass on the case: female–female jumpers once the breadboard goes, screws, and foam tape.
4. **Order from a print service** in their country (see `references/shops.md`). Pick the material for the job: PETG for anything that flexes, gets warm, or might crash. Order 2–3 copies when the service has a minimum order anyway. A fit test at a service that posts parts is a whole extra order, so measure first or add the test to an order that's already going.

## Step 8: Flash, run and debug

Claude can do most of the computer side: install tools, compile, flash, and read the serial output. The person only plugs and replugs. To make that safe:

- **Confirm the port and the board before writing anything.** How depends on the board:
  - **USB-serial chip** (most ESP32 DevKits, with a CH340 or CP2102 chip near the USB port): run `esptool chip-id`. It reads only.
  - **Native USB** (ESP32-S3, C3 and C6, and XIAO boards): the port shows as `usbmodem` or `ttyACM`. If an upload fails, hold BOOT, tap RESET, release BOOT, and try again.
  - **Arduino Nano ESP32:** upload through the Arduino core (IDE or `arduino-cli`), which uses DFU. If it stops showing up, double-tap reset to enter bootloader mode.
  - **Raspberry Pi Pico:** hold BOOTSEL while plugging in. It appears as a USB drive.
- **If no port appears, swap the USB cable first.** Charge-only cables are the most common cause.
- **Never ask for Wi-Fi passwords in chat.** Create a `secrets.h` or config file, open it in their editor for them to type into, and check it's filled in without printing it.
- **Most ESP32 boards join only 2.4 GHz Wi-Fi.**
- **Start the serial listener before pressing reset**, so the boot messages aren't missed.

The full list is under "Flashing and software" in `references/pitfalls.md`.

## Checking photos

Photos are the best way to verify hardware. Ask for a well-lit photo taken straight down, of both sides of the board when the labels matter. Crop and zoom to read small print (on a Mac, `sips`; otherwise Python's PIL) before you ask for a retake. If you still can't read a label, say so and ask for a closer photo of that spot. Don't guess. Treat batch codes printed on chips ("0729HS") as batch codes, not model numbers.

## First projects

Suggest one, matched to what the person cares about. `references/projects.md` has a step-by-step guide for each: parts, pins, the build order, known problems, and the test that proves it works.

| Interest | First project | Key parts |
|---|---|---|
| Home, plants | Soil-moisture sensor that messages the phone | Any ESP32 board, capacitive soil sensor |
| Desk gadgets | Weather or calendar display | ESP32 and a small OLED or e-paper screen |
| Lights | LED strip that changes with the time of day or with music | ESP32, addressable LED strip, 5 V supply |
| Things that move | Two-wheel robot | ESP32, motor driver board, gear motors, battery |
| Data | Room monitor that logs temperature, humidity and air quality to a web page | ESP32, BME280 or SCD40 sensor |

Every project climbs the same ladder. Name the next rung each session:

1. **Works on the breadboard over USB.**
2. **Runs on a battery.** The simplest version is a USB power bank. Soldered cells come last.
3. **Has a switch and a charger.**
4. **Lives in a printed case or mount.**
5. **Is soldered onto perfboard, or a custom board, so it survives being carried around.**

## Reference files

Read each one only when its step comes up:

- `references/kits.md`: tools and parts for each level, with specs to match and typical prices. For building a cart.
- `references/shops.md`: shops, local markets, 3D-print services and fetch notes by country, plus buying traps. For building a cart or ordering prints.
- `references/projects.md`: step-by-step guides for the first projects. Read it once the project is chosen.
- `references/safety.md`: the full safety rules, covering electricity, batteries, soldering, fumes, protecting components, 3D printers, lasers and CNC. The Step 2 summary is enough for the first reply. Read the battery and soldering sections when that work starts.
- `references/diagrams.md`: how to draw wiring, breadboard and soldering diagrams as artifacts. Only when drawing one.
- `references/3d-printing.md`: finding, checking and generating files, design rules, materials and ordering.
- `references/pitfalls.md`: real mistakes from real builds, and how to avoid them. Skim it once per session.
- `scripts/check_print.py`: checks STL, OBJ or 3MF files and renders a preview. It uses only the Python standard library.
- `assets/LAB-template.md`: the starting point for the person's lab file.
