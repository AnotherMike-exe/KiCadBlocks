# Layout Spec — PowerMux-TPS2121

The geometry of the module reference board. Every number is a decision, and each
one carries its reason. The board is placed and routed. §3.2 and §11 hold the
state that DRC checked. §12 lists every change from the draft and why.
Sections 4 to 9 keep the draft reasoning. Where they disagree with §3.2 or §11,
§3.2 and §11 are right.

R70 is now 169 k on the board (§0.1 recommendation applied in the schematic).

Board: 15 x 20 mm, 4 layers, 1.6 mm. Written 2026-09-24.

Sources:

| Tag | Document |
|---|---|
| DS | TI TPS2120/TPS2121 datasheet, **SLVSEA3F**, Aug 2018, revised Aug 2020. `_resources/Research/TPS2121/tps2121.pdf` |
| REF | `_resources/Examples/Plum-RFBridge/Plum-RFBridge.kicad_pcb`, the routed parent board |
| BLK | `PlumBlocks.kicad_blocks/PowerMux-TPS2121.kicad_block/PowerMux-TPS2121.kicad_sch`, netlist exported 2026-09-24 |

---

## 0. Schematic findings — read before layout

### 0.1 The PR1 note and R70 disagree

The block note says "PoE wins while IN1 > 4.57 V (1.06 V / (51.1k/220.1k))".
The fitted R70 is 118 k. R70 + R71 = 169.1 k, not 220.1 k.

**The note is internally consistent with R70 = 169 k.** 220.1 k = 169 k +
51.1 k, and 51.1 x (4.57 / 1.06 − 1) = 169.2 k. 169 k is an E96 value. The
writer most likely confused R70 = 169 k with the divider total 169.1 k. REF
also fits 118 k, so the parent board carries the same value.

DS §7.5 gives the comparator reference: **VREF 1.06 V rising (1.01 to 1.10),
1.04 V falling (0.99 to 1.09)**, for PR1, CP2, OV1 and OV2 alike. The 1.19 V
figure in `docs/Power-Architecture.md` §3 is wrong.

| R70 | Ratio | IN1 rising, typ | IN1 falling, typ | Falling, full VREF range |
|---|---|---|---|---|
| 118 k (fitted) | 0.3022 | 3.51 V | **3.44 V** | 3.28 to 3.61 V |
| 169 k (note) | 0.2322 | 4.57 V | **4.48 V** | 4.26 to 4.69 V |

Below the threshold the part does not force IN2. It falls back to "highest
voltage wins" (DS §9.3, Table 9-2 text).

**Recommendation: change R70 to 169 k.** With 118 k, PoE keeps priority down to
3.44 V. The TPS563208 below the mux needs 4.5 V minimum (SLVSD90B §5.3). So a
sagging PoE source holds V5_SYS in a region where the buck is out of
specification, and USB never takes over. With 169 k the handover happens at
4.48 V, at the buck's floor. Worst case rising is 4.74 V, so a PoE source below
4.75 V may never regain priority. Check the Si3402 output tolerance before you
commit. **This is a schematic decision. Do not make it inside the layout.**

### 0.2 The OV thresholds

OV1 (R75/R76) and OV2 (R72/R73) are both 46.4 k / 10 k, ratio 0.1773.

| Item | Value | Source |
|---|---|---|
| OV trip, rising, typ | **5.98 V** | 1.06 / 0.1773, DS §7.5 |
| OV trip, full range | 5.70 to 6.20 V | 1.01 and 1.10 V |
| OV release, falling, typ | 5.87 V | 1.04 V |

`docs/Power-Architecture.md` §3 and §5 give 6.71 V and "about 6.7 V". Both come
from the wrong 1.19 V reference. USB PD vSafe5V reaches 5.5 V, so the minimum
trip of 5.70 V leaves 0.2 V.

### 0.3 The current limit

DS §9.3.2 Equation 2: ILM = 65.2 / RILM^0.861, RILM in kΩ.
R74 = 80.6 k gives **1.49 A typical**. DS §7.5 lists RILM = 80 k as 1.0 A min,
1.5 A typ, 2.0 A max. So the layout carries **1.5 A continuous, and 2.0 A
worst case** on POE_5V, VBUS and V5_SYS.

### 0.4 ST, pin 9, floats

DS Pin Functions: "Connect to GND if not required." BLK leaves it
`unconnected-(U10-ST-Pad9)`. ST is an output, so a float is harmless. The
layout keeps it unconnected. Record it as a deliberate deviation, or fix the
schematic first.

## 1. Outline and regions

| Item | X | Y |
|---|---|---|
| Board outline | 100.0 → 115.0 | 100.0 → 120.0 |
| Component region | 100.5 → 114.5 | 100.5 → 116.0 |
| Breakout row | 101.2 → 113.6 | 117.5 |

IN1 (POE_5V) sits on the west side of U10. IN2 (VBUS) sits on the east side.
The row keeps that order, so neither input crosses the other.

## 2. Pin map of U10

`Texas_VQFN-HR-12_2x2.5mm_P0.5mm`. **No exposed pad.** The footprint has 12
pads and nothing else. Heat leaves through the four power pads.

| Pad | Net | Local (x, y) | Size |
|---|---|---|---|
| 1 | V5_SYS (OUT) | −0.675, −0.35 | 1.05 x 0.40 |
| 2 | VBUS (IN2) | −0.675, 0.35 | 1.05 x 0.40 |
| 7 | POE_5V (IN1) | 0.675, 0.35 | 1.05 x 0.40 |
| 8 | V5_SYS (OUT) | 0.675, −0.35 | 1.05 x 0.40 |
| 3, 4, 5, 6 | CP2 (GND), OV2, OV1, PR1 | y 1.15 | 0.2 x 0.6 |
| 9, 10, 11, 12 | ST (nc), ILIM, SS, GND | y −1.15 | 0.2 x 0.6 |

At rotation 180 the inputs face north and the outputs face south. IN and OUT
on one side are 0.3 mm apart, edge to edge. **Each power pad must exit along its
long axis**, east or west. The control pins sit 0.3 mm beyond the OUT pads.

## 3. Placement

### 3.1 The parent board

From REF. U10 sits at (139.0, 101.0, 180) on F.Cu. Every part is on F.Cu.

| Ref | REF X | REF Y | Rot | dX from U10 | dY from U10 |
|---|---|---|---|---|---|
| U10 | 139.000 | 101.000 | 180 | 0 | 0 |
| C109 | 135.950 | 100.650 | 180 | −3.050 | −0.350 |
| C108 | 141.575 | 99.700 | 90 | +2.575 | −1.300 |
| C110 | 135.165 | 102.764 | 180 | −3.835 | +1.764 |
| C111 | 141.667 | 103.975 | 270 | +2.667 | +2.975 |
| C107 | 139.250 | 104.325 | 270 | +0.250 | +3.325 |
| R70 | 138.250 | 96.400 | 270 | −0.750 | −4.600 |
| R71 | 135.948 | 98.290 | 180 | −3.052 | −2.710 |
| R72 | 139.763 | 97.615 | 270 | +0.763 | −3.385 |
| R73 | 142.043 | 97.219 | 0 | +3.043 | −3.781 |
| R74 | 136.967 | 104.781 | 180 | −2.033 | +3.781 |
| R75 | 135.980 | 96.830 | 0 | −3.020 | −4.170 |
| R76 | 136.780 | 94.030 | 0 | −2.220 | −6.970 |
| TP1 | 138.970 | 110.160 | 0 | −0.030 | +9.160 |

This cluster is sound. C109 lines up with IN1 at y 100.65. C108 pad 1 lands on
IN2's row. C110 and C111 take one OUT pad each. Keep it.

### 3.2 The module

U10 stays at the draft point. The rest of the cluster is re-placed for a
single-layer (F.Cu) route of every net; the parent geometry needed three
vias on OV1 and crossed PR1 over OV1. See §12.

| Ref | X | Y | Rot | Side | Pads |
|---|---|---|---|---|---|
| U10 | 107.500 | 109.000 | 180 | F | 7 POE_5V and 8 V5_SYS exit west; 2 VBUS and 1 V5_SYS exit east |
| C109 | 105.100 | 107.875 | 90 | F | 1 POE_5V on the U10.7 row (105.1, 108.65); 2 GND north |
| C108 | 110.300 | 107.700 | 90 | F | 1 VBUS on the U10.2 row (110.3, 108.65); 2 GND north |
| C110 | 104.600 | 111.750 | 270 | F | 1 V5_SYS (104.6, 110.275); 2 GND south |
| C111 | 110.950 | 111.975 | 270 | F | 1 V5_SYS (110.95, 110.5); 2 GND south |
| C107 | 108.300 | 111.700 | 0 | F | 1 SS west, 2 GND east |
| R74 | 107.325 | 113.250 | 0 | F | 1 ILIM west, 2 GND east |
| R71 | 103.250 | 104.175 | 90 | F | 1 PR1 south, 2 GND north |
| R70 | 104.850 | 104.175 | 270 | F | 1 POE_5V north, 2 PR1 south |
| R75 | 106.450 | 104.175 | 270 | F | 1 POE_5V north, 2 OV1 south |
| R76 | 108.050 | 104.175 | 90 | F | 1 OV1 south, 2 GND north |
| R73 | 109.650 | 104.175 | 90 | F | 1 OV2 south, 2 GND north |
| R72 | 111.250 | 104.175 | 270 | F | 1 VBUS north, 2 OV2 south |
| TP1 | 107.400 | 115.200 | 0 | F | V5_SYS, straight above the middle V5_SYS row via |

The six divider resistors stand in one row at 1.6 mm pitch. Each divider node
is a pair of south pads joined by one track: PR1 (R71, R70), OV1 (R75, R76),
OV2 (R73, R72). The node order matches the pin order, west to east, so no
control track crosses another. `check_courtyards.py`: no overlaps; C107 to
C111 is 0.02 mm, the closest pair.

## 4. Copper on the parent board

From REF, segments by net. Widths in mm.

| Net | Widths used | Vias |
|---|---|---|
| POE_5V | 0.5 on F, B, In2 (68 mm); 0.4; 0.25; 0.1524 stub | 6 x 0.6/0.3 |
| VBUS | 0.6 on F and In1 (49 mm); 0.5; 0.4; 0.1524 x 10 at the pads | 0 |
| V5_SYS | 0.5 on F, B, In1 (44 mm); 0.1524 x 5 at the pads | 0 |
| MUX_PR1, OV1, OV2, ILIM, SS | 0.1524 | 3 on OV1 |

REF reaches the 0.4 mm pads with 0.1524 mm necks, then widens to 0.5 or 0.6.
REF has no zone on any of these nets.

## 5. Track widths and net classes

| Net | Class | Width | Reason |
|---|---|---|---|
| `/POE_5V`, `/VBUS`, `/V5_SYS` | Power_2 | 0.508 minimum, polygon where it fits | 1.5 A in IPC-2221, 1 oz outer, 10 °C rise, needs 0.53 mm |
| `/MUX_PR1`, `/MUX_OV1`, `/MUX_OV2` | Default | 0.2 | microamp divider currents, DS ILK 0.1 µA |
| `/MUX_ILIM`, `/MUX_SS` | Default | 0.2 | set-point nodes, keep them short |
| `GND` | — | pour | — |

**The pad neck.** A 0.4 mm pad takes a 0.4 mm neck at most. Widen to 0.508 or
to the polygon within 0.5 mm of the pad end. DS §12.1: "Use short wide traces
for input and output planes."

The brief gives Default 0.2. REF and the PoE modules use Default 0.1524. Pick
one in `Board-Setup.md` and write it once.

Net names carry the root prefix on this board: `/POE_5V`, `/VBUS`, `/V5_SYS`.
A pattern copied from REF (`/Power/...`) binds to nothing.

## 6. Zone plan

| Zone | Layer | Net | Rectangle or region | Priority |
|---|---|---|---|---|
| Ground plane | In1.Cu | `GND` | whole board | 0 |
| Output plane | In2.Cu | `/V5_SYS` | whole board | 0 |
| Top ground | F.Cu | `GND` | whole board | 0 |
| IN1 pad | F.Cu | `/POE_5V` | from U10.7 west end to C109.1 | 1 |
| IN2 pad | F.Cu | `/VBUS` | from U10.2 east end to C108.1 | 1 |
| OUT west | F.Cu | `/V5_SYS` | U10.8 west end to C110.1 | 1 |
| OUT east | F.Cu | `/V5_SYS` | U10.1 east end to C111.1 | 1 |
| Bottom ground | B.Cu | `GND` | whole board | 0 |
| IN1 feed | B.Cu | `/POE_5V` | 100.5, 104.0 → 103.8, 118.0 | 1 |
| IN2 feed | B.Cu | `/VBUS` | 111.1, 106.0 → 114.5, 118.0 | 1 |

**In2.Cu joins the two OUT pads.** Pads 1 and 8 sit on opposite sides of the
body, and the control pins block the path between them on F.Cu. The In2 plane
joins them with no crossing. It also feeds the three V5_SYS breakout vias.

**POE_5V and VBUS reach the edge on B.Cu strips.** In1 stays one solid GND
plane under the whole module.

Konnect `add_zone` writes nothing. Use `add_copper_pour` with KiCad closed, then
reload.

## 7. Vias at U10

DS §12.1: "For high current applications place vias under input and output
pins." A 0.6 mm via cannot sit inside a 0.4 mm pad, so the vias go in the
polygon, within 1.5 mm of the pad end.

| Polygon | Vias | Reaches |
|---|---|---|
| IN1 pad | 3 | B.Cu IN1 feed |
| IN2 pad | 3 | B.Cu IN2 feed |
| OUT west | 3 | In2 plane |
| OUT east | 3 | In2 plane |
| GND at U10.12 and U10.3 | 1 each | In1 plane |

**Why three.** A 0.3 mm drill with 20 µm plating has 0.0189 mm² of barrel. That
carries about 1.5 A at 10 °C rise as an outer conductor in IPC-2221, and about
0.75 A as an inner one. Two vias carry 1.5 A. The third covers the 2.0 A
current-limit ceiling and a thin barrel. Each via adds about 1.5 mΩ.

**Heat.** Worst case I² x RON = 1.5² x 0.100 Ω = 0.23 W (DS §7.5, RON max at
125 °C). At RθJA 72.2 °C/W (DS §7.4) the rise is 16 °C. No heat spreader is
needed. The vias above are for current, not for heat.

Via-to-via pitch inside one net is 1.0 mm. That gives 0.7 mm hole to hole,
above the 0.5 mm board rule.

## 8. Capacitors

DS §11: bypass capacitors "as close to the device as possible", X5R or X7R.

| Ref | Value | Net | Pad centre to U10 pad centre |
|---|---|---|---|
| C109 | 1 µF X7R 0603 | POE_5V | 1.6 mm, same row as U10.7 |
| C108 | 10 µF X7R 0805 | VBUS | 1.9 mm, pad 1 on U10.2's row |
| C110 | 47 µF X5R 1206 | V5_SYS | 2.2 mm from U10.8 |
| C111 | 47 µF X5R 1206 | V5_SYS | 2.3 mm from U10.1 |
| C107 | 100 nF | SS | 1.4 mm from U10.11 |

Each capacitor ground pad takes one GND via to In1, within 0.5 mm of the pad.

## 9. The breakout row

Row at **y = 117.5**. Each via carries a 1.0 mm stub on the layer opposite its
arrival, ending at y 118.5. Via 0.6 mm pad on 0.3 mm drill.

| x | Net | Direction | Arrives on | Stub layer |
|---|---|---|---|---|
| 101.2 | `/POE_5V` | in | B.Cu | F.Cu |
| 102.2 | `/POE_5V` | in | B.Cu | F.Cu |
| 103.2 | `/POE_5V` | in | B.Cu | F.Cu |
| 104.8 | `GND` | stitch | pour | both |
| 106.4 | `/V5_SYS` | out | In2.Cu | F.Cu |
| 107.4 | `/V5_SYS` | out | In2.Cu | F.Cu |
| 108.4 | `/V5_SYS` | out | In2.Cu | F.Cu |
| 110.0 | `GND` | stitch | pour | both |
| 111.6 | `/VBUS` | in | B.Cu | F.Cu |
| 112.6 | `/VBUS` | in | B.Cu | F.Cu |
| 113.6 | `/VBUS` | in | B.Cu | F.Cu |

Groups are 1.6 mm apart. Vias inside one group are 1.0 mm apart. **The GND
vias sit between the power groups, not at 3.0 mm pitch.** A 15 mm edge cannot
hold three 3-via groups and a 3.0 mm GND run. A GND via next to each group
gives that group a short return, which matters more here.

The control nets do not break out. PR1, OV1, OV2, ILIM and SS stay inside the
block.

## 10. Checks before you believe a number

1. Refill the zones. `kicad-cli pcb drc --refill-zones` refills in memory only.
2. Confirm the net classes bind in the net inspector.
3. State a non-zero canary: append a 3 mm clearance rule, re-run DRC, confirm
   the count explodes, restore, diff.
4. Count segments on every interface net to its breakout via. DRC hides a
   single-pad net.
5. Render the board and look at it.

## 11. Closing state

Measured 2026-09-24 with `kicad-cli pcb drc --severity-all --schematic-parity
--refill-zones`.

| Item | Count |
|---|---|
| Errors | 0 |
| Unconnected | 0 |
| Schematic parity | 0 |
| `track_dangling` | 9, the nine power stubs |
| `lib_footprint_mismatch` | 1, U10 differs from `Package_DFN_QFN` in the library. Came with the footprint; not a layout change |
| Silkscreen warnings | 47, left for the GUI silk pass: 25 `silk_overlap`, 22 `silk_over_copper` |
| Canary (`check_import.py`) | 57 to 417, PASS |

Copper: 72 segments (63 F.Cu, 9 B.Cu), 26 vias, all vias 0.6/0.3. No
track is on In1.Cu or In2.Cu.

| Net | F.Cu segments | B.Cu segments | Vias |
|---|---|---|---|
| `/POE_5V` | 10 (U10.7 neck 0.4, 0.6 to C109.1, 0.8 trunk y 108.65 and x 102.2 to the row; row link 0.6; 0.3 divider feed to R70.1 and R75.1 round the west and north edge) | 3 (stubs) | 3 |
| `/VBUS` | 8 (U10.2 neck 0.4, 0.6 to C108.1, 0.8 trunk y 108.65 and x 113.6 to the row; row link 0.6; 0.3 divider feed to R72.1 up x 113.6) | 3 (stubs) | 3 |
| `/V5_SYS` | 15 (U10.8 neck 0.4 to C110.1 and a 3-via column at x 103.2; U10.1 neck 0.4 to C111.1 and a 3-via column at x 112.4; all 0.6 past the necks; TP1 to the row, row link) | 3 (stubs) | 9 |
| `/MUX_PR1`, `/MUX_OV1`, `/MUX_OV2` | 4, 3, 5 (0.2 mm) | 0 | 0 |
| `/MUX_ILIM`, `/MUX_SS` | 3, 2 (0.2 mm) | 0 | 0 |
| `GND` | 13 (pad to via) | 0 | 11 |

Power widths: the 0.4 mm pads limit the neck to 0.4 mm for 0.7 to 0.8 mm. The
track widens to 0.6 mm where the IN and OUT tracks on one side part, and to
0.8 mm past the input capacitor.

Interface arrival, counted by segment:

- `/POE_5V`: U10.7 to the via at 102.2, 117.5 in 4 segments (0.4, 0.6, 0.8,
  0.8), then 1 row segment each to 101.2 and 103.2.
- `/VBUS`: U10.2 to the via at 113.6, 117.5 in 4 segments (0.4, 0.6, 0.8,
  0.8), then 1 row segment each to 112.6 and 111.6.
- `/V5_SYS`: the two OUT pads reach In2.Cu through 3 vias each (x 103.2 and
  x 112.4). In2.Cu joins them to the three row vias. TP1 joins the row on F.Cu
  in 1 segment, then 1 row segment each to 106.4 and 108.4. DRC reports 0
  unconnected with the zones refilled, so the In2 path is complete.
- `GND`: the two row vias join the F.Cu, In1.Cu and B.Cu pours.

Breakout row, y 117.5. F.Fab labels at y 116.3, size 0.7, rotation 90.

| x | Net | Arrives on | Stub | Stub end |
|---|---|---|---|---|
| 101.2 | `/POE_5V` | F.Cu row link | B.Cu, 1.0 mm | 101.2, 118.5 |
| 102.2 | `/POE_5V` | F.Cu trunk | B.Cu, 1.0 mm | 102.2, 118.5 |
| 103.2 | `/POE_5V` | F.Cu row link | B.Cu, 1.0 mm | 103.2, 118.5 |
| 104.8 | `GND` | pours, In1 | — | — |
| 106.4 | `/V5_SYS` | F.Cu row link, In2.Cu plane | B.Cu, 1.0 mm | 106.4, 118.5 |
| 107.4 | `/V5_SYS` | F.Cu from TP1, In2.Cu plane | B.Cu, 1.0 mm | 107.4, 118.5 |
| 108.4 | `/V5_SYS` | F.Cu row link, In2.Cu plane | B.Cu, 1.0 mm | 108.4, 118.5 |
| 110.0 | `GND` | pours, In1 | — | — |
| 111.6 | `/VBUS` | F.Cu row link | B.Cu, 1.0 mm | 111.6, 118.5 |
| 112.6 | `/VBUS` | F.Cu row link | B.Cu, 1.0 mm | 112.6, 118.5 |
| 113.6 | `/VBUS` | F.Cu trunk | B.Cu, 1.0 mm | 113.6, 118.5 |

Open:

1. Silkscreen pass in the GUI. The value texts on F.Fab also crowd the render.
2. The F.Fab labels are centred 1.2 mm inboard and reach over their vias, as on
   the Buck board. F.Fab only.
3. U10.9 (ST) stays unconnected (§0.4).
4. The `/V5_SYS` current from U10 to the row goes through In2.Cu only (3 vias
   down on each side, 3 up at the row). There is no F.Cu path past C107 and
   R74.
5. The zones in the file are not refilled. DRC refills in memory. Refill in
   the GUI before a fab export.

## 12. Changes from the draft

| Item | Draft | Board | Why |
|---|---|---|---|
| Divider row R70 to R76 | The parent cluster: mixed rotations from y 102.0 to 106.4 | One row of six vertical 0603 at y 104.175, x 103.25 to 111.25, 1.6 mm pitch | The parent order crosses OV1 over PR1 and needs vias. In the new order each divider node sits over its U10 pin, so PR1 goes west, OV1 straight north and OV2 east, all on F.Cu at 0.2 mm. |
| C109 | 104.45, 108.65, rot 180 | 105.1, 107.875, rot 90 | At rot 180 its GND pad sits on the POE_5V line and blocks the trunk to the west. Rotated, pad 1 sits on the line and the trunk passes it. |
| C108 | 110.075, 107.7 | 110.3, 107.7 | Clears the OV2 track at y 106.1. |
| C110 | 103.665, 110.764, rot 180 | 104.6, 111.75, rot 270 | At rot 180 it lies across the POE_5V trunk at x 102.2. Vertical, it leaves the west strip to POE_5V. |
| C111 | 110.167, 111.975 | 110.95, 111.975 | Clears the courtyard of C107. |
| C107 | 107.75, 112.325, rot 270 | 108.3, 111.7, rot 0 | Pad 2 takes the U10.12 GND track, and the ILIM track passes west of pad 1. |
| R74 | 105.467, 112.781, rot 180 | 107.325, 113.25, rot 0 | Under C107. The draft spot is inside C110's courtyard. ILIM goes straight down x 106.5 to pad 1. |
| TP1 | 107.5, 115.0 | 107.4, 115.2 | Straight above the middle V5_SYS row via. |
| Priority polygons and B.Cu feeds (§6) | 4 F.Cu and 2 B.Cu | none | Not on the board. Power_2 tracks replace them: 0.4 mm necks at the U10 pads, then 0.6 and 0.8 mm. |
| POE_5V and VBUS arrival | B.Cu feeds, stubs on F.Cu | F.Cu trunks at x 102.2 and x 113.6, stubs on B.Cu | A straight F.Cu trunk with no layer change before the row. The 3 row vias are the only layer change. |
| V5_SYS arrival | In2.Cu, stubs on F.Cu | In2.Cu plus a F.Cu row link from TP1, stubs on B.Cu | The row link is on F.Cu, so the stubs go to the opposite layer. |
| U10 power vias | 3 per pad polygon, 12 in total | 3 per OUT pad, at x 103.2 and 112.4, beside C110.1 and C111.1 | The inputs have no layer change near U10. No via fits within 1.5 mm of a 0.4 mm pad without crowding the control pins. |
| Divider feeds | from the parent board | 0.3 mm F.Cu from the input trunks | POE_5V round the west and north edges to R70.1 and R75.1; VBUS up x 113.6 to R72.1. No via. |
| GND vias | at U10.12, U10.3 and each capacitor | 11: U10.3 (109.0, 107.3), U10.12 by C107.2 (109.2, 112.6), C108.2, C109.2, C110.2, C111.2, R71.2, R76.2, R73.2, 2 on the row | The U10.12 track ends at C107.2 and shares its via. |

