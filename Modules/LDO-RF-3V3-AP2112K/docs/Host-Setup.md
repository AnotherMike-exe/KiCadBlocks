# Host setup for the LDO-RF-3V3-AP2112K block

A design block carries footprints, tracks, vias and zones. **It does not carry
the board outline, the net classes, the stackup or the custom rules.** Set those
in the host board first. Then place the block.

If you skip this page, the block places and DRC passes, because the rules that
would fail are not there.

| Item | Where |
|---|---|
| Module board | `Modules/LDO-RF-3V3-AP2112K/` |
| Fragment | `${PLUM_SOLUTIONS}/Blocks/PlumBlocks.kicad_blocks/LDO-RF-3V3-AP2112K.kicad_block/` |
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
under the block.

The board file sets no surface finish. Choose it with the fab.

---

## 2. Net classes

| Class | Track | Clearance | Via | Diff pair |
|---|---|---|---|---|
| `Default` | 0.20 | 0.20 | 0.6 / 0.3 | 0.20 / 0.25 |
| `Power_1` | 0.3048 | 0.1524 | 0.6 / 0.3 | — |
| `GND_SYS` | — | 0.1524 | — | — |

### Patterns

Use plain net names. **A sheet path pattern binds to nothing here**, because the
block's nets arrive under the host's own sheet.

```
GND_SYS   GND
Power_1   /V5_SYS /+3V3_RF
```

The block uses a hierarchical label for `+3V3_RF`, so the net is `/+3V3_RF`,
with the prefix.

**Check the class column in the net inspector after you place the block.**

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

Copy `LDO-RF-3V3-AP2112K.kicad_dru` into the host project and merge it. It
holds 21 rules. All are the shared PCBWay fab rules. **The block has no module
rule.** The net classes govern it. One fab rule matters most.

1. **`Trace to Outline` 0.3 mm.** `/+3V3_RF` drops to the row 0.85 mm from the
   module's right edge.

**Confirm the file loaded.** Open Board Setup → Custom Rules. A syntax error
disables the whole file, and the command line reports nothing.

---

## 5. What the block does not bring

| Item | Why | What to do |
|---|---|---|
| Board outline | A block carries no outline. The fragment has it on `Dwgs.User` | Draw the host outline |
| F.Cu, In1.Cu, B.Cu `GND` pours | Each fills the module, 100.5, 100.5 → 109.5, 111.5 | Join them to the host GND on those layers |
| In2.Cu `/V5_SYS` plane | Fills the module. **U9's EN pin reaches `/V5_SYS` only through it** | Keep `/V5_SYS` on In2 under the block |
| Heat | 51 mW at 5.00 V, 59 mW at 5.25 V, 9 to 11 °C rise | No thermal copper needed |

**Do not cut the In2 plane under the block.** EN drops to In2 through a via at
103.862, 106.8. Without the plane, EN floats and U9 does not start.

**`/+3V3_RF` feeds only the CC1101.** The block exists to keep buck noise off
the 433 MHz front end. Connect `/+3V3_RF` to the `RF-CC1101-433` block and to
nothing else. Keep switching copper away from it.

The reference board at `Modules/LDO-RF-3V3-AP2112K/` is the worked example. Read
its `Layout-Spec.md` before you change anything the block places.

---

## 5.1 KiCad re-annotates on placement

**The block's `U9` is not your `U9`.** KiCad renumbers the references unless you
tick `keep_annotations` in the design block chooser.

Read the net names, not the designators, when you check the placed block against
`Layout-Spec.md`.

## 6. The interface

Five vias on the block's bottom edge, y 109.5 on the reference board. Each
signal via carries a 1.0 mm stub on the layer opposite its arrival, toward the
edge. **The stub has a free end by design.** DRC calls that `track_dangling`.
Land on it. Do not delete it.

An `F.Fab` label names every via.

| x | y | Net | Direction | Stub layer |
|---|---|---|---|---|
| 101.2 | 109.5 | `GND` | stitch | none |
| 102.8 | 109.5 | `/V5_SYS` | in | F.Cu |
| 104.4 | 109.5 | `GND` | stitch | none |
| 107.4 | 109.5 | `GND` | stitch | none |
| 109.0 | 109.5 | `/+3V3_RF` | out | B.Cu |

`/V5_SYS` arrives on the In2 plane, so its stub is on F.Cu. `/+3V3_RF` arrives
on F.Cu from U9 pin 5, so its stub is on B.Cu.

The load is 30 mA. One via per power net carries it.
