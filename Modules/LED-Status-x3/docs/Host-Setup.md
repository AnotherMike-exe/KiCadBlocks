# Host setup for the LED-Status-x3 block

A design block carries footprints, tracks, vias and zones. **It does not carry
the board outline, the net classes, the stackup or the custom rules.** Set those
in the host board first. Then place the block.

If you skip this page, the block places and DRC passes, because the rules that
would fail are not there.

| Item | Where |
|---|---|
| Module board | `Modules/LED-Status-x3/` |
| Fragment | `${PLUM_SOLUTIONS}/Blocks/PlumBlocks.kicad_blocks/LED-Status-x3.kicad_block/` |
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

**Set the In1.Cu type to `power`, not `signal`.** The block needs no controlled
impedance. It uses the family stackup so that it drops into any Plum host.

`Layout-Spec.md` still reads "2 layers". The board file has 4. The board file is
right.

The board file sets no surface finish. Choose it with the fab.

---

## 2. Net classes

| Class | Track | Clearance | Via | Diff pair |
|---|---|---|---|---|
| `Default` | 0.20 | 0.20 | 0.6 / 0.3 | 0.20 / 0.25 |
| `GND_SYS` | — | 0.1524 | — | — |

### Patterns

Use plain net names. **A sheet path pattern binds to nothing here**, because the
block's nets arrive under the host's own sheet.

```
GND_SYS   GND
```

The three LED nets use `Default`. Each carries 4 to 5 mA.

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

Copy `LED-Status-x3.kicad_dru` into the host project and merge it. It holds 21
rules. All are the shared PCBWay fab rules. **The block has no module rule.**
The net classes govern it. One fab rule matters most.

1. **`Trace to Outline` 0.3 mm.** The stubs end 1.5 mm from the module edge.

**Confirm the file loaded.** Open Board Setup → Custom Rules. A syntax error
disables the whole file, and the command line reports nothing.

---

## 5. What the block does not bring

| Item | Why | What to do |
|---|---|---|
| Board outline | A block carries no outline. The fragment has it on `Dwgs.User` | Draw the host outline |
| F.Cu, In1.Cu, In2.Cu, B.Cu `GND` pours | Each fills the module, 100.5, 100.5 → 113.5, 110.5 | Join them to the host GND on those layers |
| In2.Cu net | The block puts `GND` on In2, not `PWR` | Keep the host In2 plane out of the block area, or make it GND there |
| Panel position | The LEDs sit on the module's top edge side | Put that side toward the front panel |

The LEDs run green, amber, red, left to right, on a 2.6 mm pitch. That pitch
suits a light pipe.

| LED | Colour | Series resistor | Net |
|---|---|---|---|
| D1 | green | R4, 220 Ω | `/LED_RF_TX` |
| D2 | amber | R5, 330 Ω | `/LED_LEARN` |
| D3 | red | R6, 330 Ω | `/LED_FAULT` |

The reference board at `Modules/LED-Status-x3/` is the worked example. Read its
`Layout-Spec.md` before you change anything the block places.

---

## 5.1 KiCad re-annotates on placement

**The block's `D1` is not your `D1`.** KiCad renumbers the references unless you
tick `keep_annotations` in the design block chooser.

Read the net names, not the designators, when you check the placed block against
`Layout-Spec.md`.

## 6. The interface

Five vias on the block's bottom edge, y 108.5 on the reference board. Each
signal via carries a 1.0 mm stub on B.Cu, toward the edge. **The stub has a free
end by design.** DRC calls that `track_dangling`. Land on it. Do not delete it.

An `F.Fab` label names every via.

| x | y | Net | Direction | Stub layer |
|---|---|---|---|---|
| 101.0 | 108.5 | `GND` | stitch | none |
| 104.0 | 108.5 | `GND` | stitch | none |
| 107.3 | 108.5 | `/LED_RF_TX` | in | B.Cu |
| 108.9 | 108.5 | `/LED_LEARN` | in | B.Cu |
| 110.5 | 108.5 | `/LED_FAULT` | in | B.Cu |

Every signal net arrives on F.Cu. The MCU GPIO sources the current. Each LED
cathode returns to `GND` inside the block.

The 3.3 mm gap from the last GND to the first signal matches the PoE module.
