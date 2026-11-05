# electronics-lab

A Claude Code skill that sets up a home electronics lab and gets you from zero to a working hardware project.

Tell Claude what you want to build and where you live. It will:

- **Make a parts cart** for your level (beginner, expert or full kit wanker), using shops in your country. It checks live prices and stock, and catches the cables, connectors and adapters that first carts usually miss.
- **Teach the safety basics** before you power anything: batteries, the soldering iron, mains, and how to avoid frying parts.
- **Draw wiring and soldering diagrams** that look like your actual board and breadboard. Each diagram has a check to do before you plug in, and Claude compares a photo of your wiring with it.
- **Get 3D-printed parts made** without owning a printer. It finds a proven file, or writes one in OpenSCAD, checks it, and walks you through ordering from a print service.
- **Flash and debug boards** like ESP32 and Arduino from your computer.
- **Keep a `LAB.md`** of what you own, what's on order, and where each project stands, so later sessions pick up where you left off.

It grew out of real sessions where a complete beginner set up a bench and got their first boards working with Claude. The mistakes made along the way are in [`references/pitfalls.md`](references/pitfalls.md).

## Install

For all your projects:

```bash
git clone https://github.com/syllogismos/electronics-lab-skill ~/.claude/skills/electronics-lab
```

For one project only, clone it into that project's `.claude/skills/electronics-lab` folder instead.

## Use

Ask Claude Code something like:

- "I'm in Pune, never soldered anything, want to build something that tells me when my plants need water. Budget ₹8,000. What do I buy?"
- "Here's a photo of my wiring, is it right before I plug it in?"
- "I need a case for my ESP32 DevKit but I don't have a 3D printer."

Or type `/electronics-lab`.

## What's inside

| File | What it covers |
|---|---|
| `SKILL.md` | How Claude runs the whole process, step by step |
| `references/kits.md` | Tools and parts for each level, with what to look for and typical prices |
| `references/shops.md` | Shops, local markets and 3D-print services by country |
| `references/safety.md` | Electricity, batteries, soldering, fumes, protecting parts, printers, lasers and CNC |
| `references/projects.md` | Step-by-step guides for five first projects: plant sensor, desk display, LED lights, robot, room monitor |
| `references/diagrams.md` | How Claude draws wiring and soldering diagrams |
| `references/3d-printing.md` | Finding, checking, generating and ordering printed parts |
| `references/pitfalls.md` | Real mistakes from real builds |
| `scripts/check_print.py` | Checks an STL, OBJ or 3MF file and draws a preview (Python standard library only) |
| `assets/LAB-template.md` | Starting point for your lab file |

The checker also works on its own:

```bash
python3 scripts/check_print.py base.stl lid.stl --material PETG --preview case.png --section z=4 --probe z=5,y=40
```

`--section` lists the holes and outlines at a height. `--probe` measures solid and empty stretches along a line, which finds wall thicknesses and openings cut into an edge.

## Notes

- Prices, stock and delivery rules were checked in late 2026. Claude rechecks them live before building a cart.
- This skill keeps you on the low-voltage side: USB, batteries and bench supplies. It doesn't guide anyone through mains wiring.
