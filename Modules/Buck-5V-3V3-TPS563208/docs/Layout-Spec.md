# Layout Spec — Buck-5V-3V3-TPS563208

The geometry of the module reference board. Every number is a decision, and each
one carries its reason. The board is placed and routed. §3.2 and §11 hold the
state that DRC checked. §12 lists every change from the draft and why.
Sections 4 to 9 keep the draft reasoning. Where they disagree with §3.2 or §11,
§3.2 and §11 are right.

Board: 18 x 20 mm, 4 layers, 1.6 mm. Written 2026-09-24.

Sources:

| Tag | Document |
|---|---|
| DS | TI TPS563201/TPS563208 datasheet, **SLVSD90B**, Dec 2015, revised Sep 2024. `_resources/Research/TPS563208/tps563208.pdf`. One document covers both parts. |
| REF | `_resources/Examples/Plum-RFBridge/Plum-RFBridge.kicad_pcb`, the routed parent board |
| BLK | `PlumBlocks.kicad_blocks/Buck-5V-3V3-TPS563208.kicad_block/Buck-5V-3V3-TPS563208.kicad_sch`, netlist exported 2026-09-24 |

---

## 0. Schematic findings

### 0.1 The output voltage

DS §7.2.2.2 Equation 2: VOUT = 0.768 x (1 + R1/R2). R60 = 33 k, R61 = 10 k.

| Item | Value | Source |
|---|---|---|
| VOUT, typ | **3.302 V** | 0.768 x 4.3 |
| VOUT, full VFB range | 3.22 to 3.38 V | VFBTH 749 to 787 mV, DS §5.5 |
| TI's value for 3.3 V | R1 33.2 k, 3.318 V | DS Table 7-2 |

33 k is correct. The 16 mV difference from 33.2 k is inside the 2 % VFB spread.

### 0.2 TPS563201 in the note, TPS563208 fitted

The note says "TPS563201". U8 is TPS563208DDCR. **The reference is the same.**
DS §5.5 gives one VFBTH, 768 mV typ in continuous mode, for both parts. The
TPS563201 runs Eco-mode, a pulse-skip mode at light load, where DS gives 774 mV
typ. The TPS563208 runs forced PWM (FCCM) at every load. The divider and the
equation do not change. **Only the note's part name is wrong.** Fix the text.

### 0.3 The fitted passives

The brief listed C100 to C104 as 22 µF 1206. BLK says otherwise:

| Ref | Value | Role | DS check |
|---|---|---|---|
| C100 | 22 µF 1206 (was 10 µF 25 V X7R 0805 in the draft) | input | DS §7.2.2.4 asks for "over 10 µF". The 0805 was marginal after bias derating. The board now carries 22 µF 1206. |
| C101 | 100 nF 0603 | input HF | DS §7.2.2.4, optional C3 |
| C102 | 100 nF 0603 | VBST to SW | DS §7.2.2.5, 0.1 µF required |
| C103, C104 | 22 µF 16 V X5R 1206 | output | DS Table 7-2, 20 to 68 µF. 44 µF nominal passes after bias derating. |
| L30 | 3.3 µH XAL6030 | output | DS Table 7-2, 2.2 to 4.7 µH for 3.3 V |

EN (pin 5) ties to V5_SYS. DS pin table: "must be pulled up". That is correct.

### 0.4 The input floor

DS §5.3: VIN minimum 4.5 V. DS §7.3: VIN minimum is VOUT / 0.75 = 4.4 V. The
mux above this block holds PoE priority down to 3.44 V with the fitted R70. See
`Modules/PowerMux-TPS2121/docs/Layout-Spec.md` §0.1.

## 1. Outline and regions

| Item | X | Y |
|---|---|---|
| Board outline | 100.0 → 118.0 | 100.0 → 120.0 |
| Power stage | 100.5 → 113.5 | 100.5 → 115.5 |
| Feedback corner | 113.5 → 117.5 | 105.0 → 112.0 |
| Breakout row | 101.2 → 116.0 | 117.5 |

The inductor sits west of U8. The feedback network sits east of U8. SW never
reaches the east side, so the feedback nodes stay away from it (DS §7.4.1
item 8).

## 2. Pin map of U8

SOT-23-6 at rotation 0. Pin 1 top left.

| Pin | Net | Side |
|---|---|---|
| 1 | GND | west, top |
| 2 | `/SW_NODE` | west, middle |
| 3 | `/V5_SYS` (VIN) | west, bottom |
| 4 | `/VFB_33` | east, bottom |
| 5 | `/V5_SYS` (EN) | east, middle |
| 6 | `/VBST` | east, top |

SW sits between GND and VIN on one side. So VIN escapes south, GND escapes
north, and SW goes straight west to L30.

## 3. Placement

### 3.1 The parent board

From REF. U8 sits at (134.0, 112.0, 0) on F.Cu. Every part is on F.Cu.

| Ref | REF X | REF Y | Rot | dX from U8 | dY from U8 |
|---|---|---|---|---|---|
| U8 | 134.000 | 112.000 | 0 | 0 | 0 |
| C100 | 132.237 | 108.455 | 90 | −1.763 | −3.545 |
| C101 | 131.150 | 112.175 | 90 | −2.850 | +0.175 |
| C102 | 136.190 | 109.474 | 180 | +2.190 | −2.526 |
| L30 | 132.800 | 118.000 | 270 | −1.200 | +6.000 |
| C103 | 133.000 | 124.125 | 270 | −1.000 | +12.125 |
| C104 | 130.625 | 124.218 | 270 | −3.375 | +12.218 |
| R60 | 137.662 | 112.950 | 180 | +3.662 | +0.950 |
| R61 | 137.384 | 115.279 | 270 | +3.384 | +3.279 |
| R62 | 137.960 | 121.145 | 0 | +3.960 | +9.145 |
| D22 | 140.972 | 121.145 | 180 | +6.972 | +9.145 |
| TP2 | 138.710 | 87.110 | 0 | +4.710 | −24.890 |
| TP3 | 139.540 | 115.090 | 0 | +5.540 | +3.090 |

**Do not copy this cluster.** Three things break DS §7.4.1:

1. C100, the 10 µF input capacitor, sits 3.5 mm from VIN on the GND side of
   the package. Item 2 asks for it close to the device.
2. C103 and C104 sit 12 mm below U8. Item 10 asks for a short, wide GND path
   between the output capacitors and the GND pin.
3. `SW_NODE` runs at 0.1524 mm for 6.4 mm on F.Cu and 2.8 mm on B.Cu. Item 4
   asks for a short, wide SW trace.

C101 is the one good placement. Its pad 1 lines up with VIN.

### 3.2 The module

The placement on the board, read back from the saved file. It follows DS
Figure 7-18. Every part is on F.Cu.

| Ref | X | Y | Rot | Reason |
|---|---|---|---|---|
| U8 | 111.000 | 106.000 | 0 | — |
| L30 | 104.950 | 106.000 | 180 | pad 1 (SW) at 107.70, 0.79 mm pad gap to U8.2 |
| C102 | 111.000 | 102.900 | 0 | pad 2 (VBST) above U8.6; pad 1 (SW) reaches L30.1 over the top |
| C101 | 109.8625 | 109.400 | 270 | pad 1 straight under U8.3 (VIN) on the same x |
| C100 | 111.900 | 110.100 | 270 | 22 µF 1206; pad 1 level with C101.1 at y 108.625 |
| C103 | 103.675 | 110.800 | 0 | pad 1 (+3V3) on the x 102.2 trunk under L30.2; pad 2 (GND) east |
| C104 | 103.675 | 113.400 | 0 | stacked under C103, same trunk |
| R61 | 115.600 | 106.950 | 0 | pad 1 (VFB) level with U8.4 |
| R60 | 115.600 | 108.800 | 180 | pad 2 (VFB) under R61.1 |
| TP3 | 114.775 | 105.100 | 0 | VFB, north end of the VFB column |
| TP2 | 116.425 | 110.600 | 0 | +3V3 on the sense line, under R60.1 |
| R62 | 103.025 | 101.500 | 0 | pad 1 (+3V3) above L30.2 |
| D22 | 106.100 | 101.500 | 180 | anode west to R62.2, cathode to a GND via |

`check_courtyards.py`: no overlap, no gap under 0.05 mm, nothing off the board.

## 4. Copper on the parent board

From REF, segments by net. Widths in mm.

| Net | Widths used |
|---|---|
| SW_NODE | 0.1524 only (8 on F.Cu, 1 on B.Cu) |
| VBST | 0.1524 |
| VFB_33 | 0.1524, 7 segments |
| V5_SYS | 0.5 on F, B, In1; 0.1524 at pads |
| +3V3 | 0.1524 to 2.0; an In2.Cu +3V3 plane covers the board |
| LED_PWR_A | 0.1524 |

## 5. Track widths and net classes

| Net | Class | Width | Reason |
|---|---|---|---|
| `/SW_NODE` | polygon | 0.6 x 0.8 mm strip, U8.2 to L30.1 | DS item 4. The strip is as wide as the pin and as short as the courtyards allow. |
| `/SW_NODE` to C102 | Power_1 | 0.3048 | gate-drive charge only |
| `/VBST` | Power_1 | 0.3048 | gate-drive charge only |
| `/V5_SYS` | polygon, then Power_2 | 0.508 minimum | 1.47 A max input: 2 A at 3.3 V over 90 % efficiency |
| `+3V3` | polygon, then Power_2 | 0.508 minimum | up to 2 A out, limited by the 1.5 A mux above |
| `/VFB_33` | Default | 0.2 | DS item 9: as small as possible |
| Sense, R60.1 to C104.1 | Default | 0.2 | DS item 6: a separate VOUT path |
| `/LED_PWR_A` | Default | 0.2 | 4 mA |

The brief gives Default 0.2. REF and the PoE modules use Default 0.1524. Pick
one in `Board-Setup.md` and write it once.

## 6. Zone plan

| Zone | Layer | Net | Region | Priority |
|---|---|---|---|---|
| Ground plane | In1.Cu | `GND` | whole board | 0 |
| Input plane | In2.Cu | `/V5_SYS` | whole board | 0 |
| Top ground | F.Cu | `GND` | whole board | 0 |
| SW strip | F.Cu | `/SW_NODE` | 108.4, 105.7 → 109.2, 106.3 plus L30 pad 1 | 1 |
| Input | F.Cu | `/V5_SYS` | U8.3, C101.1, C100.1: 109.2, 107.3 → 112.9, 110.1, minus the GND pads | 1 |
| Output | F.Cu | `+3V3` | L30 pad 2 to C103.1 and C104.1: 100.8, 103.4 → 105.6, 111.2 | 1 |
| Bottom ground | B.Cu | `GND` | whole board | 0 |
| Output feed | B.Cu | `+3V3` | 100.5, 108.5 → 103.8, 118.0 | 1 |

**SW stays on F.Cu and stays small.** DS Figure 7-18 shows a SW pour on an
inner or bottom layer. This board does not use one. In1 must stay a whole GND
plane, and SW copper on In2 would couple into the input plane. The F.Cu strip
is 0.8 mm long, which gives the smallest radiating area.

**In2 carries V5_SYS.** EN reaches it through one via at (113.7, 106.0). The
input polygon reaches it through the vias of §7. The breakout vias land on it.

## 7. Vias

| Location | Count | Net | Reason |
|---|---|---|---|
| Input polygon, x 110.9, y 107.9 / 108.9 / 109.9 | 3 | `/V5_SYS` | DS item 3. 1.47 A needs two; the third is margin. |
| U8.1, at (109.86, 104.0) | 1 | GND | the GND pin's return to In1 |
| C101.2, C100.2 | 1 each | GND | DS item 3, input loop return |
| C103.2, C104.2 | 2 each | GND | DS item 10, output return |
| Output polygon, y 109.2 between L30 and C103 | 3 | `+3V3` | to the B.Cu output feed |
| EN, at (113.7, 106.0) | 1 | `/V5_SYS` | EN to the In2 plane |
| R61.2 | 1 | GND | see below |
| R60.1 and the sense end | 1 each | `+3V3` | sense on B.Cu |

**Why three on a power net.** A 0.3 mm drill with 20 µm plating has 0.0189 mm²
of barrel. That carries about 1.5 A at 10 °C rise as an outer conductor in
IPC-2221, and about 0.75 A as an inner one. Two carry the load. The third
covers a thin barrel.

**No via lands under U8 except the V5_SYS lane and the GND via.** DS item 5:
switching current must not flow under the device.

**The Kelvin return is open.** DS item 7 asks for a Kelvin connection from the
feedback GND to U8.1. R61.2 sits 6.5 mm east of U8.1 and the VBST trace lies
between them. This draft returns R61.2 through In1. The routing session decides
whether a dedicated trace fits.

## 8. Heat

U8: RθJA 92.6 °C/W (DS §5.4). At 2 A and 90 % the loss is about 0.7 W total,
with part of it in L30. Assume 0.5 W in U8. The rise is then 46 °C. The GND
pour on F.Cu and the In1 plane are the heat path. **Measure this on the filled
zone before you sign it off.**

## 9. The breakout row

Row at **y = 117.5**. Each via carries a 1.0 mm stub on the layer opposite its
arrival, ending at y 118.5. Via 0.6 mm pad on 0.3 mm drill.

| x | Net | Direction | Arrives on | Stub layer |
|---|---|---|---|---|
| 101.2 | `+3V3` | out | B.Cu | F.Cu |
| 102.2 | `+3V3` | out | B.Cu | F.Cu |
| 103.2 | `+3V3` | out | B.Cu | F.Cu |
| 104.8 | `GND` | stitch | pour | both |
| 107.8 | `GND` | stitch | pour | both |
| 110.8 | `GND` | stitch | pour | both |
| 112.4 | `/V5_SYS` | in | In2.Cu | F.Cu |
| 113.4 | `/V5_SYS` | in | In2.Cu | F.Cu |
| 114.4 | `/V5_SYS` | in | In2.Cu | F.Cu |
| 116.0 | `GND` | stitch | pour | both |

GND pitch is 3.0 mm in the middle run. Each power group is 1.6 mm from the
next via. Vias inside one group are 1.0 mm apart, which gives 0.7 mm hole to
hole, above the 0.5 mm board rule.

`+3V3` breaks out west, under the output capacitors. `/V5_SYS` breaks out east,
under the input capacitors. Neither crosses the other.

`/SW_NODE`, `/VBST`, `/VFB_33` and `/LED_PWR_A` stay inside the block.

## 10. Checks before you believe a number

1. Refill the zones. `kicad-cli pcb drc --refill-zones` refills in memory only.
2. Confirm the net classes bind in the net inspector. Net names on this board
   are `/SW_NODE`, `/V5_SYS`, `/VFB_33`, `/VBST`, and the global `+3V3`.
3. State a non-zero canary: append a 3 mm clearance rule, re-run DRC, confirm
   the count explodes, restore, diff.
4. Count segments on every interface net to its breakout via.
5. Render the board and look at it. Check that no SW copper runs east of U8.

## 11. Closing state

Measured 2026-09-24 with `kicad-cli pcb drc --severity-all --schematic-parity
--refill-zones`.

| Item | Count |
|---|---|
| Errors | 0 |
| Unconnected | 0 |
| Schematic parity | 0 |
| `track_dangling` | 6, the six power stubs |
| Silkscreen warnings | 29, left for the GUI silk pass: 16 `silk_overlap`, 12 `silk_over_copper`, 1 `silk_edge_clearance` (R62 reference at the top edge) |
| Canary (`check_import.py`) | 35 to 182, PASS |

Copper: 42 segments, 24 vias, all vias 0.6/0.3.

| Net | F.Cu segments | B.Cu segments | Vias |
|---|---|---|---|
| `/SW_NODE` | 3 (0.6 mm strip U8.2 to L30.1; 0.3 mm C102.1 to L30.1) | 0 | 0 |
| `/VBST` | 2 (0.3 mm) | 0 | 0 |
| `/V5_SYS` | 8 (U8.3 to C101.1 to C100.1, 0.8 mm; column x 113.4 to the row, 0.6 mm; row link; EN) | 3 (stubs) | 6 |
| `+3V3` | 9 (trunk x 102.2 L30.2 to the row, 0.8 mm; row link; R62 feed; sense R60.1 to TP2 to via) | 4 (3 stubs; sense line y 112.1, 0.2 mm) | 5 |
| `/VFB_33` | 3 (0.2 mm) | 0 | 0 |
| `/LED_PWR_A` | 1 | 0 | 0 |
| `GND` | 9 (pad to via) | 0 | 13 |

Interface arrival, counted by segment:

- `+3V3`: L30.2 to the via at 102.2, 117.5 in 4 trunk segments, then 1 row
  segment each to 101.2 and 103.2.
- `/V5_SYS`: C100.1 to the via at 113.4, 117.5 in 3 segments, then 1 row
  segment each to 112.4 and 114.4. The In2.Cu plane joins all six V5_SYS vias
  as a second path.
- `GND`: the four row vias join the F.Cu, In1.Cu and B.Cu pours.

Breakout row, y 117.5. F.Fab labels at y 116.3, size 0.7, rotation 90.

| x | Net | Arrives on | Stub | Stub end |
|---|---|---|---|---|
| 101.2 | `+3V3` | F.Cu row link | B.Cu, 1.0 mm | 101.2, 118.5 |
| 102.2 | `+3V3` | F.Cu trunk | B.Cu, 1.0 mm | 102.2, 118.5 |
| 103.2 | `+3V3` | F.Cu row link | B.Cu, 1.0 mm | 103.2, 118.5 |
| 104.8 | `GND` | pours, In1 | — | — |
| 107.8 | `GND` | pours, In1 | — | — |
| 110.8 | `GND` | pours, In1 | — | — |
| 112.4 | `/V5_SYS` | F.Cu row link, In2.Cu plane | B.Cu, 1.0 mm | 112.4, 118.5 |
| 113.4 | `/V5_SYS` | F.Cu column, In2.Cu plane | B.Cu, 1.0 mm | 113.4, 118.5 |
| 114.4 | `/V5_SYS` | F.Cu row link, In2.Cu plane | B.Cu, 1.0 mm | 114.4, 118.5 |
| 116.0 | `GND` | pours, In1 | — | — |

Open:

1. Silkscreen pass in the GUI.
2. The V5_SYS labels are 2.2 mm long and centred 1.2 mm inboard, so they reach
   over their vias. F.Fab only.
3. Kelvin return (DS item 7): R61.2 returns through its own via at 116.425,
   105.9 to In1. There is no dedicated trace to U8.1.
4. Heat (§8) is not yet measured on the filled zone.

## 12. Changes from the draft

| Item | Draft | Board | Why |
|---|---|---|---|
| C100 | 10 µF 0805 at 112.2, 109.5 | 22 µF 1206 at 111.9, 110.1 | The part changed. The 1206 courtyard (2.3 x 4.6 mm rotated) must clear U8's courtyard (y 107.7). Pad 1 now sits level with C101.1. |
| C101 | 109.86, 109.3 | 109.8625, 109.4 | Pad 1 on the exact x of U8.3; 0.1 mm down for courtyard margin. |
| C102 | y 102.8 | y 102.9 | Clears the U8.1 GND via. C102.1 joins SW at the top of L30.1, not in the gap beside U8.1, which is too narrow for a track at 0.2 mm pad clearance. |
| C103, C104 | rot 270, side by side at y 112.0 | rot 0, stacked at x 103.675, y 110.8 and 113.4 | Both +3V3 pads sit on one straight 0.8 mm trunk from L30.2 to the breakout. Both GND pads face east with two vias each. |
| R60, R61 | 115.5, 109.2 and 115.5, 107.4 | 115.6, 108.8 and 115.6, 106.95 | R61.1 level with U8.4, so the VFB node is straight. 0.1 mm east to clear the V5_SYS vias at x 113.4. |
| TP3 | 114.7, 111.2 | 114.775, 105.1 | North end of the VFB column. The draft spot is on the V5_SYS column and the sense line. |
| TP2 | 116.9, 111.2 | 116.425, 110.6 | On the straight sense line under R60.1. |
| R62, D22 | 107.4, 111.3 and 109.3, 113.6 rot 90 | 103.025, 101.5 and 106.1, 101.5 rot 180 | The top strip above L30 is free. R62.1 feeds straight from L30.2. The south area stays clear for the V5_SYS column and the sense line. |
| Priority polygons (§6) | SW strip, input, output, output feed | none | Not on the board. Short wide tracks replace them: SW 0.6 mm x 2.2 mm, V5_SYS and +3V3 0.8 mm. |
| V5_SYS input vias | 3 at x 110.9 | 2 at 113.4, 108.625 and 109.625, plus a direct F.Cu column to the row | No room for a via lane between C101 and the larger C100. The column carries the current to the row on F.Cu; In2 is the second path. |
| EN via | 113.7, 106.0 | 113.4, 106.0 | Clearance to TP3 and R61.1. |
| U8.1 GND via | 109.86, 104.0 | 109.8625, 104.1 | Clearance to the C102.1 SW track at y 102.9. |
| +3V3 path | B.Cu output feed, arrives B.Cu | F.Cu trunk, arrives F.Cu, stubs on B.Cu | One straight trunk. No output polygon exists. |
| V5_SYS arrival | In2.Cu, stubs on F.Cu | F.Cu column and In2.Cu, stubs on B.Cu | The F.Cu column exists, so the stubs go to the opposite layer. |
| Sense line | B.Cu from R60.1 | R60.1 to TP2 to via on F.Cu, B.Cu 0.2 mm at y 112.1 to a via on the trunk between C103.1 and C104.1 | DS item 6: a separate VOUT path from the output capacitors. |
