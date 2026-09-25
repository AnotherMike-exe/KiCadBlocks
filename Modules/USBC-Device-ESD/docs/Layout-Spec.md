# Layout Spec — USBC-Device-ESD

The geometry of the module reference board, as laid out on 2026-09-24.
Every number is a decision, and each one carries its reason. §11 lists every
change from the draft, and §12 gives the closing state.

Board: 20 x 21 mm, 4 layers, 1.6 mm, PCBWay. Written 2026-09-24.

Re-derive every figure from the files before you trust it. Run ERC, DRC with
`--refill-zones`, and a canary first.

---

## 0. Sources

| Item | Document | Revision |
|---|---|---|
| J1 | GCT drawing `USB4110` (USB4110-GF-A), sheet 1 of 2 | **B4**, 22 May 2024 |
| U2 | ST datasheet `USBLC6-2` | **not held.** See §8 |
| Footprint | KiCad 10 `Connector_USB:USB_C_Receptacle_GCT_USB4110` | shipped library |
| Placement | `_resources/Examples/Plum-RFBridge/Plum-RFBridge.kicad_pcb` | as found 2026-09-24 |

The drawing is in `_resources/Research/USB4110/usb4110.pdf`. Never commit it.

## 1. The block

4 parts. 9 nets. From the exported block netlist, not from the drawing.

| Ref | Value | Footprint |
|---|---|---|
| J1 | USB-C | `Connector_USB:USB_C_Receptacle_GCT_USB4110` |
| U2 | USBLC6-2SC6 | `Package_TO_SOT_SMD:SOT-23-6` |
| R1 | 5.1k | `Resistor_SMD:R_0603_1608Metric` |
| R2 | 5.1k | `Resistor_SMD:R_0603_1608Metric` |

| Net | Members |
|---|---|
| `/VBUS` | J1.A4 A9 B4 B9, U2.5 |
| `/USB_DP_CONN` | J1.A6 B6, U2.1 |
| `/USB_DM_CONN` | J1.A7 B7, U2.3 |
| `/USB_DP` | U2.6 |
| `/USB_DM` | U2.4 |
| `/USB_CC1` | J1.A5, R1.1 |
| `/USB_CC2` | J1.B5, R2.1 |
| `GND` | J1.A1 A12 B1 B12 SH, R1.2, R2.2, U2.2 |

**U2 sits in series in the data pair.** USBLC6-2 pins 1 and 6 are one
internal line, and pins 3 and 4 are the other. The cable side (`*_CONN`) lands
on pins 1 and 3. The host side leaves from pins 6 and 4. The pair flows
straight through the package. Do not tee it.

**Only `VBUS` is a hierarchical label.** `USB_DP` and `USB_DM` are local
labels. Pasted into a host sheet as a design block, they join by name. Placed
as a hierarchical sheet, the block exposes `VBUS` and no data pair. Make the
two data labels hierarchical, or record why not.

**The shield goes straight to GND.** No capacitor and no chassis net. That is
the block's choice, and it differs from the Ethernet block's `/CGND`.

## 2. The connector

### 2.1 The shell is SMT, not through-hole

The GCT drawing names the part "SMT Type, PCB Top Mount". The recommended
layout shows four **solder pads** of 2.18 x 2.00 mm for the shell. The KiCad
footprint matches: four `SH` SMD pads, `attr smd`.

The only holes are two Ø0.65 mm NPTH locating pegs. So the shell holds by
solder alone. Give each `SH` pad full copper and no thermal relief to the GND
pour, because the pads take the mating force (5 to 20 N, drawing).

### 2.2 Where the board edge goes

The footprint draws a `PCB Edge` line on `Dwgs.User` at local y = +3.675.
That is the front face of the body. The drawing gives body length 7.35 mm
and 2.85 mm from the front shell pads to the front face. The front shell pads
sit at local y = +0.825, and 0.825 + 2.85 = 3.675. The two agree.

**Put that line on `Edge.Cuts`.** The receptacle face is then flush with the
board edge.

`Plum-RFBridge` did not do this. Its J1 sits at (151.15, 54.25), rotation 180,
so the edge line lands at y 50.575, and the board edge is at y 50.0. The face
sits **0.575 mm behind the edge**. The drawing's mating view needs 1.85 mm
minimum of plug engagement, and a recessed face eats into that inside an
enclosure. This module places it flush.

### 2.3 Pad coordinates, footprint local

| Pad | x | y | Size |
|---|---|---|---|
| A1, B12 | -3.20 | -3.68 | 0.60 x 1.15 |
| A4, B9 | -2.40 | -3.68 | 0.60 x 1.15 |
| A5 | -1.25 | -3.68 | 0.30 x 1.15 |
| B8 | -1.75 | -3.68 | 0.30 x 1.15 |
| B7 | -0.75 | -3.68 | 0.30 x 1.15 |
| A6 | -0.25 | -3.68 | 0.30 x 1.15 |
| A7 | +0.25 | -3.68 | 0.30 x 1.15 |
| B6 | +0.75 | -3.68 | 0.30 x 1.15 |
| A8 | +1.25 | -3.68 | 0.30 x 1.15 |
| B5 | +1.75 | -3.68 | 0.30 x 1.15 |
| A9, B4 | +2.40 | -3.68 | 0.60 x 1.15 |
| A12, B1 | +3.20 | -3.68 | 0.60 x 1.15 |
| SH rear | ±5.11 | -3.105 | 2.18 x 2.00 |
| SH front | ±5.11 | +0.825 | 2.18 x 2.00 |
| NPTH | ±2.89 | -2.605 | Ø0.65 |

Courtyard: x ±6.7, y -4.76 to +4.18.

**The data pads interleave.** Left to right: B7 D−, A6 D+, A7 D−, B6 D+. The
two D+ pads and the two D− pads cannot join on one layer. §5 bridges them.

## 3. Outline

| Item | X | Y |
|---|---|---|
| Board outline | 100.0 → 120.0 | 100.0 → 121.0 |
| Mating edge | top, y 100.0 | — |
| Breakout row | 101.5 → 118.5 | 118.5 |

20 mm wide because J1's courtyard spans 13.4 mm, and 3.3 mm each side keeps
the shell pads 1.85 mm or more from every edge. 21 mm tall because the
RFBridge stack-up of J1, bridge vias, U2 and CC resistors ends at y 116.45,
and the breakout row sits 2.5 mm above the bottom edge, as on the PoE module.

## 4. Placement table

As placed, read back from the saved file. Carried over from `Plum-RFBridge`
without change. J1 moves from (151.15, 54.25) to
(110.0, 103.675). Every other part keeps its offset from J1, so the whole
cluster translates by **(−41.15, +49.425)**.

| Ref | X | Y | Rot | RFBridge X, Y |
|---|---|---|---|---|
| J1 | 110.000 | 103.675 | 180 | 151.150, 54.250 |
| R1 | 114.015 | 112.677 | 270 | 155.165, 63.252 |
| R2 | 108.450 | 112.697 | 270 | 149.600, 63.272 |
| U2 | 111.350 | 114.425 | 270 | 152.500, 65.000 |

J1's y is 100.0 + 3.675, so the `PCB Edge` line lands on y 100.0 (§2.2).

The resulting pad positions, for checking:

| Pad | X | Y | Net |
|---|---|---|---|
| J1.B6 | 109.25 | 107.355 | `/USB_DP_CONN` |
| J1.A7 | 109.75 | 107.355 | `/USB_DM_CONN` |
| J1.A6 | 110.25 | 107.355 | `/USB_DP_CONN` |
| J1.B7 | 110.75 | 107.355 | `/USB_DM_CONN` |
| J1.A9/B4 | 107.60 | 107.355 | `/VBUS` |
| J1.A4/B9 | 112.40 | 107.355 | `/VBUS` |
| J1.B5 | 108.25 | 107.355 | `/USB_CC2` |
| J1.A5 | 111.25 | 107.355 | `/USB_CC1` |
| U2.1 | 112.30 | 113.287 | `/USB_DP_CONN` |
| U2.2 | 111.35 | 113.287 | `GND` |
| U2.3 | 110.40 | 113.287 | `/USB_DM_CONN` |
| U2.4 | 110.40 | 115.563 | `/USB_DM` |
| U2.5 | 111.35 | 115.563 | `/VBUS` |
| U2.6 | 112.30 | 115.563 | `/USB_DP` |

**CC1 goes right, CC2 goes left.** J1.A5 sits at x 111.25 and R1 is east of
it. J1.B5 sits at 108.25 and R2 is west of it. Both are straight escapes.

Courtyard check after placement (`check_courtyards.py`): no overlap, no gap
under 0.05 mm. J1's courtyard runs to y 99.495, past the mating edge, by
design (§2.2). DRC reports no edge-clearance violation on J1.

## 5. Routing

### 5.1 The data pair bridge

As built. The draft's bridge (D− vias at y 108.60, D+ vias at 109.65, both
straight under the pads) does not fit 0.6 mm vias: the D+ stub from A6 passes
0.5 mm from the centre of each D− via, a 0.10 mm gap against the 0.20 mm
netclass. See §11.

Pad order left to right on the board: B6 D+ 109.25, A7 D− 109.75, A6 D+ 110.25,
B7 D− 110.75.

| Step | Net | Layer | Geometry |
|---|---|---|---|
| 1 | D− | F.Cu | A7 down to y 108.50, 45° west to x 109.60, down to 109.70 |
| 2 | D− | F.Cu | B7 down to y 108.50, 45° east to x 110.95, down to 109.70 |
| 3 | D− | F.Cu | the two legs join at y 109.70; from (110.40, 109.70) straight down to U2.3 |
| 4 | D+ | F.Cu | A6 straight down, inside the D− U, to via (110.25, 109.00) |
| 5 | D+ | F.Cu | B6 down to y 108.05, 45° west to x 108.95, down to via (108.95, 109.00) |
| 6 | D+ | B.Cu | (108.95, 109.00) → (110.25, 109.00) → (111.00, 109.00) → (112.30, 110.30) → via (112.30, 111.90) |
| 7 | D+ | F.Cu | via (112.30, 111.90) straight down to U2.1 |

D− joins on F.Cu as a U. D+ jumps it on B.Cu. That swaps the pair order to
match U2 (D− on pin 3 west, D+ on pin 1 east) with no second crossing.
The neighbour escapes (B6 D+, CC1) turn at y 108.05, before the D− legs turn at
108.50, so no two 45° runs sit side by side at 0.5 mm pitch (0.354 mm apart,
a 0.154 mm gap).

Vias 0.6 / 0.3. Pad escapes 0.20 mm. Smallest designed gap in the bridge:
0.25 mm (D− leg to D+ via, CC2 to VBUS via).

Lengths, connector pad to U2: D− (A7) 6.79 mm, D+ (A6) 7.22 mm. The B7 and B6
legs are the unmated-orientation stubs, 2.98 and 3.07 mm.

### 5.2 Differential pair, host side

`/USB_DP` and `/USB_DM` leave U2.6 and U2.4 as a pair.

**Net class `USB`: 0.20 mm track, 0.20 mm gap.** The same figures as the PoE
module's `MDI` class.

| Width / gap | Z single | Z diff | Method |
|---|---|---|---|
| 0.20 / 0.20 | 44.8 Ω | **84.4 Ω** | Kirschning–Jansen, t = 35 µm |
| 0.20 / 0.25 | 44.8 Ω | 85.7 Ω | same |
| 0.17 / 0.20 | 48.9 Ω | 92.0 Ω | same |
| 0.15 / 0.25 | 52.2 Ω | 99.8 Ω | same |

Edge-coupled microstrip on F.Cu over In1.Cu GND, 0.10 mm prepreg,
εr 4.5, 35 µm copper. The stackup is the PoE module's, `Host-Setup.md` §1.
Solder mask is not modelled; it lowers each figure by a few ohms.

**0.20 / 0.20 gives about 84 Ω, not 90 Ω.** It is inside the USB 2.0 band of
90 Ω ±15 %, which is 76.5 to 103.5 Ω. Keep it, for three reasons:

1. The block is Full Speed, 12 Mb/s. Its edges are 4 ns or slower. Every run
   on this board is under 10 mm, far below any critical length.
2. It keeps one pair geometry across the module family.
3. 0.17 / 0.20 hits 92 Ω but sits under the 0.20 mm board minimum.

Recompute with KiCad's calculator before any High Speed variant.

### 5.3 Widths

| Net | Width | Why |
|---|---|---|
| `/VBUS` | 0.508 mm, `Power_2` | 1 A class load. The 5 V rail feeds the power mux |
| `GND` | pour | — |
| `/USB_CC1`, `/USB_CC2` | 0.20 mm | a pull-down, microamps |
| `/USB_DP`, `/USB_DM` | 0.20 / 0.20 | §5.2 |
| `*_CONN` bridge | 0.20 mm | §5.1 |

As built. There is no VBUS polygon. Every VBUS track is 0.508 mm, and every
layer change uses two vias:

- J1.A9/B4 (107.60): F.Cu down to vias (107.60, 108.65) and (107.60, 109.45),
  then B.Cu straight down x 107.60 to y 117.00.
- J1.A4/B9 (112.40): F.Cu down to vias (112.40, 108.65) and (112.40, 109.45),
  then B.Cu 45° to (113.30, 110.35), east to x 116.00, down to y 117.00.
- A B.Cu bus at y 117.00 from x 107.60 to 116.00 joins both sides. It drops to
  the two row vias at x 107.20 and 108.80.
- U2.5: F.Cu 0.508 mm tap straight down to vias (111.35, 117.00) and
  (111.35, 117.80), joined on both layers, onto the bus.

The right-hand VBUS path goes round the east side because the D+ B.Cu jumper
(§5.1) cuts across the direct line from the right vias to the row.

GND ties: J1.B1/A12 and J1.A1/B12 each take a 0.3 mm track to a via at
y 108.90. U2.2 has a via at (111.35, 112.30), 1 mm from the pad. R1.2 and R2.2
each have a via beside the pad.

## 6. Zones

| Zone | Layer | Net | Rectangle |
|---|---|---|---|
| Top pour | F.Cu | `GND` | 100.5, 100.5 → 119.5, 120.5 |
| Ground plane | In1.Cu | `GND` | 100.5, 100.5 → 119.5, 120.5 |
| Inner 2 | In2.Cu | `GND` | 100.5, 100.5 → 119.5, 120.5 |
| Bottom pour | B.Cu | `GND` | 100.5, 100.5 → 119.5, 120.5 |

**In1 stays whole under the pair.** It is the reference for §5.2. Do not
route on In1.

In2 is GND, not a power plane. The board has no rail that needs a plane.

Stitch GND at 2.5 mm or less along both sides of the data pair, and one via
per `SH` pad beside it.

## 7. The breakout row

Via 0.6 mm pad on 0.3 mm drill. Row at **y = 118.5**. Each signal via carries a
1.0 mm stub on the far layer, ending at y 119.5. GND pitch 3.0 mm, signal pitch
1.6 mm, as on the PoE module.

| x | Net | Direction | Arrives on | Stub layer | F.Fab label |
|---|---|---|---|---|---|
| 102.2 | `GND` | stitch | pour | none | GND |
| 105.2 | `GND` | stitch | pour | none | GND |
| 107.2 | `/VBUS` | out | B.Cu | F.Cu, 0.508 | VBUS |
| 108.8 | `/VBUS` | out | B.Cu | F.Cu, 0.508 | VBUS |
| 110.4 | `/USB_DM` | both | F.Cu | B.Cu, 0.20 | USB_DM |
| 112.0 | `/USB_DP` | both | F.Cu | B.Cu, 0.20 | USB_DP |
| 115.2 | `GND` | stitch | pour | none | GND |
| 118.2 | `GND` | stitch | pour | none | GND |

Labels are F.Fab, rotation 90, 0.7 mm, at y 117.3 (1.2 mm inboard).

`/USB_DM` drops straight from U2.4 at x 110.4. `/USB_DP` jogs 0.3 mm west
from U2.6 at x 112.3. The pair stays a pair to the row.

**A differential pair crosses this block boundary.** That differs from the
PoE module. The host must continue the pair at 0.20 / 0.20 over GND to its
MCU.

**`/VBUS` breaks out on two vias**, 107.2 and 108.8, both on the row. One
0.3 mm plated via carries roughly 1 A, so two give margin for the 1 A class
load.

`/USB_CC1` and `/USB_CC2` do not break out. The 5.1 k pull-downs stay inside.

## 8. USBLC6-2 layout guidance

**The ST datasheet is not in `_resources/Research/`.** `st.com` timed out on
every scripted download on 2026-09-24. Fetch it by hand and confirm the three
points below against it. They are the standard guidance for this part,
recalled, not quoted.

1. Put U2 as close to J1 as the bridge allows. The ESD path should reach U2
   before it reaches anything else. Here U2.1 and U2.3 sit 5.9 mm from J1's
   pad row, as on `Plum-RFBridge`.
2. Give U2.2 the shortest possible path to the GND plane. One via directly
   at the pad.
3. Route the data lines through the pins, in at 1 and 3, out at 6 and 4. No
   stubs.

## 9. PCBWay edge rule

**PCBWay needs break-away rails when copper sits within 3.5 mm of an edge**
(`docs/Block-Modules-Handoff.md` §4.5). J1's front shell pads sit 1.85 mm from
the mating edge, and the breakout stubs 1.5 mm from the bottom edge. So this
board needs rails.

Put the rails on the **left and right** edges. A rail on the mating edge would
leave a break-off nub on the receptacle face.

## 10. Checks before you believe a number

1. `kicad-cli pcb drc --severity-all --schematic-parity --refill-zones`.
2. Canary: append a 3 mm clearance rule, confirm the count explodes, restore.
3. Net membership: export the netlist and compare `(ref, pin)` sets with §1.
4. Render F.Cu and look at the bridge.
5. Count segments from each interface net to its breakout via.

## 11. Changes from the draft

| # | Draft | As built | Why |
|---|---|---|---|
| 1 | §5.1 bridge: D− joined on B.Cu, vias at y 108.60; D+ vias at 109.65 straight under the pads | D− joined on F.Cu as a U; D+ vias at (108.95, 109.00) and (110.25, 109.00), B.Cu jumper to (112.30, 111.90) | `check_plan.py`: the draft left 0.10 mm between each D+ pad stub and the D− vias at 0.5 mm pitch. The netclass needs 0.20 |
| 2 | §5.1 escapes straight down | B6, D− legs and CC1 each take one 45° jog, staggered in y | parallel 45° runs at 0.5 mm pitch leave 0.154 mm |
| 3 | §5.1 D+ via at (111.575, 110.90) | (112.30, 111.90), straight above U2.1 | clears the CC1 run and the VBUS vias |
| 4 | §5.3 VBUS joins on B.Cu directly | right side goes round the east (x 116.0) to a bus at y 117.0 | the D+ B.Cu jumper blocks the direct path |
| 5 | §5.3 U2.5 tap 0.20 mm | 0.508 mm, two vias to the bus | brief: all VBUS at `Power_2`, two vias per layer change |
| 6 | §7 one VBUS via at 108.8 | two, 107.2 and 108.8, each with a 1.0 mm F.Cu stub and a label | brief; one via is marginal at 1 A |
| 7 | §6 stitching unspecified | 17 GND vias: 4 row, 4 beside the `SH` pads (x 102.9 / 117.1), 2 at the J1 GND pads, U2.2, R1.2, R2.2, and 4 along the pair | §6 asks for stitching at 2.5 mm or less and one per `SH` pad |

Placement, outline and zones are as drafted.

## 12. Closing state

Checked 2026-09-24 on the saved board, `kicad-cli pcb drc --severity-all
--schematic-parity --refill-zones`.

| Item | Count |
|---|---|
| Track segments | 57 |
| Vias | 30 (13 signal and VBUS, 17 GND) |
| DRC errors | 4, all `hole_clearance`, see below |
| Unconnected | 0 |
| Schematic parity | 0 |
| `track_dangling` | 4, the four breakout stubs, expected |
| Silkscreen warnings | 4 (`silk_overlap` 2, `silk_over_copper` 2): R2 and U2 reference text. Left for the GUI pass |
| Canary (`check_import.py`) | DRC 12 → 269 with the 3 mm rule, PASS |

**The 4 errors are inside the J1 footprint.** Rule `NPTH with copper around`
wants 0.20 mm. The shipped `USB_C_Receptacle_GCT_USB4110` footprint puts pads
A1/B12 (113.20, 107.355) 0.1944 mm from the NPTH peg at (112.89, 106.28), and
B1/A12 (106.80, 107.355) 0.1944 mm from the peg at (107.11, 106.28). No
routed copper is involved. Not fixed: the rule was not relaxed and the
footprint was not edited. Decide whether to accept it as a footprint waiver
(the drawing's land pattern) or scope the rule.

No copper-to-edge violation is reported on J1, though its courtyard runs to
y 99.495.

Interface nets to breakout, by segment count: `/USB_DM` 1 segment from U2.4;
`/USB_DP` 3 segments from U2.6; `/VBUS` reaches both row vias on B.Cu from the
y 117.0 bus. Host-side lengths U2 to row: DM 2.94 mm, DP 3.06 mm.

Not yet done: the zones in the saved file are unfilled (DRC refills them in
memory only). The heat/area check on the filled zone, `Host-Setup.md`, and the
fragment placement into `BlockBuilder/` remain.
