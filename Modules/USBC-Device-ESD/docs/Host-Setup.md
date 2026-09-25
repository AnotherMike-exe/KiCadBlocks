# Host setup for the USBC-Device-ESD block

A design block carries footprints, tracks, vias and zones. **It does not carry
the board outline, the net classes, the stackup or the custom rules.** Set those
in the host board first. Then place the block.

If you skip this page, the block places and DRC passes, because the rules that
would fail are not there.

| Item | Where |
|---|---|
| Module board | `Modules/USBC-Device-ESD/` |
| Fragment | `${PLUM_SOLUTIONS}/Blocks/PlumBlocks.kicad_blocks/USBC-Device-ESD.kicad_block/` |
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

**Set the In1.Cu type to `power`, not `signal`.** In1 is the reference for the
USB pair. The 0.10 mm prepreg under F.Cu sets its impedance. 0.20 / 0.20 over
0.10 mm gives about 84 Ω differential, inside the USB 2.0 band of 76.5 to
103.5 Ω. **If the fab's real prepreg is not 0.10 mm, compute it again.**

The board file sets no surface finish. Choose it with the fab.

---

## 2. Net classes

| Class | Track | Clearance | Via | Diff pair |
|---|---|---|---|---|
| `Default` | 0.20 | 0.20 | 0.6 / 0.3 | 0.20 / 0.25 |
| `Power_2` | 0.508 | 0.1524 | 0.6 / 0.3 | — |
| `GND_SYS` | — | 0.1524 | — | — |
| `USB` | 0.20 | 0.20 | 0.6 / 0.3 | 0.20 / 0.20 |

### Patterns

Use plain net names. **A sheet path pattern binds to nothing here**, because the
block's nets arrive under the host's own sheet.

```
GND_SYS   GND
Power_2   /VBUS
USB       /USB_DP /USB_DM /USB_DP_CONN /USB_DM_CONN
```

**Check the class column in the net inspector after you place the block.** An
unbound `USB` class routes the pair at the Default gap.

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

Copy `USBC-Device-ESD.kicad_dru` into the host project and merge it. It holds 22
rules: 21 shared PCBWay fab rules and 1 module rule. Two matter most.

1. **`J1 own pads to own pegs`, hole clearance 0.15 mm.** The stock GCT USB4110
   footprint puts pads A1/B12 and B1/A12 0.194 mm from J1's own NPTH locating
   pegs. The rule applies only when both items belong to J1. Routed copper near
   a peg keeps the full 0.20 mm.
2. **`NPTH with copper around` 0.20 mm.** Without rule 1, this rule flags the
   four J1 pads.

**Rule 1 names `J1`.** KiCad re-annotates on placement (§5.1). Edit the rule to
the new designator, or it binds to nothing and DRC reports 4 errors.

**Confirm the file loaded.** Open Board Setup → Custom Rules. A syntax error
disables the whole file, and the command line reports nothing.

---

## 5. What the block does not bring

| Item | Why | What to do |
|---|---|---|
| Board outline | A block carries no outline. The fragment has it on `Dwgs.User` | Draw the host outline |
| J1 on the host edge | J1's `PCB Edge` line on `Dwgs.User` sits at module y 100.0 | Put the host edge on that line |
| F.Cu, In1.Cu, In2.Cu, B.Cu `GND` pours | Each fills the module, 100.5, 100.5 → 119.5, 120.5 | Join them to the host GND on those layers |
| In2.Cu net | The block puts `GND` on In2, not `PWR` | Keep the host In2 plane out of the block area, or make it GND there |

**J1 must sit on the host edge.** The footprint draws its `PCB Edge` line at
local y +3.675, the front face of the receptacle. Put the host `Edge.Cuts` on
that line, so the face is flush with the edge. J1's courtyard runs to y 99.495,
past the edge, by design.

**The shell is SMT.** Four `SH` solder pads take the mating force. Give each
full copper to GND. The only holes are the two locating pegs.

**Put break-away rails on the left and right edges.** A rail on the mating edge
leaves a nub on the receptacle face.

The reference board at `Modules/USBC-Device-ESD/` is the worked example. Read
its `Layout-Spec.md` before you change anything the block places.

---

## 5.1 KiCad re-annotates on placement

**The block's `J1` is not your `J1`.** KiCad renumbers the references unless you
tick `keep_annotations` in the design block chooser. The custom rule in §4 names
`J1`.

Read the net names, not the designators, when you check the placed block against
`Layout-Spec.md`.

## 5.2 Set the power pads to solid after placement

The module board connects J1 to the pours with **solid** pads, not thermal
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
| "Place as sheet" **on** | The block gets its own page and title block. It prints whole | `/USBC-Device-ESD/VPOS` |

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

Eight vias on the block's bottom edge, y 118.5 on the reference board. Each
signal via carries a 1.0 mm stub on the layer opposite its arrival, toward the
edge. **The stub has a free end by design.** DRC calls that `track_dangling`.
Land on it. Do not delete it.

An `F.Fab` label names every via.

| x | y | Net | Direction | Stub layer |
|---|---|---|---|---|
| 102.2 | 118.5 | `GND` | stitch | none |
| 105.2 | 118.5 | `GND` | stitch | none |
| 107.2 | 118.5 | `/VBUS` | out | F.Cu |
| 108.8 | 118.5 | `/VBUS` | out | F.Cu |
| 110.4 | 118.5 | `/USB_DM` | both | B.Cu |
| 112.0 | 118.5 | `/USB_DP` | both | B.Cu |
| 115.2 | 118.5 | `GND` | stitch | none |
| 118.2 | 118.5 | `GND` | stitch | none |

`/VBUS` arrives on B.Cu from a bus at y 117.0. `/USB_DM` and `/USB_DP` arrive on
F.Cu from U2.

**A differential pair crosses this block boundary.** Continue `/USB_DM` and
`/USB_DP` at 0.20 / 0.20 over In1 GND to the MCU.

**Land on both `/VBUS` vias.** One 0.3 mm via carries about 1 A. Two give margin
for the 1 A class load. `/VBUS` feeds `PowerMux-TPS2121`.

`/USB_CC1` and `/USB_CC2` do not break out. The 5.1 k pull-downs stay inside.
