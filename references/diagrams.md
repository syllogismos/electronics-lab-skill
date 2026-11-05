# Drawing wiring and soldering diagrams

A beginner can't read a schematic, but they can copy a picture that looks like the parts in front of them. The diagram's job is to make the next physical step impossible to get wrong, and to give a check that proves it was done right.

Publish diagrams with the Artifact tool when available. Load the `artifact-design` and `artifact-diagramming` skills first. Otherwise, write a self-contained HTML file with inline SVG and open it. Make one artifact per project and update it in place (same file, same link) as the build moves on. Tell the person what changed.

## Before drawing: get the facts from the real parts

- **Photo of the exact board.** It should be taken straight down, both sides if labels are on the back. Boards with the same name differ: the ESP32 DevKit has 30-pin and 38-pin versions with different pin orders; the HW-131 and USB-C breadboard power modules have different jumpers and inputs.
- **The pin order comes from the silkscreen in the photo or the maker's pinout image.** Never infer it from the layout or from memory. When a pin order or polarity comes from documentation, quote the source in the diagram, e.g. "Seeed: the − pad is the one nearest the USB-C port".
- **What the person actually has.** Draw their breadboard size, their wire colours if they told you, and their power module, not the one you recommended.

## The wiring diagram

Draw what they will see, the same way round as their photo.

1. **Boards, to scale and the right way round.**
   - Draw the outline, the USB port and its side, the buttons, and the pins.
   - Label each pin with the text **printed on the board** ("VIN", "GND", "IO0", "U0T"), in the same order.
   - Mark which buttons face down into the breadboard. They can't be pressed once the board is plugged in, so give the workaround: replug the USB instead of pressing RST.
2. **The breadboard, as it is.**
   - Show the row numbers and column letters, the centre gap, and the power rails with their + and − markings.
   - Mark where the rails are split. Many full-size boards break the rails in the middle.
   - Shade the groups of holes that are joined inside, so it's obvious that a–e on a row are connected and f–j are a separate group.
   - If the dev board covers a whole half-size breadboard, draw two breadboards side by side, and say that they clip together and that their rails are separate until a wire joins them.
3. **Wires.**
   - Each wire is a numbered badge on a coloured path: red for +5 V or +3.3 V, black for GND, and distinct colours for signals.
   - The ends land on exact holes ("row 12, column c").
   - Avoid crossing wires over labels.
4. **Connection table** under the drawing:

   | # | From | To | Colour | Why |
   |---|---|---|---|---|
   | 1 | DevKit **5V** (row 12c) | + rail | red | powers the camera |

5. **Timing notes,** for wires that only belong in certain moments. For example: "Wire 6 (IO0 → GND): put it in **before** plugging in USB, to enter flash mode. Take it out **after** the upload finishes, then replug USB to run the program."
6. **Steps in build order.** One step per wire or part, each with its check.
7. **Check before power** (USB unplugged, meter on the beep setting):
   - Must beep: each wire's two ends, e.g. "DevKit 5V pin to camera 5V pin".
   - Must **not** beep: + to GND on every supply. List each pair.
   - Then, with power on, the expected readings: e.g. "+ rail to − rail: 4.75–5.25 V", "3V3 pin: 3.2–3.4 V".
8. **Photo check.** Ask for a photo of the finished wiring before power, and compare it wire by wire with the table. Reply "all 6 wires match", or name the exact wire and hole that is off. In one real session, the board sat one row lower than drawn, so the 5 V wire was going into GND. The photo check caught it.

## Soldering maps

For anything soldered (battery leads, headers, switches, wires to pads):

- **A close-up of the pads,** much larger than real size.
  - Label each pad, with + and − where they apply.
  - If the board doesn't label the pads, say how to tell them apart and cite the source ("the − pad is nearest the USB-C port, per Seeed's documentation"). Then add a multimeter confirmation step.
- **The order of steps.** For example:
  1. Tin both pads.
  2. Cut and strip the black wire only.
  3. Solder it.
  4. Insulate it.
  5. Then do the red wire.
- **Where heat-shrink goes:**
  - Wire-to-wire joints: slide the heat-shrink on **before** soldering.
  - Joints on board pads: use Kapton tape or hot glue instead.
- **The check after soldering:**
  - No beep between + and −.
  - The battery voltage appears at the board's pads.
  - The joints look shiny and cone-shaped, not balled up or grey.
- **Strain relief.** Tape or glue the wires near the joint so movement doesn't break them off the pad.

## Layout and mounting drawings

When parts must fit in a frame or case, draw a to-scale top view of the parts inside the printed part. One example: the board, battery and switch inside a case. Flag tight spots in millimetres (e.g. "the USB plug clears the wall by about 1 mm, so file the opening if the cable won't seat").

## Quick explanations in chat

For a one-off concept (how breadboard holes connect, the power chain from battery to board), a small ASCII sketch in the chat is faster than an artifact:

```
USB-C ──► charger board (TP4056) ──OUT+/OUT-──► switch ──► board BAT+/BAT-
                    │
                 battery (3.7 V, 1 cell)
```

## Drawing hygiene

- Inline SVG, with a grid where 2.54 mm (one breadboard hole) is a fixed number of pixels, so everything lines up.
- Text never overlaps images or wires. A real parts page had titles hidden under photos.
- Readable on a phone (the person will have it open next to the bench), and in both light and dark themes.
- Add a small legend: wire colours, the badge numbers, and "unplug before changing any wire".
- No decoration. Every mark should help someone place a wire or check a joint.
