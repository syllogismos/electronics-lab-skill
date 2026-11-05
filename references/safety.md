# Safety: protect yourself, your home and your parts

Give the short version from SKILL.md before the first power-up. Use the sections below when the project touches that area: batteries for any wireless build, machines for expert and full-kit labs. Explain the reason behind each rule; people follow rules they understand.

## Contents
1. Electricity basics for people who have never thought about it
2. Mains: the hard line
3. Lithium batteries
4. Soldering iron and hot air
5. Fumes, lead and chemicals
6. Eyes, hands and small parts
7. Protecting the components
8. Using the multimeter safely
9. 3D printers, lasers and CNC
10. Fire and first aid
11. Kids and pets

---

## 1. Electricity basics

- **Voltage is the push, current is the flow.**
  - The low voltages used here (3.3 V, 5 V, a 3.7 V battery, up to about 24 V) can't push a dangerous current through dry skin, which is why hobby electronics is safe to touch.
  - The danger at low voltage is **heat and fire**. A short circuit lets a battery or supply dump all its current through a wire or a part, and things get hot fast.
- **A short circuit** means + touching − (GND) with nothing in between. On a breadboard it is one misplaced wire. The fix is to check before power (below) and to use a supply that limits current.
- **GND is the shared reference.** Every part of a circuit that talks to another part must share GND. Two supplies with no common GND is a classic "it doesn't work" bug.

## 2. Mains: the hard line

Wall power (230 V in India, the UK, Europe and Australia; 120 V in North America; 100 V in Japan) can kill. Beginners and most experts should never:

- open, wire or modify anything that plugs into a wall socket;
- build relay boards that switch wall power. The cheap blue relay modules have poor isolation and exposed contacts;
- clip an oscilloscope's ground lead to anything connected to mains. It creates a short through the scope's earth.

Instead:

- **To control wall-powered devices,** use a certified smart plug or switch and control it over Wi-Fi.
- **Power projects from certified USB adapters, power banks or batteries,** or from a bench supply plugged into a power strip with a switch and surge protection, ideally on an RCD/GFCI-protected outlet.
- **Mains work belongs to trained people** with an isolation transformer, a differential probe and CAT-rated meters.

## 3. Lithium batteries

Lithium cells (LiPo pouches, 18650s, phone batteries) hold enough energy to start a fire that's hard to put out. Most hobby fires come from batteries.

- **Never short the leads.**
  - When cutting a battery's wires, cut **one at a time** and tape the cut end before cutting the other.
  - Solder one lead, insulate it, then do the other. Keep the iron away from the pouch.
  - Don't let loose cells rattle around with keys, coins or tools.
- **Check polarity with a multimeter before connecting.** Red isn't a guarantee, and cheap batteries with JST plugs are sometimes wired the opposite way to the board's socket. Put the red probe on the wire you think is +; a positive reading of about 3.7 V means it is.
- **Know the voltage you're buying.**
  - "1S" is one cell, 3.7 V nominal: 4.2 V full, about 3.0 V empty.
  - "2S" is 7.4 V. It will destroy a board made for one cell.
  - A raw cell isn't a 5 V supply: on a 5 V pin the board browns out. It isn't a 3.3 V supply either: 4.2 V on a 3.3 V pin is too much. Use a charger or boost board, a regulator, or a board with its own battery input.
- **Use protection.** Pick cells with a protection board, or a charger board with protection (a TP4056 with separate OUT pads). The protection stops over-discharge, which ruins cells, and short circuits.
- **Charging:**
  - On a hard, non-flammable surface (tile, metal tray, or a LiPo bag), where you can see it.
  - Never overnight or while out.
  - Not when the cell is below 0 °C.
  - Multi-cell packs only on a **balance charger**.
- **Retire a battery** that is swollen ("puffy"), dented, punctured, hot when idle, or smells sweet. Don't charge it. Put it in a metal box or a pot of sand outdoors, and take it to a battery recycling point. Never put batteries in household rubbish.
- **Storage:** about 3.8 V per cell (half full) for long storage, in a fire-resistant bag or a metal box with a loose lid.
- **Fake 18650s:** cells claiming 6,000–9,900 mAh are fake. Real 18650s top out around 3,500 mAh. Buy known brands from reputable shops.

## 4. Soldering iron and hot air

- **The tip is 300–400 °C.** It always goes back in its stand, never on the desk.
- **Route the cord** so you can't snag it and pull the iron off the bench.
- **Switch it off** when you leave the desk, even for a minute. Many irons have auto-sleep; turn it on.
- **Never catch a falling iron.** Step back and let it drop.
- **Working temperature:**
  - About 330–350 °C for leaded solder; 350–380 °C for lead-free.
  - Hotter isn't better. It burns the flux and lifts pads.
  - Hold the tip on a joint for 2–3 seconds, then stop and let it cool before trying again.
- **Hot air** (300–450 °C) melts plastic connectors, cables and nearby parts. Shield them with Kapton tape or aluminium foil.

## 5. Fumes, lead and chemicals

- **The smoke from soldering is mostly burnt flux**, which irritates the lungs and can cause asthma over time. Use a fan that pulls the smoke away from your face (beginner), or a carbon-filter extractor (expert). Open a window.
- **Leaded solder:** the lead doesn't evaporate at soldering temperatures; the risk is hands to mouth. Wash your hands after soldering, keep food and drink off the bench, and don't let children handle the solder.
- **Isopropyl alcohol** is flammable. Keep it away from the iron, and close the bottle.
- **Flux residue:** clean "no-clean" flux off with alcohol anyway when it's sticky. Activated (water-soluble) flux must be cleaned off, or it corrodes the joints.

## 6. Eyes, hands and small parts

- **Wear safety glasses when clipping leads** (the cut ends fly), when soldering (solder can spit), and when drilling or using a rotary tool.
- **Cut away from yourself** with craft knives.
- **Hot glue** sticks to skin at about 200 °C. Keep a bowl of cold water nearby.
- **Keep a magnet or a tray** for screws and small parts. Lost parts end up in feet, pets and vacuum cleaners.

## 7. Protecting the components

These rules save parts and hours of debugging.

- **Check before power** (with the USB unplugged):
  - The multimeter must **not** beep between + and GND, on each supply rail.
  - Every planned connection should beep.
  - Then power up and touch-test: after 10 seconds, touch each chip and regulator. Warm is fine; too hot to keep a finger on means unplug.
- **Use one power source at a time,** unless the design says otherwise. USB plus a battery plus VIN can back-feed into the computer's USB port or the battery.
- **Use a current limit.** On a bench supply, start at the expected voltage with a 100–200 mA limit. If the current jumps to the limit, something is shorted, and the limit kept it from burning.
- **Respect logic voltage.**
  - 3.3 V boards (ESP32, Raspberry Pi Pico, Raspberry Pi) can be damaged by 5 V on a signal pin.
  - Use a level shifter, or a voltage divider for slow signals.
  - Power 5 V sensors from 5 V, but check what voltage their signal pins send back.
- **Pin current limits:**
  - An ESP32 pin is happy at about 20 mA, enough for one LED with a 220–330 Ω resistor. A Pico pin gives less.
  - Motors, relay coils, solenoids, buzzers and LED strips need a transistor or MOSFET (or a driver board) and a separate supply, with GNDs joined.
  - Anything with a coil also needs a **diode** across it, to absorb the voltage spike when it switches off.
- **Polarity matters.** Electrolytic capacitors (they can burst), LEDs, diodes, batteries and chips (match the notch or dot to the diagram) only work one way round.
- **Static (ESD):**
  - Touch something grounded, or a metal part of the computer's case, before handling boards.
  - Hold boards by their edges.
  - Keep boards in their antistatic bags until needed.
  - Avoid carpet in dry weather.
- **Ribbons and tiny connectors:**
  - Camera ribbons need the latch opened before insertion, then closed. Check that the ribbon is fully seated.
  - U.FL antenna plugs press straight down until they click, and lift straight up. Don't pivot them.
  - Running a Wi-Fi board without its antenna fitted gives poor range.
- **Heat while running.** Wi-Fi boards get hot under heavy use, and can pass 65–70 °C. Fit the supplied heatsink, leave air gaps, and don't seal it in PLA, which softens near 55–60 °C.
- **Don't hot-plug sensors.** Plug them in with the power off.

## 8. Using the multimeter safely

- **Black probe in COM; red probe in VΩ** for nearly everything: voltage, resistance, continuity.
- **The mA and 10 A jacks are only for measuring current,** with the meter placed *in series* in the circuit. If you then measure voltage with the red probe still in an A jack, you short the source; at best you blow the meter's fuse. Move the red probe back to VΩ right after any current measurement.
- **Measure resistance and continuity only with the power off.**
- **Meters are rated by category** (CAT II, III and IV). A cheap meter isn't safe on mains, which is one more reason to stay off mains.

## 9. 3D printers, lasers and CNC

- **FDM 3D printers:**
  - The nozzle runs at about 200–260 °C and the bed at 60–110 °C.
  - Watch the first layers of every new print. Don't run unattended prints until the printer has proven reliable.
  - Put a smoke detector above it.
  - ABS and ASA give off fumes: enclose and ventilate the printer.
- **Resin printers:**
  - Liquid resin is a skin sensitizer. Allergies build with exposure.
  - Wear nitrile gloves and glasses, and ventilate the room.
  - Cure waste resin fully in sunlight or UV before throwing it away.
  - IPA wash baths are flammable.
- **Laser cutters and engravers:**
  - Never leave a laser running unattended. Fires start in seconds.
  - Use an enclosed machine with the lid interlock working.
  - Wear goggles rated for the laser's wavelength, not general safety glasses.
  - Duct the exhaust outdoors and keep a CO2 extinguisher within reach.
  - **Never cut PVC or vinyl.** It releases chlorine gas that harms people and the machine.
- **CNC mills and routers:**
  - Protect eyes and ears. Tie back hair; no loose sleeves or gloves near the spindle.
  - Clamp the work.
  - Keep the emergency stop within reach.
  - Collect the dust. MDF and fibreglass PCB dust are harmful, so use a vacuum or wet cutting and a mask.

## 10. Fire and first aid

- **Keep near the bench:** an ABC or CO2 extinguisher, a fire blanket, and a metal tin or pot of sand for a hot or swelling battery.
- **Battery fire:**
  - Get people away; the smoke is toxic.
  - A small cell inside a LiPo bag or metal tin can be left to burn out.
  - Otherwise use plenty of water to cool it, or an extinguisher, and call the fire service if it spreads.
- **Burns:** cool running water for 20 minutes. Don't use ice or butter. Get medical help for burns larger than a coin, or on the face or hands, if they blister badly.
- **Cuts:** keep a basic first-aid kit on the shelf.

## 11. Kids and pets

- **Button cells and small magnets are emergencies if swallowed;** they burn through tissue within hours. Store them locked away.
- **Switch the iron off and put it out of reach** when children are around.
- **Store lithium batteries, solder and resin out of reach.**
- **For teaching a child:** start with a low-temperature iron, lead-free solder, safety glasses, and constant supervision.
