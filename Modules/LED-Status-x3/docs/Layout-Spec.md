# Layout Spec — LED-Status-x3

DRAFT. The geometry of the module reference board, written before the board
exists. Every number is a decision, and each one carries its reason.

Board: 14 x 11 mm, 2 layers, 1.6 mm, PCBWay. Written 2026-09-24.

Nothing here is measured yet. Re-derive every figure from the files after
placement.

---

## 1. The block

6 parts. 7 nets. From the exported block netlist.

| Ref | Value | Footprint | Driven by |
|---|---|---|---|
| D1 | Green 570 nm | `LED_SMD:LED_0603_1608Metric` | `/LED_RF_TX` through R4 |
| D2 | Amber 605 nm | `LED_SMD:LED_0603_1608Metric` | `/LED_LEARN` through R5 |
| D3 | Red 625 nm | `LED_SMD:LED_0603_1608Metric` | `/LED_FAULT` through R6 |
| R4 | 220 | `Resistor_SMD:R_0603_1608Metric` | — |
| R5 | 330R | `Resistor_SMD:R_0603_1608Metric` | — |
| R6 | 330R | `Resistor_SMD:R_0603_1608Metric` | — |

Each chain is GPIO → R pin 1 → R pin 2 → LED anode, pin 2 → LED cathode, pin 1
→ `GND`. The GPIO sources the current.

At 3.3 V the green LED runs about 5 mA through 220 Ω, and the amber and red
about 4 mA through 330 Ω. 0.20 mm track carries that many times over.

## 2. Why 2 layers

No controlled impedance, no plane current, three slow signals. A 2-layer board
is the cheapest module that still carries the breakout convention: each via
takes its stub on the far layer.

## 3. The reference placement is not worth copying

On `Plum-RFBridge` the six parts sit in a 6 x 5 mm cluster at mixed angles:

| Ref | X | Y | Rot |
|---|---|---|---|
| R4 | 142.407 | 107.872 | 270 |
| D1 | 142.806 | 110.146 | 180 |
| D2 | 144.195 | 111.878 | 0 |
| R5 | 145.371 | 109.604 | 270 |
| R6 | 147.733 | 108.817 | 0 |
| D3 | 148.427 | 111.099 | 90 |

The LEDs sit at three angles and no two share a row. That packing served a
crowded host. This module keeps the **order**, green, amber, red, left to
right, and puts each chain in its own straight column.

## 4. Outline

| Item | X | Y |
|---|---|---|
| Board outline | 100.0 → 114.0 | 100.0 → 111.0 |
| LED row | — | 102.5 |
| Resistor row | — | 105.6 |
| Breakout row | 101.0 → 110.5 | 108.5 |

The LEDs sit on the top edge side so a host can put them near a panel.

## 5. Placement table

Three columns at 2.6 mm pitch. Each column is LED on top, resistor below.

| Ref | X | Y | Rot |
|---|---|---|---|
| D1 | 106.3 | 102.5 | 270 |
| D2 | 108.9 | 102.5 | 270 |
| D3 | 111.5 | 102.5 | 270 |
| R4 | 106.3 | 105.6 | 90 |
| R5 | 108.9 | 105.6 | 90 |
| R6 | 111.5 | 105.6 | 90 |

**Why these rotations.** At 270 an LED's cathode, pad 1, lands on top at
y 101.71 and its anode on the bottom at y 103.29. At 90 a resistor's pad 2
lands on top at y 104.78 and pad 1 on the bottom at y 106.43. Anode meets
pad 2 across a 1.5 mm gap. Pad 1 faces the breakout row.

**Why 2.6 mm pitch.** It puts each resistor pad 1 within 1.0 mm in x of its
breakout via, with the middle column dead straight. 2.6 mm also suits a light
pipe.

**Why y 105.6.** A 0603 courtyard is 2.96 mm long. At 105.6 the LED and
resistor courtyards clear by 0.14 mm. At 105.5 they clear by 0.04 mm.

Nearest edge: D3's courtyard ends at x 112.98, 1.0 mm from the right edge.

## 6. Routing

| Net | Path | Width |
|---|---|---|
| `/LED_RF_TX` | R4.1 (106.3, 106.43) → 45° east → via 107.3 | 0.20 |
| `/LED_LEARN` | R5.1 (108.9, 106.43) → straight down → via 108.9 | 0.20 |
| `/LED_FAULT` | R6.1 (111.5, 106.43) → 45° west → via 110.5 | 0.20 |
| `Net-(Dn-A)` | R pad 2 straight up to LED anode, 1.5 mm | 0.20 |
| `GND` | LED cathodes into the F.Cu pour | pour |

All on F.Cu. Nothing crosses.

## 7. Zones

| Zone | Layer | Net | Rectangle |
|---|---|---|---|
| Top pour | F.Cu | `GND` | 100.5, 100.5 → 113.5, 110.5 |
| Bottom pour | B.Cu | `GND` | 100.5, 100.5 → 113.5, 110.5 |

Stitch the two pours with at least four GND vias outside the courtyards.

## 8. The breakout row

Via 0.6 mm pad on 0.3 mm drill. Row at **y = 108.5**, 2.5 mm above the bottom
edge, as on the PoE module. Each signal via carries a 1.0 mm stub on B.Cu,
ending at y 109.5.

| x | Net | Direction | Arrives on | Stub layer |
|---|---|---|---|---|
| 101.0 | `GND` | stitch | pour | both |
| 104.0 | `GND` | stitch | pour | both |
| 107.3 | `/LED_RF_TX` | in | F.Cu | B.Cu |
| 108.9 | `/LED_LEARN` | in | F.Cu | B.Cu |
| 110.5 | `/LED_FAULT` | in | F.Cu | B.Cu |

GND pitch 3.0 mm. Signal pitch 1.6 mm. The 3.3 mm gap between the last GND
and the first signal matches the PoE module (x 140.0 to 143.3).

The B.Cu pour must clear each signal stub by the netclass clearance. It does
so by itself. Check the three `track_dangling` warnings are the three stubs
and nothing else.

## 9. PCBWay edge rule

Every copper feature on this board sits within 3.5 mm of an edge. **PCBWay
needs break-away rails** (`docs/Block-Modules-Handoff.md` §4.5). On a 14 x 11 mm
board, panelize instead. Rails on the left and right edges of the panel.

## 10. Schematic note

`LED_RF_TX`, `LED_LEARN` and `LED_FAULT` are **local labels**, not hierarchical
labels. A design block pasted into a host sheet joins them by name, so that
works. The same block placed as a hierarchical sheet exposes no pins. The
Ethernet block uses hierarchical labels for its interface. Decide one rule for
the family.
