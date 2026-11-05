# Kits by level

Each level includes everything in the level below it. Prices are typical street prices in late 2026, in India (₹) and the US ($), for planning only. For a rough UK or EU figure, take about 80% of the $ price in £, or about 90% in €; hobby-shop prices in those countries run close to US prices. Check live prices before you show a cart.

For each item, the cart should say what it looks like and does, the spec to match, and the quantity. Buy tools rated for the local mains voltage and plug type: a 110 V soldering station won't work in a 230 V country.

## Contents
- Beginner: tools, prototyping, power, first boards, consumables
- Expert: bench gear, measurement, rework, making boards and parts
- Full kit wanker: machines, lab-grade instruments, production, the room
- Project add-on packs

---

## Beginner (about ₹5–9k · $150–300)

The goal is to solder well, measure safely, prototype without soldering, and power a project from a battery. Skip anything not listed. Cheap "37 sensors in 1" kits are mostly unused; buy sensors per project.

**First-project kit** (buy this when the budget is tight; it's about half the full beginner list):
- Soldering iron with stand, solder, flux, wick, tip cleaner
- Multimeter
- Flush cutters, wire strippers
- Safety glasses
- 2 breadboards and jumper wires
- A USB data cable that fits both the board and the computer (a USB-C-only laptop needs USB-C to USB-C)
- The board
- The project's parts from `projects.md`

Everything else below is a **lab extra**. Add extras when the budget allows, or when a project needs one (calipers for printed parts, the power section for battery projects).

### Soldering

| Item | What it is | Spec to match | ₹ | $ |
|---|---|---|---|---|
| Soldering iron | Pen-shaped heater that melts solder | Adjustable temperature, 60 W or more, with a stand. Get a **fine conical tip** for small pads and a chisel tip for thick wires and battery plugs. The tip shape matters more than the wattage for small work. A Pinecil V2 is a good option if they have a 65 W USB-C charger. If the shop doesn't stock either, its own-brand temperature-controlled 50–60 W station is fine (e.g. Duratool at CPC in the UK). | 600–1,500 | 25–40 |
| Solder wire | Thin metal wire that melts to join parts | 0.8 mm with a rosin core. 63/37 or 60/40 tin-lead is the easiest to learn on, and it's legal for hobby use in India, the UK, the EU and the US. Many UK and EU shops mostly stock lead-free (SAC305), which is fine but needs a hotter iron (350–380 °C) and looks duller. Pick lead-free if kids are around. | 200–450 | 8–15 |
| Flux | Paste or pen that helps solder flow and stick | "No-clean" flux paste or a flux pen | 150–300 | 8 |
| Tip cleaner | Ball of brass wool in a cup | Brass, not a wet sponge (it lasts longer and the tip stays hotter) | 150–300 | 8 |
| Desoldering wick and pump | Copper braid and a spring-loaded sucker for removing solder | 2 mm wick | 150–350 | 10 |
| Helping hands with magnifier | Clips on bendable arms, with a magnifying glass and light, to hold the work | Heavy base, 2–4 arms, an LED magnifier | 500–1,500 | 15–35 |
| Silicone mat | Heat-proof mat that protects the desk and holds screws | About 40 × 30 cm | 400–800 | 15 |
| Heat-shrink tube | Plastic sleeves that shrink over joints when heated | Assortment, 1.5–6 mm. A lighter works at first; a heat gun later. | 150–300 | 8 |

### Measuring and hand tools

| Item | What it is | Spec to match | ₹ | $ |
|---|---|---|---|---|
| Multimeter | Measures voltage, resistance and current, and **beeps** when two points are connected | Auto-ranging, with a continuity beep and a fused 10 A input. A ₹250 manual one works, but auto-ranging makes beginner checks faster. | 800–2,000 | 25–45 |
| Flush cutters | Small side cutters that trim leads flat | | 150–400 | 8–12 |
| Wire strippers | Remove insulation without nicking the wire | Self-adjusting type, or one with gauge holes for 20–30 AWG | 300–700 | 10–20 |
| Needle-nose pliers | | Small, 12–15 cm | 150–300 | 8 |
| Tweezers | For tiny parts | ESD-safe, one straight and one bent | 100–300 | 8 |
| Precision screwdrivers | Small Phillips, flat and hex bits | Magnetic bit set | 300–800 | 15 |
| Digital calipers | Measure parts to 0.01 mm. Essential for 3D-printed parts that must fit. | 150 mm | 600–1,200 | 15–25 |
| Safety glasses | | Clear, wraparound | 100–300 | 8 |
| Small fan | Pulls solder smoke away from your face | Desk or USB fan. A carbon-filter extractor comes at the expert level. | 300–1,000 | 10–20 |

### Prototyping without soldering

| Item | What it is | Spec to match | ₹ | $ |
|---|---|---|---|---|
| Breadboards | Plastic boards with spring holes for pushing in wires and parts | 2 full-size (830 holes) or 4 half-size (400). An ESP32 DevKit is so wide that it covers almost every free hole on either side of a single breadboard, full-size or half-size. Put two breadboards side by side, one row of the DevKit's pins on each. | 200–500 | 10–15 |
| Jumper wires | Wires with pin or socket ends | 40 each of male–male, male–female and female–female | 150–300 | 8–12 |
| Solid-core wire kit | Pre-cut, pre-bent wires that lie flat on a breadboard | 140-piece box, or 22 AWG solid wire on spools | 150–400 | 8–15 |
| Breadboard power module | Small board that plugs onto the breadboard's power rails and gives 3.3 V or 5 V from USB | **USB-C input**, 3.3 V/5 V selectable. Avoid the older barrel-jack/USB-A type (MB102, HW-131) unless they have a 7–12 V adapter and a USB-A to USB-A cable. | 100–250 | 5–8 |
| USB data cables | Connect the board to the computer | Match each board's socket (USB-C or micro-USB). It must carry **data**; many cheap cables only charge. | 100–300 | 5–10 |
| Component assortment | A box of the basic parts | LEDs, a resistor kit (10 Ω–1 MΩ), ceramic and electrolytic capacitors, push buttons, slide switches, potentiometers, diodes (1N4148 and 1N5819), small transistors (BC547 or 2N2222) and a logic-level MOSFET (AO3400 or IRLZ44N) | 500–1,000 | 20–30 |
| Header pins | Strips of pins for soldering onto boards so they plug into breadboards | Male and female, 2.54 mm, 1 × 40 | 50–150 | 5 |
| Perfboard | Board with a grid of holes for permanent circuits | 5 × 7 cm, double-sided, pack of 5 | 100–200 | 6 |

### Power

| Item | What it is | Spec to match | ₹ | $ |
|---|---|---|---|---|
| Small USB power bank | The simplest way to run any USB board without a cable to the computer | One that **doesn't switch off at low current** (some do below about 100 mA, which randomly resets small boards) | 500–1,000 | 15–25 |
| Lithium battery | 1-cell (3.7 V) LiPo pouch or 18650 cell | 1S only. 500–1,000 mAh for small projects. Buy from a known brand; fake 18650s claim inflated capacity. | 150–700 | 6–15 |
| Charger board | Thumb-sized board that charges one cell from USB | TP4056 **with protection** (it has separate B+/B− and OUT+/OUT− pads), USB-C | 20–60 | 1–2 |
| Battery connectors | Matching plug and socket pairs | Measure the pitch or match the board's socket. JST-PH 2.0 is common; check the polarity with a meter, because cheap batteries are sometimes wired the opposite way round. | 50–150 | 5 |
| Slide switches | Small on/off switches | SS12D00 or similar, pack of 10 | 50–100 | 4 |
| 18650 holder | Clip that holds one cell, with wire leads | Only if using 18650s | 30–80 | 2 |

### First boards (pick one or two)

The default is an ESP32 board: Wi-Fi and Bluetooth, cheap, with a huge community. Which ESP32 to buy depends on where they shop. Generic DevKits are everywhere in India, on AliExpress and on Amazon, but UK, EU and Australian hobby shops often don't stock them. Check what flashes how (SKILL.md Step 8) before picking.

| Board | Why | ₹ | $ |
|---|---|---|---|
| ESP32 DevKit, USB-C | The default where it's sold (India, Amazon, AliExpress). | 350–600 | 8–15 |
| Arduino Nano ESP32 (with headers) | The default at UK and EU hobby shops such as The Pi Hut and Pimoroni. Breadboard-friendly, with good documentation. Uploads through the Arduino core (DFU). | — | 20–22 |
| Seeed XIAO ESP32-C3 / C6 | Tiny, cheap and low-power; good for battery projects. Sold almost everywhere Seeed is. | 500–900 | 5–7 |
| Raspberry Pi Pico 2 W | Simple, well documented, Wi-Fi | 700–900 | 7–8 |
| Arduino Uno (or clone) | Only if a course or book uses it | 400–2,000 | 10–28 |

### Consumables and storage

Isopropyl alcohol (99%) and an old toothbrush for cleaning off flux. Kapton tape (heat-proof). Double-sided foam tape. Electrical tape. A small hot glue gun. Compartment boxes, zip bags and labels.

---

## Expert (about ₹1–2.5 lakh · $2–5k)

The goal is to see what a circuit is doing (scope, logic analyzer, current measurement), rework tiny surface-mount parts, and make your own circuit boards and printed parts.

| Item | What it does | Typical pick | ₹ | $ |
|---|---|---|---|---|
| Soldering station | Fast heat-up, swappable cartridge tips | T12 or JBC-C245-compatible station, or Hakko FX-888DX | 4–10k | 80–150 |
| Hot-air rework station | Blows hot air to solder or remove tiny chips | 858D-class or Quick 861DW | 3–15k | 60–300 |
| Fume extractor | Fan with an activated-carbon filter | Benchtop, with a replaceable filter | 2–6k | 40–120 |
| Bench power supply | Adjustable voltage with a **current limit**, which saves parts from mistakes | 0–30 V, 0–5 A, programmable (Riden RD6006, Korad KA3005P) | 5–12k | 70–150 |
| USB-C power meter | Shows the voltage and current going into any USB device | With PD readout | 500–1,500 | 15–30 |
| Power profiler | Measures a battery device's current over time, for battery-life work | Nordic PPK2 | 9–12k | 100 |
| Oscilloscope | Shows voltage over time: noise, signals, power dips | 4 channels, 70–100 MHz+ (Rigol DHO804, Siglent SDS1104X-HD) | 35–50k | 400–550 |
| Logic analyzer | Decodes digital signals (I2C, SPI, UART) | 8-channel 24 MHz clone with PulseView, or a Saleae Logic 8 | 600–45k | 10–500 |
| Microscope | Inspect joints and read tiny markings | 7–45× stereo, or a digital one with an HDMI screen | 5–25k | 100–400 |
| ESD mat and wrist strap | Stops static from killing chips | Grounded mat, 60 × 50 cm | 1.5–4k | 30–60 |
| PCB holder | Holds boards steady while soldering | Stickvise-style or PanaVise | 1–4k | 25–70 |
| Crimp tool and terminal kits | Make your own JST and Dupont cables | IWISS SN-28B or Engineer PA-09, plus JST-PH, JST-XH and Dupont kits | 2–6k | 30–60 |
| LiPo balance charger and safety | Charges multi-cell packs correctly and stores them safely | ISDT or ToolkitRC charger, fire-resistant LiPo bag, cell checker | 4–8k | 60–100 |
| Reflow hot plate and solder paste | Solders whole surface-mount boards at once | Small hot plate, paste in a syringe, stencils from the PCB maker | 2–6k | 40–90 |
| Silicone wire | Flexible wire for anything that moves | 22, 26 and 30 AWG, red and black | 500–1,500 | 15–30 |
| 3D printer | Print cases and mounts in hours instead of days | Bambu Lab A1 mini or A1, or Prusa Core One. Buy from an authorized local seller for warranty and the right plug. | 25–80k | 250–1,200 |
| Thermal camera | Finds hot parts and shorts instantly | Phone add-on (InfiRay P2 Pro, Topdon TC001) | 20–30k | 200–300 |
| Board drawer | More boards to try | ESP32-S3, ESP32-C3/C6, RP2350, nRF52840, an STM32 Nucleo, Raspberry Pi 5 | 5–15k | 100–200 |
| Organizer and label maker | Find parts in seconds | Drawer cabinet and a label printer | 3–8k | 50–100 |

Software: KiCad (free) for designing boards. Order them from JLCPCB or PCBWay; five boards cost a few dollars plus shipping. Add PCB assembly when the parts are tiny.

---

## Full kit wanker (about ₹15–50 lakh · $20–60k+)

The goal is to make almost anything in-house: machine aluminium and circuit boards, cut and engrave, print in any material, assemble boards, and measure like a lab. Buy big machines from authorized distributors (warranty, mains voltage, service). Check import duty before importing.

| Area | Item | Typical pick | $ (approx.) |
|---|---|---|---|
| Machining | Desktop CNC mill with automatic tool changer, for aluminium, PCB milling and wood | Makera Carvera (or Carvera Air); Shapeoko 5 Pro for larger work | 2.5–6k |
| Cutting | Enclosed CO2 laser for acrylic and plywood, plus a fiber laser for marking metal | xTool P2S, xTool F1 Ultra | 2–6k |
| Printing | Multi-material FDM, plus resin with wash-and-cure | Bambu Lab H2D or X1C with AMS; Formlabs Form 4 or Elegoo Saturn | 1.5–8k |
| Board assembly | Desktop pick-and-place, reflow oven, stencil printer | LumenPnP; controlled reflow oven | 2–6k |
| Soldering | Premium station with nano handpieces | JBC CD-2BQE, Hakko FM-203, Metcal | 0.8–2k |
| Inspection | Trinocular stereo microscope with camera and ring light | AmScope | 0.8–2k |
| Scope | Mixed-signal scope with protocol decode, 350 MHz+ | Rigol MSO5000, Siglent SDS2000X HD, Keysight | 2–8k |
| Meters | 6.5-digit bench meter, LCR meter, handheld | Siglent SDM3065X or Keysight 34465A; Fluke 87V | 1–3k |
| Power | Programmable triple-output supply, DC electronic load | Rigol DP832 or Siglent SPD3303X; Siglent SDL1020X | 1–2k |
| Signals and RF | Function generator, spectrum analyzer, VNA | Siglent SDG2042X; tinySA Ultra; NanoVNA-H4 (or a Siglent SSA) | 0.5–3k |
| Power analysis | Precision current profiling | Joulescope | 1k |
| Thermal | Handheld thermal camera | FLIR E8 Pro or InfiRay | 1–3k |
| Mains work (trained people only) | Isolation transformer, variac, differential probe | | 0.5–1.5k |
| Workshop | Drill press, bench vise, rotary tool, heat-set insert press, ultrasonic cleaner | | 1–2k |
| Storage | Parts wall with drawers, inventory software | Raaco or Akro-Mils cabinets, InvenTree or PartsBox | 0.5–2k |
| Room | ESD workbench with shelf and switched power strips, RCD/GFCI-protected outlets, 5000 K high-CRI lighting, ducted fume and laser exhaust, air-quality monitor | | 2–5k |
| Fire safety | LiPo storage box, CO2 and ABC extinguishers, fire blanket, smoke detector over the printers | Bat-Safe box | 0.3–0.6k |

Even at this level, outsource what a service does better and cheaper: PCB fabrication and assembly (JLCPCB, PCBWay), CNC metal parts (JLCCNC, Xometry), sheet metal and laser cutting (SendCutSend in the US), and nylon (SLS/MJF) prints.

---

## Project add-on packs

Add these to the level kit for a specific build. Check the exact versions live.

- **Desk display:** ESP32, a 0.96" or 1.3" I2C OLED (or a 2.9" e-paper screen), a USB-C cable and wall adapter, and a printed case with a window.
- **LED lights:** ESP32, a WS2812B or SK6812 LED strip, a 5 V supply sized for the strip (about 60 mA per LED at full white), a 330 Ω resistor on the data line, a 1,000 µF capacitor across the supply, and a 3.3 V to 5 V level shifter for long strips.
- **Robot car:** ESP32, a TB6612 motor driver, 2 gear motors with wheels, a caster, a 2S battery and a 5 V buck converter, an ultrasonic or ToF distance sensor, and a chassis (printed or bought).
- **Plant sensor:** any ESP32 board, a capacitive soil sensor (check that its timer chip says TLC555, not NE555), a certified USB phone charger, and a small printed case for the top of the stake.
- **Room monitor:** any ESP32 board, a BME280 (temperature, humidity, pressure; check it isn't a BMP280), optionally an SCD40/SCD41 CO2 sensor, a certified 5 V USB wall adapter, and a printed case with vents.

The full build steps for each are in `projects.md`.
