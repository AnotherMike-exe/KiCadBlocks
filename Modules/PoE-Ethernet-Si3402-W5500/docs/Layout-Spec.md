# Layout Spec — PoE-Ethernet-Si3402-W5500

The geometry of the module reference board. Every number is a decision, and each
one carries its reason.

Board: 56 x 84 mm, 4 layers, 1.6 mm, PCBWay. Written 2026-09-23.

Read `Board-Setup.md` first. It holds the stackup, the net classes and the
patterns. This file holds the geometry.

---

## 1. Outline and regions

All coordinates are KiCad board millimetres.

| Item | X | Y |
|---|---|---|
| Board outline | 100.0 → 156.0 | 50.0 → 134.0 |
| Jack band | 100.0 → 156.0 | 50.0 → 68.0 |
| Primary region | 100.5 → 127.0 | 68.0 → 133.5 |
| Barrier band | 127.0 → 129.5 | 68.0 → 133.5 |
| Secondary region | 129.5 → 155.5 | 50.5 → 133.5 |
| Breakout row | 130.0 → 155.0 | 131.5 |

The barrier is vertical. The primary domain sits left of it. The secondary
domain sits right of it. The band is 2.5 mm wide and holds no copper of either
domain.

### 1.1 Why the barrier is vertical, and why it stops at the jack

J1 is an Abracon ARJM11C7 integrated-magnetics jack. Its line side pins and its
chip side pins interleave in one pad field:

```
left to right at rotation 180:
  1 VC2-   2 VC1-   3 RD-   4 RCT   5 RD+   6 VC2+   7 VC1+   8 TD-   9 TCT   10 TD+
  P        P        S       S       S       P        P        S       S       S
```

No straight line separates P from S. A partition therefore needs a crossing,
and the isolation in that pad field is Abracon's 1500 Vrms construction, not
layout. So the barrier band starts at y = 68.0, below the jack courtyard, and
the `.kicad_dru` J1 exception governs the band above it.

A horizontal barrier does not work at all. The MDI pairs would have to cross
it to reach the W5500.

## 2. The domain split

82 parts. The split comes from the exported netlist, not from the drawing.

**Primary, 28 parts.** U1, FB1, FB2, FB3, FB4, C1, C2, C3, C4, C5, C6, C7, C8,
C9, C10, C11, C12, C13, C14, C15, D1, D2, R1, R2, R3, R4, TP1, TP2.

**Bridges, 4 parts.** T1, U2, C16, C17. Each one straddles the band.

**Secondary, 50 parts.** J1 plus the Ethernet set and the PoE output set.

18 nets are primary. They are listed in `Board-Setup.md` section 3.

## 3. Placement table

Rotation follows KiCad. A pad at local (x, y) lands at global
`(fx + x cos t + y sin t, fy - x sin t + y cos t)`, where `t` is the footprint
angle. **A pad angle stored in a board file is absolute**, so do not add the
footprint angle to it a second time.

This table is generated from the board. Regenerate it after any move.

| Ref | X | Y | Rot |
|---|---|---|---|
| R23 | 138.5 | 53.0 | 0 |
| R24 | 142.0 | 53.0 | 0 |
| C39 | 138.0 | 58.5 | 0 |
| J1 | 125.0 | 64.8 | 180 |
| C32 | 134.0 | 67.0 | 0 |
| R21 | 137.5 | 68.0 | 0 |
| C34 | 141.0 | 68.0 | 0 |
| R20 | 151.5 | 68.5 | 90 |
| R22 | 154.0 | 68.5 | 90 |
| FB4 | 119.285 | 70.6 | 270 |
| FB3 | 125.5 | 70.6 | 270 |
| R16 | 143.75 | 72.0 | 270 |
| R15 | 145.3 | 72.0 | 270 |
| R13 | 146.85 | 72.0 | 90 |
| R14 | 148.4 | 72.0 | 90 |
| R18 | 151.5 | 72.0 | 90 |
| C36 | 154.0 | 72.0 | 270 |
| C31 | 134.0 | 73.5 | 0 |
| FB2 | 121.0 | 74.0 | 270 |
| FB1 | 125.5 | 74.0 | 270 |
| R19 | 136.5 | 76.0 | 0 |
| C23 | 135.5 | 78.0 | 0 |
| C1 | 116.0 | 78.3 | 90 |
| C4 | 119.0 | 78.3 | 90 |
| C7 | 122.0 | 78.3 | 90 |
| C10 | 125.0 | 78.3 | 90 |
| U4 | 143.5 | 80.0 | 270 |
| C30 | 150.5 | 80.0 | 0 |
| C24 | 135.5 | 80.5 | 0 |
| C2 | 116.0 | 81.7 | 270 |
| C5 | 119.0 | 81.7 | 270 |
| C8 | 122.0 | 81.7 | 270 |
| C11 | 125.0 | 81.7 | 270 |
| C26 | 135.5 | 83.0 | 0 |
| FB5 | 153.0 | 83.0 | 0 |
| C33 | 132.0 | 85.5 | 0 |
| C37 | 135.5 | 85.5 | 0 |
| C35 | 153.0 | 86.0 | 0 |
| C27 | 136.2 | 88.0 | 0 |
| C22 | 139.5 | 88.0 | 0 |
| Y1 | 143.5 | 88.0 | 0 |
| C25 | 147.5 | 88.0 | 0 |
| C38 | 153.0 | 89.0 | 0 |
| C17 | 123.25 | 90.0 | 0 |
| C28 | 136.2 | 91.0 | 0 |
| C29 | 140.0 | 91.5 | 0 |
| R10 | 143.5 | 91.5 | 0 |
| R12 | 147.5 | 91.5 | 0 |
| R17 | 139.0 | 94.0 | 270 |
| R11 | 150.0 | 95.0 | 0 |
| C13 | 110.0 | 96.0 | 0 |
| R4 | 115.0 | 96.0 | 0 |
| C15 | 122.0 | 96.0 | 0 |
| TP1 | 113.0 | 98.0 | 0 |
| C19 | 140.0 | 98.5 | 0 |
| R9 | 143.5 | 98.5 | 0 |
| C9 | 109.5 | 101.0 | 90 |
| C6 | 116.5 | 101.0 | 90 |
| C14 | 113.0 | 102.0 | 90 |
| R3 | 106.0 | 103.0 | 0 |
| D3 | 142.5 | 103.0 | 180 |
| C20 | 150.0 | 103.0 | 0 |
| T1 | 128.25 | 105.0 | 0 |
| R1 | 108.0 | 105.9 | 0 |
| TP3 | 150.0 | 107.0 | 0 |
| U1 | 114.5 | 107.5 | 270 |
| R2 | 108.0 | 108.5 | 0 |
| L1 | 142.5 | 110.0 | 0 |
| TP2 | 117.8 | 113.0 | 0 |
| D2 | 121.5 | 114.0 | 180 |
| R5 | 136.0 | 114.0 | 0 |
| D1 | 114.5 | 117.0 | 0 |
| R6 | 136.0 | 117.0 | 0 |
| U2 | 128.25 | 119.0 | 180 |
| R7 | 136.0 | 120.0 | 0 |
| C12 | 120.0 | 121.0 | 0 |
| C21 | 148.0 | 121.0 | 0 |
| R8 | 136.0 | 123.0 | 0 |
| C3 | 108.0 | 124.0 | 0 |
| C16 | 123.25 | 127.0 | 0 |
| U3 | 137.0 | 127.0 | 0 |
| C18 | 141.5 | 129.5 | 0 |

**U1 sits at rotation 270 for one reason.** SWO, pin 18, then faces the
barrier. U1.18 lands at (116.85, 107.5) and T1.2 lands at (119.74, 107.5). The
switch node is a straight horizontal trace 2.89 mm long. No other rotation of
U1 gives that, because T1's primary pad row is fixed at `barrier_x - 8.51`.

**U4 sits at rotation 270 so the MDI pins face the jack.** Pins 1 to 12 land on
the top edge, and the SPI pins 32 to 36 land on the bottom edge above the
breakout row.

**C16 and C17 use `C_Disc_D10.5mm_W5.0mm_P10.00mm`, whose origin sits on pad 1,
not at the body centre.** Their placement X is therefore 128.25 - 5.0 = 123.25.

Every courtyard pair is checked by `Modules/analysis/check_courtyards.py`. No
overlap. The smallest gap is 0.09 mm, between R13 and R14.

## 4. The jack fanout

The jack pads sit at y 62.26, the top row, and y 64.8, the bottom row. The jack
body covers y 50.04 to 66.05, so every escape leaves through that band.

| Net | Pad | Escape |
|---|---|---|
| POE_VC2N | J1.1 (119.285, 62.26) | F.Cu, straight down to FB4 |
| POE_VC1N | J1.2 (120.555, 64.80) | F.Cu, down then left to FB2 |
| MDI_RDN | J1.3 (121.825, 62.26) | F.Cu, **up** to y 59.3, then right |
| RCT | J1.4 (123.095, 64.80) | F.Cu, up between pads 3 and 5, then right |
| MDI_RDP | J1.5 (124.365, 62.26) | F.Cu, **up** to y 59.0, then right |
| POE_VC2P | J1.6 (125.635, 64.80) | F.Cu, straight down to FB3 |
| POE_VC1P | J1.7 (126.905, 62.26) | F.Cu, down then 45 deg left to FB1 |
| TXN_MDI | J1.8 (128.175, 64.80) | F.Cu, down then right |
| TCT | J1.9 (129.445, 62.26) | F.Cu, right at y 63.0 |
| TXP_MDI | J1.10 (130.715, 64.80) | F.Cu, down then right |

**Every tap stays on F.Cu.** `Plum-RFBridge` dropped pins 6 and 7 to B.Cu to
clear the RD pair. This module does not need that, because the RD pair, RCT and
TCT all escape **upward** into the jack body band and turn right at y 60.6 to
61.4. Below the pad rows the primary side is then empty, so pins 6 and 7 run
straight down on F.Cu.

The upward escape works because the gap between two top-row pads is 1.04 mm of
copper. A 0.15 mm trace centred in it clears 0.44 mm each side.

The RD pair descends to the right of J1.10 at x 132.0 and 132.6. It cannot
descend between the pads: J1.10's barrel spans x 129.965 to 131.465 and J1.8's
spans 127.425 to 128.925, and the one clear gap between them is taken by
POE_VC1P. That descent is why the MDI termination band sits at x 134 and 137.5
rather than 131 and 134.5.

CGND runs from J1.SH2 (117.125, 58.96) to J1.SH1 (132.875, 58.96) at y 58.96,
then right to C39. It passes above every tap escape.

## 5. The heat spreader

**This is the reason the module exists as its own board.**

| Item | Value |
|---|---|
| Layer | B.Cu, an OUTER layer |
| Net | `/VNEG` |
| Zone priority | 2 |
| Rectangle | 100.5, 68.0 → 127.0, 133.0 |
| Area | 26.5 x 65.0 = **1722 mm²**, 2.67 in² |
| Required | 1290 mm², 2 in² |
| Margin | 432 mm², 33 percent |

The plane must stay on an outer layer. AN956 measures 44 °C/W for 2 in² on an
outer layer and 54 °C/W for 1 in² on an inner layer. Inner copper is not a
substitute.

| Thermal item | Value |
|---|---|
| Class 1 power budget | 3.84 W |
| Worst case dissipation in U1 | 0.85 W |
| Rise at 44 °C/W | 37 °C |
| Junction at 85 °C ambient | 122 °C |
| Thermal shutdown | 160 °C |
| Margin | 38 °C |

The spreader starts at y 68.0, below the jack courtyard. It must not approach
J1's secondary through-hole barrels.

**The F.Cu primary pour carries VPOS, not VNEG.** An earlier draft made both
outer pours VNEG and routed VPOS as a bus. That bus has to leave U1 on the
barrier side, turn south past T1, and cross both the SWO trace and the four tap
lanes. The clearance check found the short. VPOS reaches fourteen pads, so a
pour costs nothing and removes every one of those crossings.

U1's exposed pad still gets local F.Cu copper. A small `/VNEG` island at
priority 3, 110.0, 103.0 → 121.0, 112.0, sits above the VPOS pour and holds the
pad, pin 9 and the thermal via array. The 2 in² compliance area is the B.Cu
spreader alone, and it always was.

**Measure the area on the filled zone, never on this table.** A thermal
estimator on the parent board gave 1.74 in² against a real 2.012 in².

## 6. Thermal via array

U1 is a QFN-20 with a 2.75 x 2.75 mm exposed pad, pad 21, on F.Cu only. The
footprint carries no thermal vias. The module adds them.

| Item | Value |
|---|---|
| Array | 3 x 3, nine vias |
| Pitch | 0.9 mm |
| Via | 0.6 mm diameter, 0.3 mm drill |
| Net | `/VNEG` |
| Centre | 114.5, 107.5 |

Positions: x in {113.6, 114.5, 115.4} by y in {106.6, 107.5, 108.4}.

Why 0.9 mm. The outer via edge sits 0.9 + 0.3 = 1.2 mm from the centre. The
exposed pad half width is 1.375 mm. That leaves 0.175 mm of pad copper outside
the via ring. A 1.0 mm pitch leaves 0.075 mm. A 4 x 4 array at 0.75 mm pitch
overruns the pad.

**The four corner vias sit under solder paste.** The footprint puts four 1.2 mm
paste windows at (±0.7, ±0.7). The vias at (±0.9, ±0.9) fall inside them. Tent
the vias on both faces, which is the board default. Ask PCBWay for resin
plugging on a production run. No nine-via arrangement avoids the paste windows
inside a 2.75 mm pad at this via size.

Add at least twelve more `/VNEG` stitching vias in the primary pour, one per
100 mm², none inside a courtyard.

## 7. The inner plane void

A keepout zone on In1.Cu and In2.Cu.

| Item | Value |
|---|---|
| Rectangle | 99.0, 49.0 → 129.5, 135.0 |
| Layers | In1.Cu, In2.Cu |
| Forbids | copper pour |
| Allows | tracks, vias |

It covers the whole primary region, the barrier band and the primary half of the
jack band. It runs past the outline on three sides so no inner copper survives
at the edge.

The secondary ground plane must not run under the primary circuit. Inner copper
there would carry the barrier across on two layers and defeat T1, U2, C16 and
C17. The void is also what lets the thermal vias pass from F.Cu to B.Cu without
touching a secondary plane, and what makes the B.Cu tap jog in section 4 safe.

**It ends at x 129.5, the secondary edge, not at the band centre.** An earlier
draft ended it at 128.25 and left 1.25 mm of inner GND inside the band.

## 8. The isolation slot

| Item | Value |
|---|---|
| Type | NPTH slot |
| Width | 1.0 mm |
| Centre line | x = 128.25 |

PCBWay's minimum NPTH slot is 0.8 mm at ±0.2 mm tolerance, so the module draws
1.0 mm.

The slot breaks at each bridge body. Segments, with a 0.5 mm end margin:

| Segment | Y from | Y to | Length |
|---|---|---|---|
| 1 | 68.5 | 86.75 | 18.25 mm |
| 2 | 93.75 | 97.0 | 3.25 mm |
| 3 | 113.0 | 115.2 | 2.2 mm |
| 4 | 122.8 | 124.25 | 1.45 mm |

**The slot does not run the full height, and it cannot.** Four bridges occupy
the band. The slot is a creepage aid. The 2.5 mm clearance is the requirement,
and the band carries it everywhere, slotted or not.

The slot stops at y 68.5. Above that the jack body spans the band, and
Abracon's construction is the isolation there. See section 1.1.

### 8.1 Cut 2026-09-24

Four closed rectangles on `Edge.Cuts`, drawn through Konnect `add_board_outline`,
which writes over IPC and appends rather than replacing. `Edge.Cuts` now holds
20 lines: 4 for the outline and 16 for the four slots.

| Segment | x from | x to | y from | y to |
|---|---|---|---|---|
| 1 | 127.75 | 128.75 | 68.50 | 86.75 |
| 2 | 127.75 | 128.75 | 93.75 | 97.00 |
| 3 | 127.75 | 128.75 | 113.00 | 115.20 |
| 4 | 127.75 | 128.75 | 122.80 | 124.25 |

Every vertex is used exactly twice, so all five loops close.

**The corners are drawn sharp.** A 1.0 mm router bit cannot cut a sharp inside
corner, so the fab produces rounded ends. That is the normal reading of a
rectangular slot. Say it in `README-FAB.md` and let the fab confirm.

**`Edge.Cuts` travels with a design block.** Measured 2026-09-24 by placing the
block into an empty project. All 16 slot lines arrived, 1.0 mm wide, translated
with the block. **No conversion to NPTH pads is needed.**

In the fragment the module's own outline moves to `Dwgs.User`, so a host sees
the area the block occupies. The 16 slot lines stay on `Edge.Cuts`. See
`GUI-Runbook.md` job 8a, and mind the shared file name.

## 9. Zone table

| Zone | Layer | Net | Rectangle |
|---|---|---|---|
| Heat spreader | B.Cu | `/VNEG` | 100.5, 68.0 -> 127.0, 133.0 |
| Primary pour | F.Cu | `/VPOS` | 100.5, 68.0 -> 127.0, 133.0 |
| Secondary top pour | F.Cu | `GND` | 129.5, 50.5 -> 155.5, 133.5 |
| Secondary bottom pour | B.Cu | `GND` | 129.5, 50.5 -> 155.5, 133.5 |
| Ground plane | In1.Cu | `GND` | 129.5, 50.5 -> 155.5, 133.5 |
| Power plane, lower | In2.Cu | `GND` | 129.5, 95.0 -> 155.5, 133.5 |
| Power plane, upper | In2.Cu | `/3V3A` | 136.0, 68.0 -> 155.0, 94.0 |

Seven zones. No priority and no keepout. No two zones on one layer overlap.

**In2.Cu is split, and In1.Cu is not.** The stackup names In1 `GND` and In2 `PWR`,
and this is what that means in practice. In1 stays one whole ground plane,
because it sits 0.1 mm under F.Cu and carries the return path for every F.Cu
signal in the secondary region. Cutting In1 removes the reference under the
Ethernet section. In2 is the layer that splits.

**The split is what makes U4 routable.** The W5500 is an LQFP-48 on a 0.5 mm
pitch. Its six AVDD pins sit between MDI and AGND pins, three on the top edge
and three on the left. Every F.Cu path from the top three to a 3V3A bus crosses
either the MDI band or the left-side escape fan. With a 3V3A plane under the
part, each pin takes a via straight down. The same plane then feeds C27, C28,
C29, C30, FB5, R18, R20 and R22 with one via each.

**The inner planes stop at x 129.5, the secondary edge of the barrier band.**
The primary side carries no inner copper at all. A secondary plane under the
jack's primary barrels is the exact safety defect that `layout-rules.md` names.

**The F.Cu primary pour carries VPOS, and there is no F.Cu VNEG island.** An
earlier draft added one around U1 to give the exposed pad local copper. Sized
to clear U1's own pads it came to 3.2 x 3.2 mm, about 10 mm2, which buys almost
no thermal path. The 2 in2 compliance area is the B.Cu spreader, reached by the
nine thermal vias of section 6. AN956 measures an OUTER layer plane, and B.Cu
is one.

**The MDI traces have no reference plane inside the jack band.** In1.Cu starts
at x 129.5, and the RD pair runs at x 121.8 to 132.8 above y 68. Nothing can be
done about it, for the reason just given. `Plum-RFBridge` carries the same
characteristic. The runs are under 12 mm and the link is 100BASE-TX.

### 9.1 Editing a zone

Konnect `add_zone` reports success and writes nothing. `add_copper_pour` works,
but it only appends, and it writes the FILE while pcbnew holds its own copy in
memory. `Modules/analysis/zone_tool.py` lists zones and deletes one by uuid, so
a zone can be replaced rather than duplicated.

The delete is safe on this board because a zone carries no cross-reference:
0 groups, and each zone uuid appears exactly once. The tool refuses a uuid it
finds more than once, refuses a uuid that is not a zone, refuses if the
parenthesis balance changes, and writes a timestamped backup first.

**Close the board in pcbnew before any zone write, and open it again after.**
Mixing the file transport with the IPC transport discards work in whichever
direction was written second.

## 10. The breakout row

Twelve vias on the bottom edge at **y = 131.5**. Each carries a 1.0 mm stub on
the opposite layer, ending at y 132.5. A host board lands on the stub.

Via 0.6 mm pad on 0.3 mm drill.

| x | Net | Direction | Arrives on | Stub layer |
|---|---|---|---|---|
| 131.00 | `GND` | stitch | pour | both |
| 134.00 | `GND` | stitch | pour | both |
| 137.00 | `GND` | stitch | pour | both |
| 140.00 | `GND` | stitch | pour | both |
| 143.30 | `/POE_5V` | out | F.Cu | B.Cu |
| 144.90 | `/ETH_CS` | in | B.Cu | F.Cu |
| 146.50 | `/ETH_CLK` | in | B.Cu | F.Cu |
| 148.10 | `/ETH_MISO` | out | B.Cu | F.Cu |
| 149.70 | `/ETH_MOSI` | in | B.Cu | F.Cu |
| 151.30 | `/ETH_INT` | out | B.Cu | F.Cu |
| 152.90 | `/ETH_RST` | in | B.Cu | F.Cu |
| 154.50 | `+3V3` | in | B.Cu | F.Cu |

GND pitch is 3.00 mm. Signal pitch is 1.60 mm. The two groups are separate
because the copper west of x 142.3 is taken: `TLV_K` runs at y 129.15 on F.Cu
and `COMP_SEC` at y 129.4 on B.Cu. **Nothing can descend to the edge there.**
The GND positions need no descent, because the pour reaches them.

`/ETH_RST` breaks out **and** keeps its 4.7 k pull-up (R11) inside the block.
A host drives the pin or leaves it floating.

`/CGND` does not break out. It reaches GND only through C39 inside the block.

**No differential pair crosses the block boundary.** All four MDI pairs run
from J1 to U4 inside the block, so the pair matching is an internal matter.
A host board never has to match anything.

### 10.1 Eight dangling tracks are the interface, not a defect

DRC reports eight `track_dangling` warnings, one for each signal stub. A stub
with a free end is what a breakout point is. Do not delete them, and do not
route them to anything inside the block.

The four GND vias raise no warning. They sit in the pour on every layer.

## 11. Checks before you believe a number

1. Refill the zones. `kicad-cli pcb drc` grades the saved fill unless you pass
   `--refill-zones`, and that flag refills in memory only. It never writes back.
   One run on the parent board showed 61 errors, and 53 were stale fills.
2. Confirm the net classes bind. Open the net inspector and read the class
   column. An unbound class makes the barrier rule pass with zero hits.
3. Confirm the custom rules loaded. Open Board Setup, Custom Rules. A syntax
   error disables the whole file and the command line reports nothing.
4. State a non-zero canary before you believe a DRC count. A drop in violations
   is a suspect event, not a success.
5. Render the board to SVG or PDF and look at the image.

---

## 12. Routing record — feedback loop, LEDs, crystal

Written after the pass that closed the last 22 unconnected items. Each entry is a
decision a future session should not re-derive.

### 12.1 The FB_REF column

`R6` / `R7` / `R8` sit at `x 136`, `y 117` / `120` / `123`. **R7 is rotated 180°** so its
FB_REF pad lands at `136.825` — the same x as `R6.2` and `R8.2`. FB_REF is then one
straight vertical from `117` to `124.7`, and `R7.2` (GND) faces the pour at `135.175`.

Rotating R7 removed a three-segment detour around U2's pad field. Do not rotate it back.

### 12.2 EROUT crosses VDD_PRI on B.Cu

`U1.1` (EROUT) and `R3.2` sit on opposite sides of the VDD_PRI lane at `y 104.5`, which
runs the full width from `105.175` to `114.5` and then dives to `C14.1`. There is no F.Cu
path between them: **C6**'s 2.7 mm pads block `y 101.9–103.05` and the `x 118.3` VSS_PRI
wall seals the east side against T1's pads at `118.725` (a 0.45 mm channel).

EROUT therefore takes **one B.Cu segment, `111.95 → 122.0` at `y 103.6`**, with a jog to a
via at `(116.1, 104.1)` for U1.1. The jog exists because a via on the straight lane would
sit 0.15 mm from `C6.1` — the netclass wants 0.2.

This cut costs the B.Cu VNEG spreader about 6 mm² out of 1290 and does not sever it: the
island is open both west of `111.95` and east of `122.0` at that y.

### 12.3 EROUT's east branch avoids starving T1.1

The branch to `U2.4` runs at `x 122.0`, not `121.5`. At `121.5` it left `T1.1` (VPOS) with
one thermal spoke and DRC reported `starved_thermal`. Moving it 0.5 mm east restores the
pad's east spoke. **Check the spoke count after any trace placed within 1 mm of a
through-hole pad that relies on a pour.**

### 12.4 TP1

`TP1` moved to `(119.5, 97.0)`. Its courtyard is asymmetric — it extends `+1.0` in x and
`+0.7` in y from the origin, so the origin must sit at `y ≤ 97.32` to clear T1's courtyard
at `98.02`.

### 12.5 POE_5V leaves the bottom band

`POE_5V` used to reach `C16.2` along `y 130.8`. That lane is now free: POE_5V drops to
B.Cu at `(139.5, 124.0)` and reaches the `C16.2` barrel directly, because C16 is
through-hole. The freed band carries TLV_K at `130.9` and the COMP_SEC crossing.

### 12.6 TLV_K and COMP_SEC cross on B.Cu

Both leave the secondary regulator cluster heading for `C18` at `x ~141`. They must cross.
COMP_SEC takes the hop: F.Cu down `x 134.6`, via at `(135.0, 129.4)`, B.Cu east under the
TLV_K lane, via at `(142.275, 130.6)`, F.Cu up into `C18.2`.

TLV_K stays on F.Cu the whole way and enters `U3.2` from below at `x 135.8`. It was at
`135.6` first; that put it 0.1 mm from the COMP_SEC via, because **Konnect's `add_via`
makes a 0.8 mm pad, not the 0.6 mm `check_plan.py` assumed.** The checker has been
corrected.

### 12.7 The crystal was rebuilt to free U4's LED pins

This is the largest change in the pass, and the reason is worth stating plainly.

`U4.25` (LINKLED) and `U4.27` (ACTLED) are on U4's bottom edge at `x 140.75` and `141.75`.
Every escape was sealed:

| Direction | Blocked by |
|---|---|
| North, under the body | GND via `(141.0, 82.25)`, +3V3 escape at `x 141.9`, 0.5 mm pad pitch |
| North-west corridor at `y 83.2` | fits exactly **one** 0.2 mm trace between `U4.24`'s pad and the bottom row |
| South | XI's horizontal at `y 85.4`, spanning `138.725 → 143.25` |
| South, further out | Y1's pads start at `y 86.55` — the band is 1.65 mm and already holds XI, XO's via and Y1's GND via |

XI ran west to `x 141.1`, then south, because a direct `U4.30 → Y1.1` path was blocked by
`Y1.4`'s pad (`x ≤ 143.1`) and **XO's via at `(143.75, 85.9)`**. Moving XO's via east to
`(145.6, 85.8)` opens the 0.8 mm channel between `Y1.4` and `Y1.3`, and XI then runs
`143.25 → 143.5 → 88.45 → Y1.1` entirely on F.Cu.

With XI's `y 85.4` horizontal gone, both LED pins escape straight south to vias at
`(140.75, 85.8)` and `(141.85, 85.8)`.

Consequences, all deliberate:

- **`C22` is rotated 180°** so its XI pad faces `Y1`. This shortened XI by 1.55 mm.
- **Y1.4's GND via and its stub trace were deleted.** Y1.4 connects to the F.Cu GND pour by
  thermal relief, exactly as `Y1.2` always did. The via existed only to clear a lane that
  no longer runs there.
- XO keeps its B.Cu hop from `(145.6, 85.8)` to `(145.85, 90.4)`; it still has to cross
  XTAL_B at `y 87.15`.

### 12.8 The LED nets use the east edge

`ACTLED` and `LINKLED` run the full height on B.Cu at `x 154.7` and `x 155.2`. That
channel is free only because **TCT was moved off the board edge**: it used to run
`(155, 63) → (155, 71.225) → (154, 71.225)` and `(155, 75.175) → (154, 75.175)`. It now
comes off its via at `(153.0, 63.0)` and reaches both `C36.1` and `R22.1` from `x 153.2–153.5`.

`C36.2` lost a thermal spoke to that re-route and gained a GND via at `(154.0, 74.0)`.

The two LED lanes turn west at **`y 95.5`** (ACTLED) and **`y 96.5`** (LINKLED). ACTLED was
at `y 94.0` first and shorted to the ETH_RST via; 95.5 clears it by 2.0 mm.

`LED_ACT_K` is a short F.Cu run from `J1.14`. `LED_LINK_K` leaves `J1.12` on B.Cu, passes
**west of `SH2` at `x 115.4`** — `115.5` failed the 0.4 mm `Chassis clearance` rule against
the shield barrel — runs east at `y 60.9` in the band between the shield barrels
(`y ≤ 60.11`) and J1's row-1 barrels (`y ≥ 61.51`), then north at `x 134.6` to a via at
`(141.175, 51.5)`.

That `y 60.9` B.Cu lane crosses the barrier band inside J1's courtyard, where the
`.kicad_dru` exception applies. It is the only conductor that does so outside the pad
field itself.

### 12.9 +3V3 reaches the jack along the top

`J1.11` and `J1.13` are linked by a **B.Cu segment at `y 53.37`** between their own
barrels, clear of the NPTH posts at `y 54.285–57.535`. From `J1.13` the rail runs F.Cu at
`y 56.3` to `x 155.0`, then south to `y 90.5` and west into the existing +3V3 at
`(152.225, 89)`.

The `x 132.8` vertical is 0.05 mm east of where it wants to be: at `132.7` it failed the
0.254 mm `NPTH to Track clearance` against the post at `(130.715, 55.91)`.

### 12.10 The VPOS pour was in two pieces

`CT1_NET` and `CT2_NET` form two nested rings around U1 — verticals at `x 101.1` / `101.9`
and `114.5` / `115.3`, horizontals at `y 84` / `85` and `112.6` / `113.4`. The pour pinches
to about 0.05 mm of copper between `CT1` at `x 101.1` and the zone's west edge at `100.5`,
which is under the 0.25 mm `min_thickness`, so the strip holding `U1.12` separated.

`U1.12` was the only VPOS pad on the orphaned island. It now hops to B.Cu at
`(113.7, 111.6)` and returns at `(113.7, 115.0)`, south of both rings. A 3.4 mm slit in
the VNEG spreader, which does not reach either edge of the island.

**Do not try to fix this on F.Cu.** Every westward and southward lane out of that pocket is
taken by `SP1_NET` (`x 112.9`), `SP2_NET` (`y 111.0`, `x 111.9`) or the CT rings.

### 12.11 State at the end of the pass

```
pads 254   segments 330   vias 74
kicad-cli pcb drc --severity-all --schematic-parity --refill-zones
  0 errors   0 unconnected   0 parity
  76 warnings:  55 silk_overlap   17 silk_over_copper   4 lib_footprint_issues
```

The zone fills stored in the file are **stale** — `--refill-zones` refills in memory only.
Open the board, `Edit → Fill All Zones`, save, before plotting anything.

Remaining: the silkscreen pass, the isolation slot (GUI runbook job 2), the breakout row
in §10, and the copy into `PlumBlocks/`.

---

## 13. Routing record — the SPI escape and the breakout row

### 13.1 Why the SPI nets needed a via fanout

`/ETH_CS`, `/ETH_CLK`, `/ETH_MISO`, `/ETH_MOSI` and `/ETH_INT` sit on U4 pads
32 to 36, bottom edge, 0.5 mm pitch, x 144.25 to 146.25.

Every escape to the south was sealed:

| Route | Blocked by |
|---|---|
| south, x 144.2 to 145.6 | XO's F.Cu lane at y 85.8 |
| south, x 145.2 to 146.0 | XO's via at (145.6, 85.8) |
| south, below y 86.55 | Y1's pad row |
| north, under the body | GND vias at (141.0, 82.25) and (142.75, 82.5), the +3V3 escape at x 141.9 |

The band between U4's pads (y 84.9) and Y1 (y 86.55) is 1.65 mm. It already
held XI, XO and Y1's ground. It cannot take five more escapes.

### 13.2 The fanout

Five vias at **y 82.3**, x 143.65 / 144.35 / 145.05 / 145.75 / 146.45.
**0.50 mm pad on 0.30 mm drill**, 0.70 mm pitch, 0.10 mm annular ring.

That band is bounded by the `+3V3` B.Cu bridge at y 81.5 above and U4's pad
row at y 83.425 below — 1.8 mm, which takes exactly one via row.

The escapes are 0.15 mm wide and fan outward from the pads, so they do not
cross. `/ETH_CS` leaves its pad at **x 144.30**, not the pad centre. At 144.25
it came within 0.19 mm of U4.31, and at 144.35 within 0.175 mm of U4.33. The
window is about 0.1 mm wide.

**The 0.70 mm pitch gives 0.40 mm hole to hole and the board rule asks for
0.50 mm.** The `.kicad_dru` carries a relaxation scoped to `U4.insideCourtyard`
and nothing else. Raise it with the fab before you order.

### 13.3 The descent

The five lanes run south on B.Cu, spread to 1.2 mm pitch at y 94.6, then cross
to F.Cu for 2.7 mm and back to B.Cu at y 97.3.

**The F.Cu window exists because `/ACTLED` and `/LINKLED` cross the whole board
on B.Cu at y 95.5 and y 96.5.** No B.Cu lane can pass them. The window sits at
x 142.6 to 147.4, west of R11 and east of R9.

Below y 97.3 the B.Cu is empty, so each lane steps east on a staggered 45°
jog and drops to the row. The jogs run east to west in y order — `/ETH_INT`
first at y 100, `/ETH_CS` last at y 121 — so no two lanes cross.

`/ETH_RST` and `+3V3` join the row from the east side. `+3V3` reuses the x 155
F.Cu lane it already had, and crosses to B.Cu at the same y 97.3.

A GND stitch via moved from (145.0, 128.5) to (142.0, 126.0). It sat on the
`/ETH_CS` lane.

### 13.4 The GND pour split, and why R12 moved

The pass left one `Zone [GND] on F.Cu` in three pieces. The 15.10 mm2 island at
x 143.70 to 149.05, y 82.74 to 91.20 held **Y1 pin 2**, the crystal case ground.

The pinch was 0.10 mm of copper between **R12 pad 2** at x 148.675 and the
`+3V3` rail at x 149.3, at y 91.0 to 92.0. The `min_thickness` is 0.25 mm, so
the pour broke there.

No via could repair it from inside. Five B.Cu lanes cross that pocket —
`/ETH_CLK` at 143.8, `/ETH_MISO` at 144.9, `/ETH_MOSI` at 146.6, `/ETH_INT` at
147.15 and `/ETH_RST` at 148.5 — and the widest gap between them is 0.55 mm.

**R12 moved from x 147.5 to x 146.9.** That opens the pinch to 0.70 mm. `/XO`
and `/XTAL_B` follow it. Do not move R12 back.

### 13.5 State at the end of the pass

```
pads 254   segments 401   vias 103
kicad-cli pcb drc --severity-all --schematic-parity --refill-zones
  0 errors   0 parity
  0 unconnected
  85 warnings:  56 silk_overlap   17 silk_over_copper
                 8 track_dangling  4 lib_footprint_issues
```

Canary: a 3 mm track-to-track rule raises 286 clearance hits, and removing it
returns 0. The rules file loads, the scoped fanout rule included.

### 13.6 The footprint library is now inside the module

The four custom footprints live at `libraries/PoEEthModule.pretty/`. They are
byte-identical copies of the `PlumRFBridge` originals. The project
`fp-lib-table` carries a `PoEEthModule` row with a `${KIPRJMOD}` path, so the
module needs no network mount.

The nickname had to change. **A project library table does not shadow the
global one**, so a second `PlumRFBridge` row would have resolved to the global
one and changed nothing.

The schematic points at the new nickname. **The board does not yet.** That is
why DRC reports 4 `footprint_symbol_mismatch` parity issues. `GUI-Runbook.md`
job 5 closes them with one Update PCB from Schematic.

ERC fell from 34 to 30 on this change. The four `footprint_link_issues` went,
and every other ERC count held.

Five **symbols** still come from `PlumRFBridge`: `Si3402-B`, `FA2924-AL`,
`ARJM11C7-114-BA-EW2` and `TLV431`. A `.kicad_sch` caches every symbol it uses,
so the schematic opens and ERC runs without the library.

**Open items**

1. `GUI-Runbook.md` job 5 — Update PCB from Schematic. Clears 4 parity issues
   and 4 `lib_footprint_issues`.
2. `GUI-Runbook.md` job 6 — move 25 passive refdes to `F.Fab`. Clears most of
   the 73 silkscreen warnings.
3. `GUI-Runbook.md` job 2 — cut the isolation slot.

The 30 remaining ERC violations are all structural to a module board: 19
hierarchical labels with no parent sheet, 6 pins with no driver inside the
block, and 5 labels on a single pin. A host project supplies all three.

---

## 14. Silkscreen classification

Measured after `GUI-Runbook.md` jobs 5 and 6, on the saved board.

```
silk_over_copper      17 -> 0
silk_overlap          56 -> 28
lib_footprint_issues   4 -> 0
schematic parity       4 -> 0
```

64 reference designators sit on `F.Fab`. 18 stay on `F.Silkscreen`.

### The 28 that remain

| Count | Class | Action |
|---|---|---|
| 24 | A footprint outline crosses **its own** pads | none |
| 2 | A reference sits on **its own** body outline, T1 and U1 | none |
| 2 | T1's body outline crosses the TP2 and U1 references | none |
| 1 | D3 and L1 references landed on the same point | **fixed 2026-09-24** |

**The 24 are harmless once the soldermask is subtracted.** Plot the silk with
`--subtract-soldermask`, and no ink reaches an exposed pad. The legend file
becomes polygon based and larger than stroked silk. That is intended. Say so in
`README-FAB.md`, and offer to re-issue without it.

Confirmed on this board:

```
kicad-cli pcb export gerbers -o out --layers "F.Silkscreen,F.Mask" \
    --subtract-soldermask PoE-Ethernet-Si3402-W5500.kicad_pcb
```

T1 and J1 account for 19 of the 24. Both footprints draw a body rectangle that
crosses their own through-hole pads. The three test points draw a circle around
their own pad.

### The one real defect

`D3` sits at rotation 180, so its reference offset of `0, -3` maps to `0, +3`
on the board. The text lands at **142.5, 106.0**. `L1` puts its own text at
**142.5, 105.95**. The two designators print on top of each other, and neither
reads.

Fixed on 2026-09-24. D3's reference offset is now `0, +3`, which maps to
y 100.0. `silk_overlap` fell from 29 to 28.

### The 8 track_dangling warnings

They are the breakout stubs. See §10.1. Do not remove them.

---

## 15. Closing state, 2026-09-24

```
pads 254   segments 401   vias 103

kicad-cli pcb drc --severity-all --schematic-parity --refill-zones
  0 errors   0 unconnected   0 parity
  36 warnings:  28 silk_overlap   8 track_dangling

kicad-cli sch erc --severity-all
  30 violations, all structural to a module board
```

Canary: a 3 mm track-to-track rule raises 286 clearance hits. Removing it
returns 0. The rules file loads.

**Every warning is classified.** §14 covers the 28 silkscreen items, §10.1 the
8 breakout stubs, and §13.6 the 30 ERC items.

**Verified, not estimated**

| Check | Result |
|---|---|
| VNEG heat spreader on the filled zone | 2.59 in², against 2 in² |
| Board outline | one closed rectangle, 56 x 84 mm |
| Pads outside the outline | none |
| Courtyard overlaps | none |
| Copper to board edge | 0.80 mm minimum |
| Zone islands | every zone one piece |
| Interface nets reaching the edge | 9 of 9 |
| Footprint library | inside the module, `${KIPRJMOD}` path |

**The isolation slot is cut.** See §8.1.

---

## 16. The block fragment test, 2026-09-24

Placed `PoE-Ethernet-Si3402-W5500` from `PlumBlocks` into an empty project,
then ran Update PCB from Schematic with all three Options ticked.

### Everything travels

| Item | Module | Placed |
|---|---|---|
| footprints, with placement | 82 | 82 |
| segments | 401 | 401 |
| vias | 103 | 103 |
| zones | 7 | 7 |
| `F.Fab` breakout labels | 12 | 12 |
| `Edge.Cuts` slot lines | 16 | 16 |
| `Dwgs.User` outline reference | 4 | 4 |
| board group | — | 1 |

Connectivity holds. The placed board reports **one** unconnected item, a GND
pour split, because the host had no inner layers to carry it.

Its 552 DRC violations are the absence of net classes, minimums and custom
rules. `Host-Setup.md` supplies all three.

### KiCad re-annotates the references

**The block's `U4` is not the host's `U4`.** Component values agreed for only
23 of 82 references after placement. The setting is `keep_annotations` in the
design block chooser, and it is off by default.

Never compare a placed block to its module by reference designator. Compare by
count, by relative geometry or by net membership.

### Three defects the test found

| Defect | Cause | Fix |
|---|---|---|
| Footprints not found | the vendored library was project scoped | registered `PoEEthModule` in the **global** table |
| Library parse errors | `cp -p` wrote 45 AppleDouble `._` files onto the synced volume | removed them all, use `cp -X` |
| Three groups from one placement | the module schematic held two stale `(group ...)` definitions from its own build | removed them, then re-copied to the block |

The third is the one to watch on the other eight blocks. **A module schematic
assembled from blocks keeps their group definitions.** Strip them before you
copy the schematic into a fragment. Net membership proves the strip is safe:
81 nets and 253 nodes, sets identical before and after.
