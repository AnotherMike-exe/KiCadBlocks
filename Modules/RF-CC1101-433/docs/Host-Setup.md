# Host setup for the RF-CC1101-433 block

A design block carries footprints, tracks, vias and zones. **It does not carry
the board outline, the net classes, the stackup or the custom rules.** Set those
in the host board first. Then place the block.

If you skip this page, the block places and DRC passes, because the rules that
would fail are not there.

| Item | Where |
|---|---|
| Module board | `Modules/RF-CC1101-433/` |
| Fragment | `${PLUM_SOLUTIONS}/Blocks/PlumBlocks.kicad_blocks/RF-CC1101-433.kicad_block/` |
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

**Set the In1.Cu type to `power`, not `signal`.** The 0.10 mm prepreg under F.Cu
sets the `RF_50` width. 0.17 mm gives about 49 Ω over 0.10 mm. **If the fab's
real prepreg is not 0.10 mm, compute the width again.** At 0.20 mm, 50 Ω is
about 0.35 mm wide.

J3 fits a 0.062 in board. Order **1.6 mm finished**.

The board file sets no surface finish. Choose it with the fab. U4 is a 0.5 mm
pitch QFN-20.

---

## 2. Net classes

| Class | Track | Clearance | Via | Diff pair |
|---|---|---|---|---|
| `Default` | 0.20 | 0.20 | 0.6 / 0.3 | 0.20 / 0.25 |
| `Power_1` | 0.3048 | 0.1524 | 0.6 / 0.3 | — |
| `GND_SYS` | — | 0.1524 | — | — |
| `RF_50` | 0.17 | 0.25 | 0.6 / 0.3 | — |

### Patterns

Use plain net names. **A sheet path pattern binds to nothing here**, because the
block's nets arrive under the host's own sheet.

```
GND_SYS   GND
Power_1   /+3V3_RF /VDD_CC1101
RF_50     /ANT_433
```

**`RF_50` on `/ANT_433` is the 50 Ω feed from C35 to J3.** The 0.25 mm
clearance is the gap to the F.Cu GND pour on each side of the line.

**Check the class column in the net inspector after you place the block.** An
unbound `RF_50` class leaves the feed at the Default width.

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

Copy `RF-CC1101-433.kicad_dru` into the host project and merge it. It holds 23
rules: 21 shared PCBWay fab rules and 2 module rules. Both matter.

1. **`J3 pads reach the board edge`, edge clearance 0 mm, scoped to
   `A.Parent == 'J3'`.** J3 is an edge-mount SMA. Its pads end at the board
   edge by design. Without this rule the 0.5 mm board minimum flags every J3
   pad. A pad that touches the edge still fails DRC, so J3 sits 0.02 mm
   inboard.
2. **`Fine-pitch fanout clearance` 0.10 mm, scoped to `U4.insideCourtyard`.**
   The QFN-20 fanout needs it. It applies nowhere else.

**Both rules name a designator.** KiCad re-annotates on placement (§5.1). Edit
each rule to the new `J3` and `U4`, or the rule binds to nothing.

**Confirm the file loaded.** Open Board Setup → Custom Rules. A syntax error
disables the whole file, and the command line reports nothing.

---

## 5. What the block does not bring

| Item | Why | What to do |
|---|---|---|
| Board outline | A block carries no outline. The fragment has it on `Dwgs.User` | Draw the host outline |
| J3 on the host edge | J3 straddles the edge. Pad 1 must end at the edge line, module y 100.0 | Put the host edge on that line |
| F.Cu, B.Cu, In2.Cu `GND` pours | Each fills the module, 100.5, 100.5 → 124.5, 129.5 | Join them to the host GND on those layers |
| In1.Cu `GND` notch under J3 pad 1 | Part of the In1 zone, x 110.38 → 112.38, y 100.5 → 105.33 | Keep the notch if you redraw In1 |
| In2.Cu net | The block puts `GND` on In2, not `PWR` | Keep the host In2 plane out of the block area, or make it GND there |
| Exposed pad vias | 5 vias sit inside U4's EP mask opening, not tented | Fab question. See below |

**The In1 notch sets the J3 launch.** Pad 1 over In1 at 0.10 mm forms about
3.0 pF. At 433 MHz that is a 122 Ω shunt. With In1 cut, the reference is In2 GND
at 1.375 mm. Do not fill the notch.

**Never change C20 or C21.** 12 pF and 15 pF are asymmetric on purpose. TI's
SWRR046 reference sets them for the NX3225GA crystal.

**The exposed pad vias need plugging.** The four corner vias sit inside the
paste windows. Ask the fab to fill and cap them, or make a footprint variant
with a split mask. `Layout-Spec.md` §10 D1 holds the detail.

The reference board at `Modules/RF-CC1101-433/` is the worked example. Read its
`Layout-Spec.md` before you change anything the block places.

---

## 5.1 KiCad re-annotates on placement

**The block's `U4` is not your `U4`.** KiCad renumbers the references unless you
tick `keep_annotations` in the design block chooser. The custom rules in §4 name
`J3` and `U4`.

Read the net names, not the designators, when you check the placed block against
`Layout-Spec.md`.

## 5.3 Place as sheet: the net names change

Two ways to place this block. Both bring the same layout.

| Option in the Design Blocks panel | The schematic | The net names |
|---|---|---|
| "Place as sheet" **off** | The symbols land on the host's own page | `/VPOS`, as in the patterns above |
| "Place as sheet" **on** | The block gets its own page and title block. It prints whole | `/RF-CC1101-433/VPOS` |

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

Eleven vias on the block's bottom edge, y 127.5 on the reference board. Each
signal via carries a 1.0 mm stub on B.Cu, toward the edge. **The stub has a free
end by design.** DRC calls that `track_dangling`. Land on it. Do not delete it.

An `F.Fab` label names every via.

| x | y | Net | Direction | Stub layer |
|---|---|---|---|---|
| 101.5 | 127.5 | `GND` | stitch | none |
| 104.5 | 127.5 | `GND` | stitch | none |
| 105.6 | 127.5 | `/CC1101_MOSI` | in | B.Cu |
| 107.2 | 127.5 | `/CC1101_SCK` | in | B.Cu |
| 108.8 | 127.5 | `/CC1101_MISO` | out | B.Cu |
| 110.4 | 127.5 | `/CC1101_GDO2_RX` | out | B.Cu |
| 112.0 | 127.5 | `/CC1101_GDO0_TX` | in | B.Cu |
| 113.6 | 127.5 | `/CC1101_CS` | in | B.Cu |
| 115.2 | 127.5 | `/+3V3_RF` | in | B.Cu |
| 118.5 | 127.5 | `GND` | stitch | none |
| 121.5 | 127.5 | `GND` | stitch | none |

Every signal net arrives on F.Cu.

Feed `/+3V3_RF` from the `LDO-RF-3V3-AP2112K` block. Keep switching copper away
from it.

`/ANT_433` does not break out. It ends at J3.
