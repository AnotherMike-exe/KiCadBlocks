# Host setup for the Buck-5V-3V3-TPS563208 block

A design block carries footprints, tracks, vias and zones. **It does not carry
the board outline, the net classes, the stackup or the custom rules.** Set those
in the host board first. Then place the block.

If you skip this page, the block places and DRC passes, because the rules that
would fail are not there.

| Item | Where |
|---|---|
| Module board | `Modules/Buck-5V-3V3-TPS563208/` |
| Fragment | `${PLUM_SOLUTIONS}/Blocks/PlumBlocks.kicad_blocks/Buck-5V-3V3-TPS563208.kicad_block/` |
| Outline in the fragment | `Dwgs.User`, not `Edge.Cuts` |

---

## 1. Stackup

Four layers. Board Setup → Board Editor Layers.

| Layer | Type | Name | Thickness |
|---|---|---|---|
| F.Cu | signal | — | 0.035 |
| dielectric 1 | prepreg | — | 0.10 |
| In1.Cu | **power** | `GND` | 0.035 |
| dielectric 2 | core | — | 1.24 |
| In2.Cu | **power** | `PWR` | 0.035 |
| dielectric 3 | prepreg | — | 0.10 |
| B.Cu | signal | — | 0.035 |

**Set the In1.Cu type to `power`, not `signal`.** In1 is one whole GND plane
under the block. It is the return for the switching loop and a heat path for U8.

The board file sets no surface finish. Choose it with the fab.

---

## 2. Net classes

| Class | Track | Clearance | Via | Diff pair |
|---|---|---|---|---|
| `Default` | 0.20 | 0.20 | 0.6 / 0.3 | 0.20 / 0.25 |
| `Power_2` | 0.508 | 0.1524 | 0.6 / 0.3 | — |
| `GND_SYS` | — | 0.1524 | — | — |

### Patterns

Use plain net names. **A sheet path pattern binds to nothing here**, because the
block's nets arrive under the host's own sheet.

```
GND_SYS   GND
Power_2   /V5_SYS +3V3 /SW_NODE
```

`+3V3` is a global net. It has no `/` prefix.

**Check the class column in the net inspector after you place the block.** The
block carries up to 2 A out and 1.47 A in.

---

## 3. Board minimums

| Rule | Value |
|---|---|
| min track width | 0.20 |
| min via diameter | 0.50 |
| min via annular width | 0.10 |
| min through hole diameter | 0.30 |
| min hole to hole | 0.25 |
| min hole clearance | 0.25 |
| min copper to edge | 0.50 |
| min resolved spokes | 2 |
| min text height | 0.80 |
| min text thickness | 0.08 |

---

## 4. Custom rules

Copy `Buck-5V-3V3-TPS563208.kicad_dru` into the host project and merge it. It
holds 21 rules. All are the shared PCBWay fab rules. **The block has no module
rule.** The net classes govern it. Two fab rules matter most.

1. **`hole to hole clearance (different nets)` 0.5 mm.** The breakout vias
   inside one power group are 1.0 mm apart, which gives 0.7 mm hole to hole.
2. **`Trace to Outline` 0.3 mm.** The stubs end 1.5 mm from the module edge.

**Confirm the file loaded.** Open Board Setup → Custom Rules. A syntax error
disables the whole file, and the command line reports nothing.

---

## 5. What the block does not bring

| Item | Why | What to do |
|---|---|---|
| Board outline | A block carries no outline. The fragment has it on `Dwgs.User` | Draw the host outline |
| F.Cu, In1.Cu, B.Cu `GND` pours | Each fills the module, 100.5, 100.5 → 117.5, 119.5 | Join them to the host GND on those layers |
| In2.Cu `/V5_SYS` plane | Fills the module. EN reaches `/V5_SYS` through it, and it joins the six `/V5_SYS` vias | Keep `/V5_SYS` on In2 under the block |
| Heat | Measured on the filled zone | **Not measured yet.** Estimate 0.5 W in U8, 46 °C rise. Measure it |

### The output, as fitted

| Item | Value |
|---|---|
| Vout, typ | **3.30 V**, 0.768 x (1 + 33 k / 10 k) = 3.302 V |
| Vout, full VFB range | 3.22 to 3.38 V |
| Vin minimum | 4.5 V |

**The input capacitors sit at VIN.** C101, 100 nF, lines up with U8 pin 3.
C100, 22 µF 1206, sits beside it. Do not move them away from U8 in the host.
TI SLVSD90B §7.4.1 asks for them close to the device.

**The switch node stays inside the block.** `/SW_NODE` is a 0.6 mm strip on
F.Cu from U8 pin 2 to L30. Route no host signal east of U8, near the feedback
network.

The reference board at `Modules/Buck-5V-3V3-TPS563208/` is the worked example.
Read its `Layout-Spec.md` before you change anything the block places.

---

## 5.1 KiCad re-annotates on placement

**The block's `U8` is not your `U8`.** KiCad renumbers the references unless you
tick `keep_annotations` in the design block chooser.

Read the net names, not the designators, when you check the placed block against
`Layout-Spec.md`.

## 5.2 Set the power pads to solid after placement

The module board connects U8, L30 and C100 to C104 to the pours with **solid** pads, not thermal
spokes (review R2-3, 2026-09-25). **The fragment does not carry this.** The
placement takes each footprint from the library, and the per-footprint zone
connection is lost. Measured 2026-09-25: 0 of the solid overrides arrived.

1. In the host board, select the listed footprints.
2. Open **Properties**. Set **Zone connection** to **Solid**.
3. Refill the zones (B).

## 5.3 Place as sheet: the net names change

Two ways to place this block. Both bring the same layout.

| Option in the Design Blocks panel | The schematic | The net names |
|---|---|---|
| "Place as sheet" **off** | The symbols land on the host's own page | `/VPOS`, as in the patterns above |
| "Place as sheet" **on** | The block gets its own page and title block. It prints whole | `/Buck-5V-3V3-TPS563208/VPOS` |

**With "Place as sheet" on, every `/NAME` pattern above binds to nothing.**
Measured 2026-09-25 on the PoE block through the KiCad API: MDI bound 0 of 10
nets, and Chassis, GND_PRI and PoE_Load bound none. An unbound net class makes
every class rule pass with zero hits.

Fix it once in the host, **Board Setup → Net Classes → Patterns**. Change each
pattern from `/NAME` to `*/NAME`, for example `*/VPOS`. The `*` matches the root
`/` and any sheet path. Power nets such as `GND` and `+3V3` keep no prefix.
Measured on the same board: with `*/NAME` every class binds again, and on a
flat placement `*/NAME` binds exactly the nets `/NAME` binds. Patterns that name
a designator, such as `unconnected-(U1-*)`, need the section 5.1 fix as well.
Then check the class column in the net inspector.

## 6. The interface

Ten vias on the block's bottom edge, y 117.5 on the reference board. Each power
via carries a 1.0 mm stub on B.Cu, toward the edge. **The stub has a free end by
design.** DRC calls that `track_dangling`. Land on it. Do not delete it.

An `F.Fab` label names every via.

| x | y | Net | Direction | Stub layer |
|---|---|---|---|---|
| 101.2 | 117.5 | `+3V3` | out | B.Cu |
| 102.2 | 117.5 | `+3V3` | out | B.Cu |
| 103.2 | 117.5 | `+3V3` | out | B.Cu |
| 104.8 | 117.5 | `GND` | stitch | none |
| 107.8 | 117.5 | `GND` | stitch | none |
| 110.8 | 117.5 | `GND` | stitch | none |
| 112.4 | 117.5 | `/V5_SYS` | in | B.Cu |
| 113.4 | 117.5 | `/V5_SYS` | in | B.Cu |
| 114.4 | 117.5 | `/V5_SYS` | in | B.Cu |
| 116.0 | 117.5 | `GND` | stitch | none |

Every power net arrives on F.Cu. `/V5_SYS` also arrives on the In2 plane.

`+3V3` breaks out west, under the output capacitors. `/V5_SYS` breaks out east,
under the input capacitors. Neither crosses the other.

`/V5_SYS` comes from `PowerMux-TPS2121`. Land on all three vias of each group.

`/SW_NODE`, `/VBST`, `/VFB_33` and `/LED_PWR_A` stay inside the block.
