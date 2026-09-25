# Host setup for the PoE-Ethernet-Si3402-W5500 block

A design block carries footprints, tracks, vias and zones. **It does not carry
the board outline, the net classes, the stackup or the custom rules.** Set those
in the host board first. Then place the block.

If you skip this page, the block places and DRC passes, because the rules that
would fail are not there.

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

**In1.Cu must be typed `power`, not `signal`.** The 0.10 mm prepreg under F.Cu
is what carries the return path for every MDI pair. A thicker dielectric there
changes the impedance.

Surface finish **ENIG**. U4 is a 0.5 mm pitch LQFP-48.

---

## 2. Net classes

| Class | Track | Clearance | Via | Diff pair |
|---|---|---|---|---|
| `Default` | 0.20 | 0.20 | 0.6 / 0.3 | 0.20 / 0.25 |
| `MDI` | 0.20 | 0.20 | 0.6 / 0.3 | 0.20 / 0.20 |
| `Power_1` | 0.3048 | 0.1524 | 0.6 / 0.3 | — |
| `Power_2` | 0.508 | 0.1524 | 0.6 / 0.3 | — |
| `GND_SYS` | — | 0.1524 | — | — |
| `GND_PRI` | — | 0.20 | — | — |
| `PoE_Primary` | — | 0.20 | — | — |
| `PoE_Load` | — | 0.20 | — | — |
| `Chassis` | — | 0.40 | — | — |

### Patterns

Use plain net names. **A sheet path pattern binds to nothing here**, because the
block's nets arrive under the host's own sheet.

```
PoE_Primary   /VPOS /VDD_PRI /CLAMP_MID /COMP_PRI /CT1_NET /CT2_NET
              /EROUT /RCL /RDET /SP1_NET /SP2_NET /SWO
              /POE_VC1P /POE_VC1N /POE_VC2P /POE_VC2N
              unconnected-(U1-*)
              unconnected-(T1-MECH_NC-Pad3) ...Pad4 ...Pad5
GND_PRI       /VNEG /VSS_PRI
PoE_Load      /POE_5V /VOUT_RAW
GND_SYS       GND
Power_1       +3V3 /3V3A
MDI           /TXP_MDI /TXN_MDI /RXP_T /RXN_T
              /TXP_CHIP /TXN_CHIP /RXP_CHIP /RXN_CHIP
              /MDI_RDP /MDI_RDN
Chassis       /CGND
```

**Check the class column in the net inspector after you place the block.** An
unbound class makes the isolation rule pass with zero hits.

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

Copy `PoE-Ethernet-Si3402-W5500.kicad_dru` into the host project and merge it.
It holds 26 rules. Four matter most.

1. **The 2.5 mm isolation barrier.** Primary copper to secondary copper. The
   rule excludes anything inside J1's courtyard, because the jack interleaves
   line-side and chip-side pins in one pad field at 1.27 mm pitch. No layout
   reaches 2.5 mm inside that field.
2. **`Chassis clearance` 0.4 mm.** `/CGND` reaches GND only through C39.
3. **"J1 line-side pads", 1.0 mm.** Added 2026-09-25 (review R1-2). Chip-side
   copper keeps 1.0 mm from J1's VC pads. The barrier's J1 exception no longer
   hides chip-side tracks inside the jack courtyard.
4. **Hole to hole 0.35 mm, scoped to `U4.insideCourtyard`.** The SPI fanout runs
   0.50 mm vias on 0.30 mm drills at 0.70 mm pitch. It applies nowhere else.

**Confirm the file loaded.** Open Board Setup → Custom Rules. A syntax error
disables the whole file, and the command line reports nothing.

---

## 5. What the block does not bring

| Item | Why | What to do |
|---|---|---|
| Board outline | A block carries no outline | Draw the host outline |
| Isolation slot | — | **It travels.** Measured 2026-09-24 |
| Inner plane void under the primary island | A board wide zone | Re-draw it. `Layout-Spec.md` §7 |
| Heat spreader area | Measured on the filled zone | Re-measure. 2 in² minimum |

The reference board at `Modules/PoE-Ethernet-Si3402-W5500/` is the worked
example. Read its `Layout-Spec.md` before you change anything the block places.

---

## 5.1 KiCad re-annotates on placement

**The block's `U4` is not your `U4`.** KiCad renumbers the references unless you
tick `keep_annotations` in the design block chooser. Values agreed for only 23 of
82 references in the reference test.

Read the net names, not the designators, when you check the placed block against
`Layout-Spec.md`.

## 5.3 Place as sheet: the net names change

Two ways to place this block. Both bring the same layout.

| Option in the Design Blocks panel | The schematic | The net names |
|---|---|---|
| "Place as sheet" **off** | The symbols land on the host's own page | `/VPOS`, as in the patterns above |
| "Place as sheet" **on** | The block gets its own page and title block. It prints whole | `/PoE-Ethernet-Si3402-W5500/VPOS` |

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

Twelve vias on the block's bottom edge, y 131.5 on the reference board. Each
signal via carries a 1.0 mm stub on the far layer. **The stub has a free end by
design.** DRC calls that `track_dangling`. Land on it, do not delete it.

Every via is labelled on `F.Fab`.

| x offset from the GND at 131.0 | Net |
|---|---|
| 0.0 | `GND` |
| 3.0 | `GND` |
| 6.0 | `GND` |
| 9.0 | `GND` |
| 12.3 | `/POE_5V` |
| 13.9 | `/ETH_CS` |
| 15.5 | `/ETH_CLK` |
| 17.1 | `/ETH_MISO` |
| 18.7 | `/ETH_MOSI` |
| 20.3 | `/ETH_INT` |
| 21.9 | `/ETH_RST` |
| 23.5 | `+3V3` |

`/ETH_RST` keeps its 4.7 k pull-up inside the block. Drive it or leave it.

`/CGND` does not break out. **No differential pair crosses the block boundary**,
so a host never matches a pair.
