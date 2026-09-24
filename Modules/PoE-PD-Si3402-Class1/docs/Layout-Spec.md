# Layout Spec — PoE-PD-Si3402-Class1

The geometry of the module reference board. Every number here is a decision,
and each one carries its reason.

Board: 40 x 76 mm, 4 layers, 1.6 mm, PCBWay.

---

## 1. Outline and regions

All coordinates are KiCad board millimetres.

| Item | X | Y |
|---|---|---|
| Board outline | 100.0 → 140.0 | 60.0 → 136.0 |
| Primary region | 100.0 → 140.0 | 60.0 → 98.5 |
| Barrier band | 100.0 → 140.0 | 98.5 → 101.0 |
| Secondary region | 100.0 → 140.0 | 101.0 → 136.0 |

The barrier band is 2.5 mm tall and holds no copper of either domain.

The primary region is 38.5 mm tall because the heat spreader needs it. See
section 3.

## 2. The domain split

45 parts. The split is taken from the exported netlist, not from the schematic
drawing.

**Primary, 28 parts.** U5, C70 to C82, C87, C88, D30, D31, FB3, FB4, FB5, FB6,
R50, R51, R57, R58, TP5, TP6.

**Bridges, 4 parts.** T1, U7, C89, C90. Each one straddles the barrier band.

**Secondary, 13 parts.** C83, C84, C85, C86, D32, L31, R52, R53, R54, R55,
R56, U6, TP4.

`../../../docs/Block-Modules-Handoff.md` section 4.1 names 26 primary components. TP5 and
TP6 raise that to 28. TP5 probes SWO and TP6 probes EROUT. Both are primary
nets, so both test points are primary side.

`SNUB_MID` is a **secondary** net. It joins C83 pin 2 to R52 pin 1, and the
other ends sit on SEC_A and VOUT_RAW. The RC snubber is across the secondary
rectifier D32.

## 3. The heat spreader

**This is the reason the module exists as its own board.**

| Item | Value |
|---|---|
| Layer | B.Cu, an OUTER layer |
| Net | `/VNEG` |
| Zone priority | 2 |
| Rectangle | X 100.5 → 139.5, Y 60.5 → 98.0 |
| Area | 39.0 x 37.5 = **1462 mm²**, 2.27 in² |
| Required | 1290 mm², 2 in² |
| Margin | 172 mm², 13 percent |

**The plane must stay on an outer layer.** AN956 measures 44 °C/W for 2 in² on
an outer layer, and 54 °C/W for 1 in² on an inner layer. Inner layer copper is
not a substitute.

Thermal budget:

| Item | Value |
|---|---|
| Class 1 power budget | 3.84 W |
| Worst case dissipation in U5 | 0.85 W |
| Rise at 44 °C/W | 37 °C |
| Junction at 85 °C ambient | 122 °C |
| Thermal shutdown | 160 °C |
| Margin | 38 °C |

A second VNEG pour sits on F.Cu over the same rectangle, at priority 2. The
parts break it up, so it does not count toward the 2 in². It lowers spreading
resistance and it gives the stitching vias something to land on.

## 4. Thermal via array

U5 is a QFN-20 with a 2.75 x 2.75 mm exposed pad, pad 21, on F.Cu only. The
footprint carries no thermal vias. The module adds them.

| Item | Value |
|---|---|
| Array | 3 x 3, nine vias |
| Pitch | 0.9 mm |
| Via | 0.6 mm diameter, 0.3 mm drill |
| Net | `/VNEG` |
| Centre | U5 origin |

Why 0.9 mm. The outer via edge sits 0.9 + 0.3 = 1.2 mm from the centre. The
exposed pad half width is 1.375 mm. That leaves 0.175 mm of pad copper outside
the via ring. A 1.0 mm pitch leaves 0.075 mm, and a 4 x 4 array at 0.75 mm
pitch overruns the pad.

**The four corner vias sit under solder paste.** The footprint puts four
1.2 mm paste windows at (±0.7, ±0.7), which span 0.1 to 1.3 mm in each
quadrant. The vias at (±0.9, ±0.9) fall inside those windows. Tent the vias on
both faces, which is the board default. Ask PCBWay for resin plugging if you
build more than a handful. No nine via arrangement avoids the paste windows
inside a 2.75 mm pad at this via size.

Twelve stitching vias ring U5 at ±4.5 mm, three on each side, on net `/VNEG`.
They tie the F.Cu primary pour to the B.Cu spreader. They sit outside U5's
3.075 mm courtyard.

## 5. The inner plane void

A keepout zone on In1.Cu and In2.Cu.

| Item | Value |
|---|---|
| Rectangle | X 99.0 → 141.0, Y 59.0 → 101.0 |
| Layers | In1.Cu, In2.Cu |
| Forbids | copper pour |
| Allows | tracks, vias |

It covers the whole primary region and the whole barrier band, and it runs past
the outline on three sides so no inner copper survives at the edge.

The secondary ground plane must not run under the primary circuit. Inner copper
there would carry the barrier across on two layers and defeat T1, U7, C89 and
C90.

The void is also what lets the thermal vias pass from F.Cu to B.Cu without
touching a secondary plane.

## 6. The isolation slot

| Item | Value |
|---|---|
| Type | NPTH slot |
| Width | 1.0 mm |
| Centre line | Y = 99.75 |
| Extent | segmented across X 100 → 140 |

PCBWay's minimum NPTH slot is 0.8 mm at ±0.2 mm tolerance, so the module draws
1.0 mm.

The slot breaks at each bridge body. T1, U7, C89 and C90 sit on the band and
their pads reach both sides, so the slot runs only in the gaps between them.

**On this module the slot runs the full width, in segments.** On a host board
with a magjack it cannot. `../../../docs/Block-Modules-Handoff.md` section 4.5 records why:
the magjack's line side pins interleave with its chip side pins in one pad
field, about 1.3 mm copper to copper, and Abracon's land pattern fixes that.
The slot must stop at the magjack body, and Abracon's 1500 Vrms construction is
the isolation there. A host board must add that exception back.

## 7. Zone table

| Zone | Layer | Net | Priority | Rectangle |
|---|---|---|---|---|
| Heat spreader | B.Cu | `/VNEG` | 2 | 100.5, 60.5 → 139.5, 98.0 |
| Primary top pour | F.Cu | `/VNEG` | 2 | 100.5, 60.5 → 139.5, 98.0 |
| Secondary top pour | F.Cu | `GND` | 1 | 100.5, 101.5 → 139.5, 135.5 |
| Secondary bottom pour | B.Cu | `GND` | 1 | 100.5, 101.5 → 139.5, 135.5 |
| Inner plane 1 | In1.Cu | `GND` | 0 | 100.5, 60.5 → 139.5, 135.5 |
| Inner plane 2 | In2.Cu | `GND` | 0 | 100.5, 60.5 → 139.5, 135.5 |
| Inner plane void | In1.Cu, In2.Cu | keepout | 0 | 99.0, 59.0 → 141.0, 101.0 |

The two inner planes are drawn over the whole board. The void takes the primary
half away. That is one zone to edit when the barrier moves, not two.

## 8. Checks before you believe a number

1. Refill the zones. `kicad-cli pcb drc` grades the saved fill unless you pass
   `--refill-zones`, and that flag refills in memory only. It never writes back.
   One run on the parent board showed 61 errors, and 53 were stale fills.
2. Confirm the net classes bind. Open the net inspector and read the class
   column. An unbound class makes the barrier rule pass with zero hits.
3. Confirm the custom rules loaded. A syntax error disables the whole file and
   KiCad reports nothing.
4. Render the board to SVG and look at it. Coordinate arithmetic got the parent
   board's J3 geometry wrong twice before a render settled it.
