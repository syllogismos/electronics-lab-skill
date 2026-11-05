# Pitfalls from real builds

Every item here happened in real sessions where a complete beginner set up a bench and got their first boards working with Claude. Each lesson is written generally, with what happened in brackets.

## How Claude should behave

- **Explain every part name on first use,** by how it looks and what it does. (An 18650 holder and a U.FL connector both had to be explained after the fact.)
- **Don't let a suggestion sound like a second purchase** when it's an option or a replacement. (A "power module" suggestion read as "buy another power supply" when the person already had one.)
- **Don't assume they lack something.** Check `LAB.md` or ask. (A multimeter and flux paste were put in a cart although the person already owned both.)
- **Say exactly when.** Write "before plugging in USB" and "after the upload finishes", not "for flashing". (The person had to ask when the flash-mode wire goes in and when it comes out.)
- **Justify parts that look odd,** in one line, before they ask. (A large adapter board for a tiny chip prompted "why do we need this?")
- **Verify; don't extrapolate or invent.** If you already searched for something, use the result instead of asking again. (A shop's distance was made up, and a delivery estimate was argued from past events instead of checked.)
- **Check before asking.** Use the browser, the docs or the photo first.
- **Answer only what was asked.** Raise safety issues; skip unrequested advice about deadlines or scope.
- **Verify your own artifacts against the photo** when asked, and never present an inferred pin order as fact.
- **For a list to copy, use plain lines** without checkboxes or dashes.
- **Say when soldering isn't needed.** USB-C powers and flashes most boards, and a USB power bank makes them wireless with no soldering. (Claude first said a battery had to be soldered on.)

## Buying

- **Same name, different product.** (Shops use "ESP32 CH340C" for both the ESP32-CAM-MB programmer board and a DevKit.) Confirm by photo, pin count and USB type.
- **Relabelled sensors.** (An "OV2640" ESP32-CAM had a GC2145, ribbon marked "M21-45". It failed with "JPEG format is not supported on this sensor / Camera init failed with error 0x106". The workaround gave raw images at only 320×240.) Read the ribbon marking on arrival. If the camera matters, buy from a shop that names the sensor and has good reviews.
- **Board revisions change between batches.** (Popular camera boards have changed sensors from batch to batch, and a newer revision was wrongly called "the latest".) Check the listing and the arrival, and never claim "latest" without checking.
- **Local shops substitute.** (A USB-C breadboard power module was asked for, and an HW-131/MB102 was handed over. It needs a 6.5 V+ barrel jack or a USB-A to USB-A cable, which wasn't available nearby. A power bank board with no breadboard pins was handed over as a "power module".) Show the shop a photo of the exact part, and photograph what you're given before leaving.
- **Incomplete carts.** (A first project cart missed adapter boards for tiny surface-mount chips, battery plugs, a micro-USB cable for a micro-USB board, wire, headers, flux, tweezers, foam tape and a strap.) Run the four-question completeness pass in SKILL.md.
- **Pack sizes.** (A PCB sold as a 2-pack went in as quantity 2.)
- **Wrong listing data.** (A battery was listed at more than twice its real weight. Another listing showed the wrong brand and no plug type.) For anything weight- or size-critical, check the datasheet or weigh it on arrival.
- **Items vanish between cart and order.** (An item that was in the checked cart was missing from the placed order.) Compare the confirmation against the list.
- **Restricted categories.** Some marketplaces won't ship some kinds of kits to some countries. Check before planning around them.
- **Low-rated listings.** Flag anything under 4 stars, or with few reviews, or pick a better seller.
- **Niche boards sell out in waves.** (A popular dev board was out of stock at the two biggest hobby shops. It came from a smaller shop with one unit left; Amazon cost more but was fastest.) Check 4–6 shops.
- **Robu pages are built in the browser** (403 to curl). **Robocraze rate-limits** direct fetches (429). The browser extension can disconnect in the middle of filling a cart, so recheck the cart afterwards.

## Power

- **"3.7 V battery" isn't a 5 V supply.** A bare cell browns out a 5 V pin and over-volts a 3.3 V pin. Use a board with a battery input, a charger/boost board, or a USB power bank. ("18650 holder with 5 V USB output" was read as "buy a 3.7 V battery".)
- **Power bank boards switch off at light loads,** which randomly resets a small board. Their USB-A output has no breadboard pins, and their BAT± pads carry raw battery voltage, not 5 V. (About ten turns went into getting one board's 5 V onto a breadboard.)
- **The LCD on a power bank board runs a display test at connection.** (It showed "118%"; the real charge was 19%.)
- **Unlabelled battery pads.** Some small boards have battery pads with no + or − marking. Quote the maker's documentation for which pad is which, then confirm with a meter. (Claude once invented "BAT+/BAT−" labels and a battery socket that didn't exist.)
- **Simplest path first:** run on USB, then on a USB power bank, then on a soldered battery with a switch.
- **ESP32-CAM brownouts** under Wi-Fi load: it needs a solid 5 V supply that can deliver at least 500 mA.
- **Heat.** Wi-Fi boards under heavy use can pass 65–70 °C. Fit any heatsink supplied, vent the case, and print it in PETG or better.

## Wiring and breadboards

- **The ESP32 DevKit covers a whole half-size breadboard.** Draw how the holes connect inside, and show two boards clipped side by side with separate rails. (The person didn't know breadboards clip together, or which holes are joined.)
- **Off by one row.** (The DevKit sat one row lower than drawn, so the "5 V" wire went into GND.) Use row numbers in the diagram, and do a photo check before power.
- **Buttons facing down into the breadboard can't be pressed.** (The ESP32-CAM's RST button.) Replug the USB instead.
- **Ribbon not seated.** (The first photo showed the camera ribbon socket empty.) Open the latch, insert the ribbon fully, then close the latch.
- **Using a DevKit as the USB programmer for an ESP32-CAM:**
  - EN to GND holds the DevKit's own chip in reset.
  - 5V to 5V and GND to GND.
  - **TX0 → U0T and RX0 → U0R, straight, not crossed.** The DevKit's USB chip talks directly to the camera board.
  - IO0 on the camera board to GND for flash mode.

  Normal UART between two running boards is crossed (TX → RX).
- **Multimeter probe jacks.** (The probes were in the wrong jacks.) Black goes in COM, red in VΩ.
- **Some boards have only a few free pins.** (On the ESP32-CAM, the camera and SD card use most pins, so adding an I2S microphone is tight.) Check the free pins before choosing a board for a multi-sensor project.

## Soldering

- **Heat-shrink only fits wire-to-wire joints,** and goes on the wire before soldering. On board pads, use Kapton tape or glue. (Claude first said to heat-shrink joints on the pads, then corrected itself.)
- **Battery leads:** cut and solder one at a time, keep them from touching, and keep the iron off the cell.
- **The tip matters more than the wattage** for small pads: use a fine conical tip at 300–350 °C, 0.8 mm rosin-core solder and flux. Thick wires and big battery plugs (XT60) need 60 W or more and a chisel tip.
- **Headers are optional.** Many small boards ship without them. Solder them only if the board will go on a breadboard.
- **The U.FL antenna** presses straight down until it clicks. Without it, Wi-Fi range is poor.

## Flashing and software

- **Charge-only cables** are the first suspect when no serial port appears.
- **Drivers:** recent macOS has the CH340 driver built in. Windows may need the CH340 or CP210x driver.
- **Port names:**
  - macOS: `/dev/cu.usbserial-*` (CH340 or CP210x), `/dev/cu.usbmodem*` (native USB on the ESP32-S3 or C3).
  - Linux: `/dev/ttyUSB0` or `/dev/ttyACM0` (add the user to the `dialout` group).
  - Windows: `COMx`.
- **Apple-chip Macs:** `arduino-cli compile` for ESP32 failed with "ctags: bad CPU type" until Rosetta was installed (`softwareupdate --install-rosetta --agree-to-license`).
- **Run read-only checks first:** `esptool chip-id` and `esptool flash-id` confirm the port and chip before anything is written.
- **Missed boot messages:** start the serial listener first, then press reset or replug.
- **ESP32-S3 boards with native USB:**
  - Enable "USB CDC on boot" to see serial output.
  - If an upload fails, hold BOOT, tap RESET, release BOOT, and upload again.
  - Camera projects need PSRAM enabled and a partition scheme with enough app space.
- **Wi-Fi:** most ESP32s join only 2.4 GHz. `.local` names often don't resolve on Android, so use the IP address or a DHCP reservation in the router.
- **Secrets:** the person typed the Wi-Fi password into the sketch file opened in their editor. Claude checked it was filled in without printing it.
- **What worked:** Claude installed the tools in the background while the person wired, then compiled, flashed and read the serial output. The person only plugged and replugged.

## 3D printing

- **Exact-size file with no builds versus a proven close design:** pick the proven one, and explain why. (The exact size requested had no files with posted builds; a slightly larger design had over a hundred.)
- **Print only the part you need.** (A multi-part design only needed its base.)
- **Comments reveal weak spots.** (A design known to break in small impacts was printed in PETG, with spare copies.)
- **Robu print orders** are separate from normal parts, have an ₹80 minimum, and give an instant price after the STL upload. Browser upload from ~/Downloads was blocked by permissions until the file was copied elsewhere.
- **Check fit-critical dimensions** against the real parts, using `check_print.py --section`. (A clip that measured slightly smaller than its part meant a press fit. Printed holes come out small, so keep a round file ready.)
