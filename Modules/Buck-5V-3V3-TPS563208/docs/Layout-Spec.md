# Layout Spec — Buck-5V-3V3-TPS563208

The geometry of the module reference board. Every number is a decision, and each
one carries its reason. **Draft.** No board exists yet. Nothing here is checked
by DRC.

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
| C100 | 10 µF 25 V X7R 0805 | input | DS §7.2.2.4 asks for "over 10 µF". At 5 V bias an 0805 keeps about 70 %. **Marginal. Consider 22 µF 1206.** |
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

A new placement that follows DS Figure 7-18.

| Ref | X | Y | Rot | Side | Reason |
|---|---|---|---|---|---|
| U8 | 111.000 | 106.000 | 0 | F | — |
| L30 | 104.950 | 106.000 | 180 | F | pad 1 (SW) at 107.70, 0.8 mm from U8.2 |
| C102 | 111.000 | 102.800 | 0 | F | pad 2 above U8.6 (VBST) |
| C101 | 109.860 | 109.300 | 270 | F | pad 1 under U8.3 (VIN) |
| C100 | 112.200 | 109.500 | 270 | F | beside C101, via lane between them |
| C103 | 102.200 | 112.000 | 270 | F | pad 1 under L30 pad 2 |
| C104 | 104.600 | 112.000 | 270 | F | beside C103 |
| R61 | 115.500 | 107.400 | 0 | F | pad 1 near U8.4 (VFB) |
| R60 | 115.500 | 109.200 | 180 | F | pad 2 on the VFB node |
| TP3 | 114.700 | 111.200 | 0 | F | VFB, beside R60 pad 2 |
| TP2 | 116.900 | 111.200 | 0 | F | +3V3 at the sense end |
| R62 | 107.400 | 111.300 | 0 | F | pad 1 on +3V3 |
| D22 | 109.300 | 113.600 | 90 | F | anode up, to R62 pad 2 |

The L30 courtyard is 7.43 x 6.86 mm (footprint `L_Coilcraft_XAL6030`). At this
position it spans x 101.24 to 108.67. U8's courtyard starts at 108.95.

The tightest courtyard pairs by hand arithmetic are C101 against U8 (0.07 mm)
and L30 against U8 (0.28 mm). Run `Modules/analysis/check_courtyards.py` to
confirm. Render the board and look at it.

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
