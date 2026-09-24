# Layout Spec — USBC-Device-ESD

DRAFT. The geometry of the module reference board, written before the board
exists. Every number is a decision, and each one carries its reason.

Board: 20 x 21 mm, 4 layers, 1.6 mm, PCBWay. Written 2026-09-24.

Nothing here is measured yet. Re-derive every figure from the files after
placement. Run ERC, DRC with `--refill-zones`, and a canary first.

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

Carried over from `Plum-RFBridge`. J1 moves from (151.15, 54.25) to
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

Courtyard gaps, computed: R2 to U2 0.47 mm, R1 to U2 0.22 mm. Confirm with
`Modules/analysis/check_courtyards.py` after placement.

## 5. Routing

### 5.1 The data pair bridge

Translated from `Plum-RFBridge`, with two changes.

| Step | Net | Geometry |
|---|---|---|
| 1 | D− | F.Cu stubs straight down from B7 and A7 to vias at y **108.60** |
| 2 | D− | B.Cu bridge between the two D− vias at y 108.60 |
| 3 | D+ | F.Cu stubs straight down from B6 and A6 to vias at y **109.65** |
| 4 | D+ | B.Cu bridge between the two D+ vias at y 109.65, on to a via at (111.575, 110.90) |
| 5 | D+ | F.Cu from (111.575, 110.90) to U2.1 |
| 6 | D− | F.Cu from the B7 via down to U2.3 |

**Change 1: the vias are 0.6 / 0.3, not 0.52 / 0.3.** The house via is 0.6.
The two via rows sit 1.05 mm apart in y and 0.5 mm apart in x, which leaves
0.56 mm of copper between a D− via and a D+ via.

**Change 2: the D− via row moves from 1.02 mm to 1.245 mm below the pad
centres.** At RFBridge's offset a 0.6 mm via sits 0.15 mm from the corner of
the neighbouring 0.30 mm pad of the other net. The netclass wants 0.20. At
y 108.60 the gap is 0.37 mm. The D+ row moves by the same 0.225 mm.

**Pad escapes are 0.20 mm, not RFBridge's 0.1016.** A 0.20 mm trace on a pad
centre at 0.5 mm pitch clears the neighbouring 0.30 mm pad by 0.25 mm.

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

`/VBUS` leaves J1.A9/B4 and J1.A4/B9 on F.Cu, joins on B.Cu through two vias
beside the connector, and runs B.Cu to the breakout. U2.5 takes a 0.20 mm
tap. Pin 5 is a reference, not a supply path.

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

| x | Net | Direction | Arrives on | Stub layer |
|---|---|---|---|---|
| 102.2 | `GND` | stitch | pour | both |
| 105.2 | `GND` | stitch | pour | both |
| 108.8 | `/VBUS` | out | B.Cu | F.Cu |
| 110.4 | `/USB_DM` | both | F.Cu | B.Cu |
| 112.0 | `/USB_DP` | both | F.Cu | B.Cu |
| 115.2 | `GND` | stitch | pour | both |
| 118.2 | `GND` | stitch | pour | both |

`/USB_DM` drops straight from U2.4 at x 110.4. `/USB_DP` jogs 0.3 mm west
from U2.6 at x 112.3. The pair stays a pair to the row.

**A differential pair crosses this block boundary.** That differs from the
PoE module. The host must continue the pair at 0.20 / 0.20 over GND to its
MCU.

**One `/VBUS` via is marginal.** A 0.3 mm plated via carries roughly 1 A.
Add a second `/VBUS` via beside the first, off-grid, if the host draws more.

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
