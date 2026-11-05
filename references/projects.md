# First-project guides

Each guide gives what the person ends up with, the parts beyond the beginner kit, the pins, the build order (each step with its check), the known problems, and the test that proves it's done. Draw the wiring diagram from these (see `diagrams.md`), and check the pin numbers against the actual board's pinout before drawing.

The pins below are for a 30- or 38-pin ESP32 DevKit. On other boards, map them by function (I2C SDA/SCL, an ADC1 analog pin) from the board's pinout, not by number.

## Contents
1. Plant sensor that messages the phone
2. Desk display (weather or calendar)
3. LED lights
4. Two-wheel robot
5. Room monitor
6. Sending phone notifications (used by several projects)

---

## 1. Plant sensor that messages the phone

**What they get:** a stake in the pot that sends a phone notification when the soil gets dry, once per dry spell, not every minute.

**Parts:** any ESP32 board; a capacitive soil-moisture sensor (v1.2 or v2.0, about ₹100 / £3–5; avoid the two-pronged "resistive" fork type, which corrodes within weeks); 3 female–female or female–male jumpers; a USB phone charger for power.

**Wiring:**
- Sensor VCC → **3V3**
- Sensor GND → **GND**
- Sensor AOUT → an **ADC1 pin**. On a DevKit that's GPIO32–39; GPIO34 is a good pick. On an Arduino Nano ESP32, use A0–A3.

  ADC2 pins stop working while Wi-Fi is on, so a sensor on ADC2 reads garbage as soon as the notification code runs.

**Build order:**
1. Flash a sketch that prints the raw reading every second. Check: numbers appear in the serial monitor.
2. **Calibrate:**
   - Note the reading with the sensor in air (dry).
   - Note it with the sensor in a glass of water, up to the line printed on the stake (wet).
   - Wet reads *lower* than dry on most of these sensors.
3. Convert the reading to 0–100% using those two numbers. Check: dry soil reads 0–30%, freshly watered soil 70–100%.
4. Add Wi-Fi and the notification (section 6). Check: a test message arrives on the phone.
5. **Add hysteresis:**
   - Send the alert when the reading drops below, say, 30%.
   - Don't send another until it has gone back above 50% (watered).
   - Read every 10–30 minutes, not every second.
6. **Stake it:**
   - Only the part below the printed line goes in the soil.
   - The electronics above the line must stay dry. Seal the edges with nail polish, conformal coating or heat-shrink, and keep the board in a small printed case.

**Known problems:**
- **The wrong timer chip.** Some cheap sensors carry an NE555 timer chip, which needs about 4.5 V and gives nonsense at 3.3 V. The correct one is a TLC555. Read the 8-pin chip's marking on arrival.
- **Slow or drifting clones.** Some clones have a layout fault that makes readings drift slowly. Buy from a shop with reviews, and test in air against water before planting.
- **Battery life.** DevKits drain a battery in days, even in deep sleep, because of their USB chip and regulator. Use a phone charger first. For battery power, move to a board with low sleep current (XIAO ESP32-C3/C6 or a FireBeetle) and deep-sleep between readings.

**Done when:** the plant goes dry, one notification arrives, and none follow until it has been watered and dried out again.

---

## 2. Desk display (weather or calendar)

**What they get:** a small screen on the desk showing the weather, the time, or their next calendar event, updated over Wi-Fi.

**Parts:** ESP32; a 0.96" SSD1306 or 1.3" SH1106 I2C OLED (4 pins), or a 2.9" e-paper module for a paper-like display; 4 jumpers.

**Wiring (OLED):**
- VCC → 3V3
- GND → GND
- SDA → GPIO21
- SCL → GPIO22

**Read the labels on the screen's pins.** Some boards order them VCC-GND, others GND-VCC. Swapping them can kill the screen.

**Build order:**
1. Run an I2C scanner sketch. Check: it finds address `0x3C` (sometimes `0x3D`).
2. Show "hello" with the U8g2 library. U8g2 supports both the SSD1306 and the SH1106; a 1.3" screen that shows garbage is usually an SH1106 driven as an SSD1306.
3. Fetch the weather from Open-Meteo, which is free and needs no API key, and show the temperature. Check: it matches a weather app.
4. Get the time from NTP, set the time zone, and redraw the screen every minute.
5. Put it in a printed stand or case with a window (see `3d-printing.md`).

**Done when:** it runs for a day on a USB charger and shows the correct weather and time.

---

## 3. LED lights

**What they get:** an addressable LED strip, where every LED can be any colour, controlled from the phone, with effects, schedules, and optionally music.

**Parts:**
- ESP32.
- A WS2812B or SK6812 strip, 5 V.
- A **5 V power supply sized for the strip**: about 60 mA per LED at full white, so 60 LEDs need 3.6 A, a 5 V 4 A supply. Use a certified one.
- A 330 Ω resistor and a 1,000 µF capacitor.
- For strips longer than about 1 m: a 74AHCT125 level shifter (3.3 V data to 5 V).

**Wiring:**
- Supply + → strip 5V, and supply − → strip GND.
- Strip GND → ESP32 GND. **The grounds must be joined.**
- ESP32 GPIO16 → 330 Ω resistor → strip DIN, at the end with the arrow pointing *away* from it.
- The 1,000 µF capacitor across the supply at the strip, with the stripe (−) to GND.
- **Never power the strip from the ESP32's 5V pin or USB** beyond about 10 LEDs. The board's traces and the computer's USB port aren't made for amps.

**Build order:**
1. Easiest route: flash **WLED** from its web installer. It's free firmware with a phone app and no coding. Coders can use FastLED instead.
2. Start with the brightness limit set in WLED (about 1–2 A) until the supply is confirmed. Check: the strip lights a test colour and the supply stays cool.
3. On long strips, feed 5 V and GND into the strip again every 1–2 m. Without it, the far end turns brown or orange at white.

**Done when:** the phone controls the colour, and a full-white test for 5 minutes leaves the wires and the supply only warm.

---

## 4. Two-wheel robot

**What they get:** a small car driven from the phone over Wi-Fi, then made to avoid obstacles.

**Parts:**
- ESP32.
- A TB6612FNG motor driver board. It's small and efficient; avoid the old L298N, which wastes power and gets hot.
- 2 yellow TT gear motors with wheels, and a caster wheel.
- A battery: 2S LiPo (7.4 V) with a balance charger, or a 6×AA pack.
- A 5 V buck converter, which turns the battery voltage into 5 V for the ESP32.
- A VL53L0X or HC-SR04 distance sensor.
- A chassis kit or a printed chassis.

**Wiring:**
- Battery → TB6612 VM, and battery → buck input. Buck 5 V → ESP32 5V/VIN.
- **Join all the grounds:** battery, buck, driver and ESP32.
- TB6612 VCC → ESP32 3V3, and STBY → 3V3.
- PWMA/AIN1/AIN2 and PWMB/BIN1/BIN2 → six free GPIOs. Avoid the boot pins (0, 2, 5, 12 and 15) and the input-only pins (34–39). GPIO 25, 26, 27, 14, 32 and 33 work.
- Solder a 0.1 µF capacitor across each motor's terminals, to cut electrical noise.

**Build order:**
1. Test each motor alone, forward and back, with the wheels off the table. Check: both spin the right way. If one doesn't, swap that motor's two wires.
2. Drive from a simple web page served by the ESP32, with buttons that set the motor speeds.
3. Add the distance sensor, and stop when something is under 15 cm away.

**Known problem:** the ESP32 resetting whenever the motors start means the battery voltage is dipping. Add a 470–1,000 µF capacitor at the buck input, or use a stronger battery.

**Done when:** it drives around a room from the phone and stops before hitting a wall.

---

## 5. Room monitor

**What they get:** a page on the home network, or a Home Assistant dashboard, showing temperature, humidity and air quality, with history.

**Parts:**
- ESP32.
- A BME280 board (temperature, humidity, pressure).
- Optional: an SCD40 or SCD41 for real CO2 readings. Skip "MQ-135" gas sensors; they don't measure CO2 and need a 5 V heater.

**Wiring:** both sensors use I2C and share the same four wires.
- VCC → 3V3
- GND → GND
- SDA → GPIO21
- SCL → GPIO22

**Build order:**
1. Run an I2C scanner. Check: the BME280 shows at `0x76` or `0x77`, and the SCD4x at `0x62`.
2. Read the chip ID. **Many "BME280" boards are really a BMP280, which has no humidity sensor.** A BME280 returns ID `0x60`; a BMP280 returns `0x58`.
3. Serve a small web page from the ESP32, or flash **ESPHome** and add the device to Home Assistant for graphs.
4. Keep the sensor away from the ESP32 itself, on short wires or at the other end of the case, because the board's heat raises the temperature reading.

**Done when:** the readings match a reference thermometer to within about 1 °C, and history builds up overnight.

---

## 6. Sending phone notifications

| Way | Setup | Notes |
|---|---|---|
| **ntfy** (default) | Install the ntfy app and subscribe to a topic. The ESP32 sends an HTTP POST to `https://ntfy.sh/<topic>` with the message as the body. | Free, with no account. **Anyone who guesses the topic name can read and send to it**, so use a long random topic (e.g. `plant-7f3k9q2x`), or self-host. |
| Telegram bot | Create a bot with @BotFather, get its token, and find your chat ID. The ESP32 calls `https://api.telegram.org/bot<token>/sendMessage`. | Private. The token is a secret, so it goes in `secrets.h`, never in chat or in a shared repo. |
| Home Assistant | Use ESPHome on the device and the Home Assistant app's notifications. | Best when they already run Home Assistant. |

Whatever the route, send on a change of state ("now dry"), not on every reading. Rate-limit to a few messages a day.
