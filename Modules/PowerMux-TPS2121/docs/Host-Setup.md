# Host setup for the PowerMux-TPS2121 block

A design block carries footprints, tracks, vias and zones. **It does not carry
the board outline, the net classes, the stackup or the custom rules.** Set those
in the host board first. Then place the block.

If you skip this page, the block places and DRC passes, because the rules that
would fail are not there.

| Item | Where |
|---|---|
| Module board | `Modules/PowerMux-TPS2121/` |
| Fragment | `${PLUM_SOLUTIONS}/Blocks/PlumBlocks.kicad_blocks/PowerMux-TPS2121.kicad_block/` |
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

**Set the In1.Cu type to `power`, not `signal`.** In1 is one solid GND plane under
the whole block.

The board file sets no surface finish. Choose it with the fab. U10 is a 0.5 mm
pitch VQFN-HR-12 with no exposed pad.

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
Power_2   /POE_5V /VBUS /V5_SYS
```

**Check the class column in the net inspector after you place the block.** The
three power nets carry 1.5 A typical and 2.0 A at the current limit ceiling.

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

Copy `PowerMux-TPS2121.kicad_dru` into the host project and merge it. It holds
22 rules: 21 shared PCBWay fab rules and 1 module rule. Two matter most.

1. **`Fine-pitch fanout clearance` 0.10 mm, scoped to `U10.insideCourtyard`.**
   The 0.5 mm pitch fanout needs it. It applies nowhere else.
2. **`hole to hole clearance (different nets)` 0.5 mm.** The breakout vias
   inside one power group are 1.0 mm apart, which gives 0.7 mm hole to hole.

**The module rule names `U10`.** KiCad re-annotates on placement (§5.1). Edit
the rule to the new designator, or it binds to nothing.

**Confirm the file loaded.** Open Board Setup → Custom Rules. A syntax error
disables the whole file, and the command line reports nothing.

---

## 5. What the block does not bring

| Item | Why | What to do |
|---|---|---|
| Board outline | A block carries no outline. The fragment has it on `Dwgs.User` | Draw the host outline |
| F.Cu, In1.Cu, B.Cu `GND` pours | Each fills the module, 100.5, 100.5 → 114.5, 119.5 | Join them to the host GND on those layers |
| In2.Cu `/V5_SYS` plane | Fills the module. **It is the only path from the two OUT pads to the row** | Keep `/V5_SYS` on In2 under the whole block |
| Heat | 0.23 W worst case, 16 °C rise | No spreader needed |

**Do not cut the In2 plane under the block.** U10's OUT pads, 1 and 8, sit on
opposite sides of the body. Each drops to In2 through 3 vias. In2 joins them and
carries the current to the three row vias. There is no F.Cu path past C107 and
R74.

### The set points, as fitted

| Item | Parts | Value |
|---|---|---|
| PR1 priority, IN1 rising | R70 169 k, R71 51.1 k | **4.57 V** typ |
| PR1 priority, IN1 falling | same | **4.48 V** typ |
| OV1 and OV2 trip, rising | 46.4 k / 10 k | **5.98 V** typ, 5.70 to 6.20 V |
| Current limit | R74 80.6 k | 1.49 A typ |

The thresholds use SLVSEA3F §7.5: VREF 1.06 V rising and 1.04 V falling. Below
the PR1 threshold, the higher input wins. The handover at 4.48 V sits at the
floor of the TPS563208 buck below the mux.

The reference board at `Modules/PowerMux-TPS2121/` is the worked example. Read
its `Layout-Spec.md` before you change anything the block places.

---

## 5.1 KiCad re-annotates on placement

**The block's `U10` is not your `U10`.** KiCad renumbers the references unless
you tick `keep_annotations` in the design block chooser. The custom rule in §4
names `U10`.

Read the net names, not the designators, when you check the placed block against
`Layout-Spec.md`.

## 5.2 Set the power pads to solid after placement

The module board connects C108 to C111 to the pours with **solid** pads, not thermal
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
| "Place as sheet" **on** | The block gets its own page and title block. It prints whole | `/PowerMux-TPS2121/VPOS` |

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

Eleven vias on the block's bottom edge, y 117.5 on the reference board. Each
power via carries a 1.0 mm stub on B.Cu, toward the edge. **The stub has a free
end by design.** DRC calls that `track_dangling`. Land on it. Do not delete it.

An `F.Fab` label names every via.

| x | y | Net | Direction | Stub layer |
|---|---|---|---|---|
| 101.2 | 117.5 | `/POE_5V` | in | B.Cu |
| 102.2 | 117.5 | `/POE_5V` | in | B.Cu |
| 103.2 | 117.5 | `/POE_5V` | in | B.Cu |
| 104.8 | 117.5 | `GND` | stitch | none |
| 106.4 | 117.5 | `/V5_SYS` | out | B.Cu |
| 107.4 | 117.5 | `/V5_SYS` | out | B.Cu |
| 108.4 | 117.5 | `/V5_SYS` | out | B.Cu |
| 110.0 | 117.5 | `GND` | stitch | none |
| 111.6 | 117.5 | `/VBUS` | in | B.Cu |
| 112.6 | 117.5 | `/VBUS` | in | B.Cu |
| 113.6 | 117.5 | `/VBUS` | in | B.Cu |

Every power net arrives on F.Cu. `/V5_SYS` also arrives on the In2 plane.

**Land on all three vias of a group.** Two vias carry 1.5 A. The third covers
the 2.0 A ceiling.

`/POE_5V` comes from a PoE block. `/VBUS` comes from `USBC-Device-ESD`.
`/V5_SYS` feeds the buck and the RF LDO.

The control nets `/MUX_PR1`, `/MUX_OV1`, `/MUX_OV2`, `/MUX_ILIM` and `/MUX_SS`
stay inside the block. U10 pin 9, ST, stays unconnected.
