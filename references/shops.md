# Where to buy, by country

These are starting points, not endorsements. Shops change stock, prices and delivery rules weekly, so check each one live before it goes in a cart. Delivery thresholds marked "seen" were observed on the date given.

## How to choose a shop

- **One main shop per cart.** Reaching the free-delivery threshold at one shop usually beats saving ₹20 on an item somewhere else. Add a second shop only for items the main one doesn't sell.
- **Big specialist shops** have the best datasheets, genuine parts and reliable stock (DigiKey, Mouser, element14/Farnell, RS, LCSC). Their delivery is fast in most countries, but their prices for hobby modules are higher.
- **Hobby shops** sell ready-made modules (sensor boards, charger boards, dev boards) cheaply, with tutorials. They're the right place for most beginner carts.
- **Amazon** is fast and handles returns easily. Listing quality varies, so check the seller and the rating. Treat anything under 4 stars, or with few reviews, as a risk, and say so in the cart.
- **AliExpress, Taobao, Temu** are cheapest but slow (2–5 weeks). Some categories won't ship to some countries, so check before planning around them. Fake parts are common here (18650 capacities, sensors, chips).
- **Local electronics markets** exist mainly in India and much of Asia. In most UK, EU and US cities, online shops are the default; the walk-in exceptions are chain stores such as Micro Center (US) and Jaycar or Altronics (Australia). Where markets exist, they're best for tools, wire, batteries and "I need it today". Phone first: Maps categories are often wrong. A shop listed under "electronics" turned out to sell washing machines; another was a training centre; a third sold TV remotes. Check reviews and photos, then give the person the shop's name, phone number, closing time, and the exact words to ask for. Show a photo of the exact part at the counter, because shops hand over substitutes.

## India (230 V, 50 Hz; plug types C/D/M)

**Online hobby shops** (the main options for most carts):

| Shop | Good for | Notes |
|---|---|---|
| Robu.in (Pune) | The widest hobby range: boards, sensors, batteries, motors, tools; also a **3D-print service** | Free delivery above ₹999 (seen Oct 2026). Pages are built in the browser and return 403 to curl, so use a browser. Listings sometimes carry wrong specs, such as weights. |
| Robocraze (Bengaluru) | Dev boards, kits, small adapters (e.g. 7Semi SOT-23 adapter boards) | Free delivery above ₹999 (seen Oct 2026). Returns HTTP 429 to direct fetches, so use a browser. |
| Quartz Components (Jaipur) | Small parts, adapters, flux, tweezers, tape | Shopify, so `/products/<handle>.json` works. Free delivery above ₹500 (seen Oct 2026). |
| Hubtronics (Bengaluru) | Seeed and other dev boards, often in stock when others aren't | |
| Evelta (Mumbai) | Genuine modules, camera modules, harder-to-find parts | |
| ElectronicsComp, Probots, ThinkRobotics, CompoIndia | Extra stock for boards that are sold out elsewhere | ThinkRobotics has quoted 2–4 week lead times. |
| element14 India, Mouser India, DigiKey India | Genuine chips, connectors and datasheet-grade parts | Check at checkout whether duties are included. |
| Amazon.in | Tools, cables, power banks, fast delivery | Check the seller and rating. |
| JLCPCB / PCBWay / LCSC | Custom PCBs, assembly, chips | Ships to India; customs may add duty. |

**Local markets** (phone first; verify by reviews):
- Bengaluru: SP Road
- Mumbai: Lamington Road
- Delhi: Lajpat Rai Market and Bhagirath Palace (Chandni Chowk)
- Chennai: Ritchie Street
- Kolkata: Chandni Chowk market
- Pune: Budhwar Peth
- Hyderabad: Koti

**3D-print services:**
- **Robu 3D printing.** Upload an STL and get an instant price. Choose the quality (0.2/0.15/0.1 mm layers), the material (PLA, PETG, ABS, TPU and others), the infill and the colour. As seen in Oct 2026:
  - A print must be its **own order**, separate from normal parts.
  - The print subtotal must be at least **₹80**, so order 2–3 copies of small parts.
  - A small, flat PETG part at 50% infill cost ₹36 each.
- **JLC3DP** (JLCPCB's print service) does FDM, resin, nylon and metal, with good quality and international shipping.
- **Karkhana.io** handles CNC, sheet metal and 3D printing. It suits bigger or B2B jobs.
- **Local print shops and college or maker labs.** Search "3D printing service <city>". Check their reviews and ask for photos of past prints.

## United States (120 V, 60 Hz)

- **Hobby shops:**
  - Adafruit and SparkFun, both with excellent guides.
  - Pololu (motors, drivers, regulators).
  - Micro Center (walk-in stores), Jameco and Amazon.
- **Specialist shops:** DigiKey and Mouser. Free shipping thresholds are around $50–100, and their delivery is fast.
- **3D printing:**
  - Craftcloud compares prices across many print shops.
  - JLC3DP, Xometry and Protolabs.
  - Many public libraries and makerspaces print for a small fee.
  - SendCutSend does laser-cut and sheet-metal parts.

## United Kingdom (230 V, 50 Hz; type G)

Buy online; the UK has no walk-in component markets like India's. Delivery thresholds weren't recorded, so check them at the basket.

| Shop | Good for | Notes |
|---|---|---|
| The Pi Hut | Boards, sensors, breakout boards, kits | Doesn't stock generic ESP32 DevKits; pick the Arduino Nano ESP32 or a XIAO. Expensive for tools (its only multimeter was £55 when checked). Fetch notes below. |
| Pimoroni | Boards, sensors, LED products | Shopify, like The Pi Hut. |
| CPC Farnell | **Budget tools and meters** (own brands Duratool and Tenma), components | The cheap place for the iron, meter and hand tools. Category pages can time out, so search by product name. |
| Rapid Electronics | Components, tools, education kits | |
| Amazon UK | Fast delivery of tools, cables and power banks | Check the plug: some irons ship with an EU plug and an adapter. |
| Mouser, DigiKey, RS | Genuine chips and connectors | |

- **Solder:** leaded solder is legal for hobby use, but most UK shops stock lead-free. Set the iron to 350–380 °C for lead-free.
- **3D printing:** Craftcloud, JLC3DP, 3DPRINTUK, and local makerspaces.

## European Union (230 V, 50 Hz)

- **Hobby and specialist shops:**
  - Reichelt, Conrad and Berrybase (Germany).
  - TME and Botland (Poland).
  - Kiwi Electronics (Netherlands).
  - Mouser and DigiKey.
- **3D printing:** Craftcloud, JLC3DP, and local FabLabs (many cities have one).
- **Solder:** lead-free solder is the norm in the EU. Leaded solder is still sold for hobby use, so check local rules.

## Canada (120 V)

- **Shops:** DigiKey (ships fast from the US border, with duties handled), Mouser, RobotShop, PiShop.ca, BC Robotics, Elmwood Electronics, and Canada Computers (stores).
- **3D printing:** Craftcloud, JLC3DP, and makerspaces.

## Australia (230 V; type I)

- **Hobby shops:** Core Electronics, Little Bird Electronics, and Jaycar and Altronics (both with stores).
- **Specialist shops:** element14 and DigiKey.
- **3D printing:** Craftcloud, JLC3DP, and makerspaces.

## Japan (100 V)

- **Shops:** Akizuki Denshi, Switch Science, Marutsu and Sengoku Densho.
- **Walk-in market:** Akihabara.

## Southeast Asia

- **Malaysia:** Cytron.
- **Singapore:** Sim Lim Tower for walk-ins.
- **Shopee and Lazada:** these marketplaces have many sellers. Treat them like AliExpress: cheap, but check the seller and expect fakes.

## Anywhere else

1. **Search for local shops:** "<country> electronics components online shop" and "<city> electronics market".
2. **Check each shop** by its reviews, how long it has been in business, and whether it stocks the specific boards.
3. **Fall back to big shops that ship almost anywhere:** DigiKey, Mouser, LCSC and Seeed Studio, or AliExpress for slow, cheap parts. Warn about customs duties.
4. **For 3D printing:** use Craftcloud or JLC3DP, or find the nearest makerspace or FabLab (fablabs.io lists them).

## Fetching shop pages

Shops block or rate-limit automated requests in different ways. Use the cheapest route that works, and fall back to the browser.

- **Shopify stores** (Quartz Components, The Pi Hut, Pimoroni and many others):
  - `/search/suggest.json?q=<words>&resources[type]=product&resources[limit]=10` returns the price, stock flag, image and link for up to 10 products in one call. It's the most efficient way to price a cart.
  - `/products/<handle>.json` gives full details, but The Pi Hut returned 429 (retry after 60 s) after about 3 quick calls.
  - In curl, escape the brackets as `%5B%5D`, or use `-g`. Unescaped brackets make curl fail silently.
- **Robu:** pages are built in the browser and curl gets 403. Use the browser.
- **Robocraze:** returns 429 to direct fetches. Use the browser.
- **CPC Farnell:** category pages can time out after 60 s. Search for the exact product instead.
- **DigiKey, Mouser and Amazon** often block scripts. Use their search in the browser, or search results that show prices.
- **Budget:** when lookups are limited, follow the priority order in SKILL.md Step 3 (board, sensors, iron, meter, then the rest), and mark the rest "price not checked".

## Buying traps (from real carts)

- **Same name, different product.** "ESP32 CH340C" is sold both as a DevKit and as the ESP32-CAM-MB programmer board. Confirm by photo, pin count and USB type.
- **Relabelled parts.** An "OV2640" ESP32-CAM shipped with a GC2145 sensor (ribbon marked "M21-45"). That sensor has no hardware JPEG, so it is stuck at low resolution. Camera boards also change sensors between batches. Check the ribbon marking on arrival.
- **Pack sizes.** If the listing says "pack of 2" and you set the quantity to 2, you get 4.
- **Wrong connector, wrong cable.** Micro-USB and USB-C boards look alike in thumbnails. "JST" covers several sizes that don't fit each other.
- **1S versus 2S batteries.** A 7.4 V pack fries a board made for 3.7 V. Ask for "3.7 V single cell".
- **Sold out everywhere.** Niche boards go out of stock in waves. Check 4–6 shops, including the small ones. Amazon may cost more but deliver first.
- **Silent cart failures.** Compare the cart, then the order confirmation, against the list.
