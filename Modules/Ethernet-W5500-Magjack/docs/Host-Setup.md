# Host setup for the Ethernet-W5500-Magjack block

A design block carries footprints, tracks, vias and zones. **It does not carry
the board outline, the net classes, the stackup or the custom rules.** Set those
in the host board first. Then place the block.

If you skip this page, the block places and DRC passes, because the rules that
would fail are not there.

| Item | Where |
|---|---|
| Module board | `Modules/Ethernet-W5500-Magjack/` |
| Fragment | `${PLUM_SOLUTIONS}/Blocks/PlumBlocks.kicad_blocks/Ethernet-W5500-Magjack.kicad_block/` |
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
sets the return path for every MDI pair. A thicker dielectric there changes the
impedance.

The board file sets no surface finish. Choose it with the fab. U3 is a 0.5 mm
pitch LQFP-48.

---

## 2. Net classes

| Class | Track | Clearance | Via | Diff pair |
|---|---|---|---|---|
| `Default` | 0.20 | 0.20 | 0.6 / 0.3 | 0.20 / 0.25 |
| `MDI` | 0.20 | 0.20 | 0.6 / 0.3 | 0.20 / 0.20 |
| `Power_1` | 0.3048 | 0.1524 | 0.6 / 0.3 | — |
| `GND_SYS` | — | 0.1524 | — | — |
| `Chassis` | — | 0.40 | — | — |
| `Line_Side` | — | 0.40 | — | — |

### Patterns

Use plain net names. **A sheet path pattern binds to nothing here**, because the
block's nets arrive under the host's own sheet.

```
GND_SYS     GND
Power_1     +3V3 /3V3A
MDI         /TXP_MDI /TXN_MDI /RXP_T /RXN_T
            /TXP_CHIP /TXN_CHIP /RXP_CHIP /RXN_CHIP
            /MDI_RDP /MDI_RDN
Chassis     /CGND
Line_Side   /POE_VC1P /POE_VC1N /POE_VC2P /POE_VC2N
```

**Check the class column in the net inspector after you place the block.** Every
VC net must read `Line_Side`, and `/CGND` must read `Chassis`. An unbound class
makes the 0.4 mm rules pass with zero hits.

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

Copy `Ethernet-W5500-Magjack.kicad_dru` into the host project and merge it. It
holds 25 rules: 21 shared PCBWay fab rules and 4 module rules. Three matter
most.

1. **`J2 line side clearance` 0.4 mm.** The VC nets carry PSE voltage whenever
   the cable comes from a PoE switch, even with no PoE converter on the board.
   The rule stops at J2's courtyard, because the jack interleaves line side and
   chip side pins in one pad field. Outside the courtyard the full 0.4 mm
   applies. **If you add a PoE converter, this rule is not enough.** Use
   `PoE-Ethernet-Si3402-W5500` instead.
2. **`Chassis clearance` 0.4 mm.** `/CGND` reaches GND only through C67, a
   1 nF 2 kV capacitor. It is not a ground.
3. **The U3 fanout rules.** Clearance 0.10 mm and hole to hole 0.35 mm, scoped
   to `U3.insideCourtyard`. The SPI fanout needs them. They apply nowhere else.

**The rules name `J2` and `U3`.** KiCad re-annotates on placement (§5.1). Edit
each rule to the new designator, or the rule binds to nothing.

**Confirm the file loaded.** Open Board Setup → Custom Rules. A syntax error
disables the whole file, and the command line reports nothing.

---

## 5. What the block does not bring

| Item | Why | What to do |
|---|---|---|
| Board outline | A block carries no outline. The fragment has it on `Dwgs.User` | Draw the host outline |
| Top edge at J2 | J2's nose runs 2.7 mm past the module's top edge | Put J2 on the host edge |
| F.Cu, In1.Cu and B.Cu `GND` pours | Each fills the Ethernet region, 129.5, 50.5 → 155.5, 104.5 | Join them to the host GND pours on those layers |
| In2.Cu `/3V3A` island and `GND` strip | In2 is split under U3, not a whole plane | Keep the host In2 plane out of the block area |
| Line side strip keepout | Not in the board file | Draw it if the host needs a future barrier. See below |

**The line side strip holds no pour on any layer.** The strip runs from the
module's left edge to x 129.5. `Layout-Spec.md` §6 and §8 ask for a keepout on
In1.Cu and In2.Cu over 113.0, 49.0 → 129.5, 106.0. The board file has no keepout.
If a host adds a PD beside this block, draw that rule area: forbid pours, allow
tracks and vias. The host can then draw the PoE module's 2.5 mm barrier at
x 127.0 → 129.5.

The reference board at `Modules/Ethernet-W5500-Magjack/` is the worked example.
Read its `Layout-Spec.md` before you change anything the block places.

---

## 5.1 KiCad re-annotates on placement

**The block's `U3` is not your `U3`.** KiCad renumbers the references unless you
tick `keep_annotations` in the design block chooser.

Read the net names, not the designators, when you check the placed block against
`Layout-Spec.md`.

## 6. The interface

Fifteen vias on the block's bottom edge, y 102.5 on the reference board. Each
signal via carries a 1.0 mm stub on the far layer, toward the edge. **The stub
has a free end by design.** DRC calls that `track_dangling`. Land on it. Do not
delete it.

An `F.Fab` label names every via.

| x | Offset from the GND at 131.0 | y | Net | Direction | Stub layer |
|---|---|---|---|---|---|
| 119.285 | −11.715 | 102.5 | `/POE_VC2N` | both | B.Cu |
| 120.9 | −10.1 | 102.5 | `/POE_VC1N` | both | B.Cu |
| 125.1 | −5.9 | 102.5 | `/POE_VC2P` | both | B.Cu |
| 126.7 | −4.3 | 102.5 | `/POE_VC1P` | both | B.Cu |
| 131.0 | 0.0 | 102.5 | `GND` | stitch | none |
| 134.0 | 3.0 | 102.5 | `GND` | stitch | none |
| 137.0 | 6.0 | 102.5 | `GND` | stitch | none |
| 140.0 | 9.0 | 102.5 | `GND` | stitch | none |
| 144.9 | 13.9 | 102.5 | `/ETH_CS` | in | F.Cu |
| 146.5 | 15.5 | 102.5 | `/ETH_CLK` | in | F.Cu |
| 148.1 | 17.1 | 102.5 | `/ETH_MISO` | out | F.Cu |
| 149.7 | 18.7 | 102.5 | `/ETH_MOSI` | in | F.Cu |
| 151.3 | 20.3 | 102.5 | `/ETH_INT` | out | F.Cu |
| 152.9 | 21.9 | 102.5 | `/ETH_RST` | in | F.Cu |
| 154.5 | 23.5 | 102.5 | `+3V3` | in | F.Cu |

The VC nets arrive on F.Cu. The SPI nets and `+3V3` arrive on B.Cu.

**The offsets from 131.0 onward match PoE `Host-Setup.md` §6.** A host laid out
for the PoE block takes this block without a new landing pattern. The
`/POE_5V` slot at 12.3 stays empty, because this block has no 5 V output.

**The four VC nets carry PSE voltage.** A PSE puts up to 57 V between the
pairs. Keep 0.4 mm from every other net where the host routes them.

`/ETH_RST` keeps its 4.7 k pull-up, R40, inside the block. Drive it or leave it.

`/CGND` does not break out. **No MDI pair crosses the block boundary**, so a
host never matches a pair.
