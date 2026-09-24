# Layout Spec — LDO-RF-3V3-AP2112K

The geometry of the module reference board. Every number is a decision, and each
one carries its reason. The board is laid out. Section 10 records the changes
from the draft and section 11 the state DRC measured.

Board: 10 x 12 mm, 4 layers, 1.6 mm. Written 2026-09-24.

Sources:

| Tag | Document |
|---|---|
| DS | Diodes AP2112 datasheet, **DS39724 Rev. 2-2**, June 2017. `_resources/Research/AP2112/AP2112.pdf` |
| REF | `_resources/Examples/Plum-RFBridge/Plum-RFBridge.kicad_pcb`, the routed parent board |
| BLK | `PlumBlocks.kicad_blocks/LDO-RF-3V3-AP2112K.kicad_block/LDO-RF-3V3-AP2112K.kicad_sch`, netlist exported 2026-09-24 |

---

## 0. Schematic findings

No defect. Three parts: U9 AP2112K-3.3TRG1, C105 and C106, 1 µF X7R 0603.

| Item | BLK | DS |
|---|---|---|
| Input capacitor | 1 µF X7R | 1 µF ceramic, X5R or X7R (Note 4) |
| Output capacitor | 1 µF X7R | same |
| EN, pin 3 | tied to V5_SYS | high 1.5 to 6.0 V, "H – normal work" |
| NC, pin 4 | unconnected | "No Connection" |
| VIN range | V5_SYS, 5 V | 2.5 to 6.0 V (Recommended Operating Conditions) |

## 1. Dissipation

| Item | Value | Source |
|---|---|---|
| Load | 30 mA, CC1101 transmitting | the brief; not checked against the CC1101 datasheet |
| Quiescent | 55 µA typ, 80 µA max | DS AP2112-3.3 table |
| Drop at 5.00 V in | 1.70 V | 5.00 − 3.30 |
| Loss at 5.00 V | **51 mW** | 1.70 V x 30 mA, plus 0.3 mW quiescent |
| Loss at 5.25 V | 59 mW | USB upper tolerance |
| RθJA | 184 °C/W | DS thermal table, SOT25, no heatsink |
| Rise | **9 to 11 °C** | 51 to 59 mW x 184 |
| Junction at 85 °C ambient | 96 °C | against a 160 °C shutdown |

The block note says "60 mW". That matches the 5.25 V case.

**No thermal copper is needed.** 59 mW in a SOT-23-5 is small. The GND pad
takes an ordinary pour connection.

## 2. What the datasheet says about layout

**Nothing.** DS39724 has no layout section. It gives a suggested land pattern
and Note 4 on the capacitor dielectric. This spec applies the general LDO rules
instead, and says so at each point:

1. Put C105 and C106 within 1 mm of their pins. An LDO loop is only stable with
   its output capacitor close.
2. Return both capacitors to the GND pin by the shortest path.
3. Keep switching copper away. The block exists to keep buck noise off the
   433 MHz front end.

## 3. Placement

### 3.1 The parent board

From REF. U9 sits at (137.0, 124.0, 0) on F.Cu.

| Ref | REF X | REF Y | Rot | dX from U9 | dY from U9 |
|---|---|---|---|---|---|
| U9 | 137.000 | 124.000 | 0 | 0 | 0 |
| C105 | 136.030 | 126.497 | 0 | −0.970 | +2.497 |
| C106 | 140.587 | 123.345 | 0 | +3.587 | −0.655 |

C105 sits 2.5 mm below the package. C106 sits 2.5 mm east of VOUT. Both work,
but both are longer than they need to be. REF also puts U9 next to the buck
output capacitors C103 and C104, at 4 mm. The module has no such neighbour.

### 3.2 The module

As laid out. Read from the saved board.

| Ref | X | Y | Rot | Side | Reason |
|---|---|---|---|---|---|
| U9 | 105.000 | 104.500 | 0 | F | — |
| C105 | 101.300 | 104.000 | 270 | F | pad 1 (V5_SYS) at 101.30, 103.225; pad 2 (GND) at 101.30, 104.775. Moved 0.6 mm west of the draft; see §10 |
| C106 | 108.100 | 104.000 | 270 | F | pad 1 (+3V3_RF) at 108.10, 103.225; pad 2 (GND) at 108.10, 104.775 |

U9 pins at this position:

| Pin | Net | At |
|---|---|---|
| 1 VIN | `/V5_SYS` | 103.862, 103.550 |
| 2 GND | `GND` | 103.862, 104.500 |
| 3 EN | `/V5_SYS` | 103.862, 105.450 |
| 4 NC | — | 106.138, 105.450 |
| 5 VOUT | `/+3V3_RF` | 106.138, 103.550 |

A 0603 pad pitch of 1.55 mm cannot match the SOT-23-5 pitch of 0.95 mm, so no
capacitor pad is exactly level with a U9 pin. Each capacitor pad 1 sits 0.325 mm
above its pin and joins it with a 45° jog.

Gap from the capacitor pad to the U9 pad end: C105 1.33 mm, C106 0.83 mm.
Courtyard check: no overlaps.

## 4. Copper on the parent board

| Net | Widths used |
|---|---|
| +3V3_RF | 0.25 mm on F.Cu, 7 segments, 12.6 mm |
| V5_SYS | shared with the buck, 0.5 mm |

## 5. Track widths

| Net | Class | Width | Reason |
|---|---|---|---|
| `/V5_SYS` | Power_1 | 0.3048 | 30 mA needs far less; the width lowers the inductance to C105 |
| `/+3V3_RF` | Power_1 | 0.3048 | REF used 0.25; this matches the class |
| `GND` | pour | — | — |

The brief gives Default 0.2. REF and the PoE modules use Default 0.1524. Pick
one in `Board-Setup.md` and write it once.

## 6. Zone plan

| Zone | Layer | Net | Region | Priority |
|---|---|---|---|---|
| Ground plane | In1.Cu | `GND` | whole board | 0 |
| Input plane | In2.Cu | `/V5_SYS` | whole board | 0 |
| Top ground | F.Cu | `GND` | whole board | 0 |
| Bottom ground | B.Cu | `GND` | whole board | 0 |

**No power polygon on F.Cu.** 30 mA does not need one. Two short traces carry
VIN and VOUT.

**EN reaches V5_SYS through In2.** EN sits below GND on the same side as VIN.
An F.Cu trace from EN to VIN must cross the GND path from U9.2 to C105.2. A via
at (103.9, 106.8) drops EN to the In2 plane instead.

## 7. Vias

| Location | Count | Net |
|---|---|---|
| (103.862, 106.8), below EN | 1 | `/V5_SYS` |
| (101.3, 102.1), above C105.1 | 1 | `/V5_SYS` |
| (101.3, 105.9), below C105.2 | 1 | GND |
| (108.1, 105.9), below C106.2 | 1 | GND |

All vias 0.6 mm pad on 0.3 mm drill. U9.2 has no via of its own; see §10.

One via carries 30 mA with a margin of 25 times. No thermal via is needed; see
§1.

## 8. The breakout row

Row at **y = 109.5**. Each via carries a 1.0 mm stub on the layer opposite its
arrival, ending at y 110.5. Via 0.6 mm pad on 0.3 mm drill.

| x | Net | Direction | Arrives on | Stub layer |
|---|---|---|---|---|
| 101.2 | `GND` | stitch | pour | both |
| 102.8 | `/V5_SYS` | in | In2.Cu | F.Cu |
| 104.4 | `GND` | stitch | pour | both |
| 107.4 | `GND` | stitch | pour | both |
| 109.0 | `/+3V3_RF` | out | F.Cu | B.Cu |

GND pitch is 3.0 mm between 104.4 and 107.4. Signal pitch to each neighbour is
1.6 mm. One via per power net carries this load.

`/+3V3_RF` leaves C106.1 on F.Cu, runs east of C106 at x 109.0, and drops to
the row. It never passes over the input side. GND vias carry no stub.

## 9. Checks before you believe a number

1. Refill the zones. `kicad-cli pcb drc --refill-zones` refills in memory only.
2. Confirm the net names. The block uses a hierarchical label for `+3V3_RF`, so
   the module net is `/+3V3_RF`.
3. State a non-zero canary: append a 3 mm clearance rule, re-run DRC, confirm
   the count explodes, restore, diff.
4. Count segments on every interface net to its breakout via.
5. Render the board and look at it.

## 10. Changes from the draft

| Item | Draft | Laid out | Why |
|---|---|---|---|
| C105 X | 101.900 | 101.300 | At 101.9 the gap from C105.2 to U9.2 was 0.83 mm. Both GND pads need a 0.5 mm thermal gap, so the F.Cu pour could not fill between them. U9.2 got one spoke against a minimum of 2, and DRC gave `starved_thermal`. At 101.3 the pour fills between them and DRC is clean. The cost is 0.6 mm more loop, against the §2 aim of 1 mm |
| U9.2 to C105.2 | draft implied a direct path | F.Cu pour only | A direct 0.3048 mm track was tried first. KiCad does not count a track as a spoke, and the track took the west spoke position. It was deleted |
| GND via beside U9.2 | 1 | 0 | No 0.6 mm via fits between the SOT-23-5 pad rows or between C105 and U9 with 0.2 mm clearance. U9.2 reaches GND through the F.Cu pour and the C105.2 via |
| EN via | 103.9, 106.8 | 103.862, 106.8 | On the pin centre line, so the track is straight |
| `/+3V3_RF` drop | x 109.3 | x 109.0 | Straight down to the breakout via at x 109.0. Track edge 0.85 mm from the board edge |
| Breakout stubs | "both" on GND | signal vias only | The procedure puts a stub on signal vias only, so `track_dangling` counts the signal stubs |

## 11. Closing state

Measured 2026-09-24 with `kicad-cli pcb drc --severity-all --schematic-parity
--refill-zones`.

| Item | Count |
|---|---|
| Errors | 0 |
| Unconnected | 0 |
| Schematic parity | 0 |
| `track_dangling` | 2, the two signal stubs |
| Silkscreen warnings | 5, left for the GUI silk pass: C106 reference clipped by the edge, C105 reference over U9 pads (3) and over the U9 outline |
| Canary (`check_import.py`) | 7 to 61, PASS |

Copper: 12 segments, 9 vias.

| Net | F.Cu segments | B.Cu segments | Vias |
|---|---|---|---|
| `/V5_SYS` | 5 (3 C105 to U9.1, 1 EN, 1 stub) | 0 | 3 |
| `/+3V3_RF` | 4 (U9.5 to the breakout via) | 1 (stub) | 1 |
| `GND` | 2 (capacitor to via) | 0 | 5 |

Breakout row, y 109.5. F.Fab labels at y 108.3, size 0.7, rotation 90.

| x | Net | Arrives on | Stub | Stub end |
|---|---|---|---|---|
| 101.2 | `GND` | pours, In1 | — | — |
| 102.8 | `/V5_SYS` | In2.Cu plane | F.Cu, 1.0 mm | 102.8, 110.5 |
| 104.4 | `GND` | pours, In1 | — | — |
| 107.4 | `GND` | pours, In1 | — | — |
| 109.0 | `/+3V3_RF` | F.Cu track, 4 segments from U9.5 | B.Cu, 1.0 mm | 109.0, 110.5 |

Open:

1. Silkscreen pass in the GUI.
2. The F.Fab value fields of U9 and C105 overlap the breakout labels, and C105's
   value field sits off the board edge. F.Fab only.
