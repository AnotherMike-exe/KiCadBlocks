# Host setup for the MCU-ESP32S3-MINI block

A design block carries footprints, tracks, vias and zones. **It does not carry
the board outline, the net classes, the stackup or the custom rules.** Set those
in the host board first. Then place the block.

If you skip this page, the block places and DRC passes, because the rules that
would fail are not there.

| Item | Where |
|---|---|
| Module board | `Modules/MCU-ESP32S3-MINI/` |
| Fragment | `${PLUM_SOLUTIONS}/Blocks/PlumBlocks.kicad_blocks/MCU-ESP32S3-MINI.kicad_block/` |
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

**Set the In1.Cu type to `power`, not `signal`.** Espressif HDG §4.1 asks for a
complete GND plane on layer 2 with no tracks. The 0.10 mm prepreg under F.Cu
sets the USB pair impedance.

The board file sets no surface finish. Choose it with the fab.

---

## 2. Net classes

| Class | Track | Clearance | Via | Diff pair |
|---|---|---|---|---|
| `Default` | 0.20 | 0.20 | 0.6 / 0.3 | 0.20 / 0.25 |
| `Power_1` | 0.3048 | 0.1524 | 0.6 / 0.3 | — |
| `GND_SYS` | — | 0.1524 | — | — |
| `USB` | 0.20 | 0.20 | 0.6 / 0.3 | 0.20 / 0.20 |

### Patterns

Use plain net names. **A sheet path pattern binds to nothing here**, because the
block's nets arrive under the host's own sheet.

```
GND_SYS   GND
Power_1   +3V3
USB       /USB_DP /USB_DM
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

Copy `MCU-ESP32S3-MINI.kicad_dru` into the host project and merge it. It holds
23 rules: 21 shared PCBWay fab rules and 2 module rules. Both matter.

1. **`Pad to Outline`, edge clearance 0.3 mm, for every pad.** Espressif puts
   the antenna end of the module at the board edge. So U1's top row pads 46 to
   60, 62 and 65 sit 0.3 mm from the edge. C3 and R7 sit 0.485 mm from the
   left edge. The board minimum of 0.5 mm flags all of them. 0.3 mm is PCBWay's
   routed-edge limit. **The rule is not scoped.** In the host it relaxes every
   pad to 0.3 mm. Scope it to U1, C3 and R7 if the host needs 0.5 mm elsewhere.
2. **`SW own pads to own pegs`, hole clearance 0.09 mm.** The Alps SKRTLAE010
   land pattern puts pad 1 and the SH pads 0.099 to 0.150 mm from the switch's
   own locating holes. The rule applies only when both items belong to one
   switch.

**Rule 2 names `SW1` and `SW2`.** KiCad re-annotates on placement (§5.1). Edit
the rule to the new designators, or it binds to nothing.

**Confirm the file loaded.** Open Board Setup → Custom Rules. A syntax error
disables the whole file, and the command line reports nothing.

---

## 5. What the block does not bring

| Item | Why | What to do |
|---|---|---|
| Board outline | A block carries no outline. The fragment has it on `Dwgs.User` | Draw the host outline. See the antenna rule below |
| F.Cu, In1.Cu, B.Cu `GND` pours | Each fills the module, 100.5, 100.5 → 126.5, 123.5 | Join them to the host GND on those layers |
| In2.Cu `+3V3` plane | Fills the module. It feeds U1 pin 3 through the vias beside C3 | Keep `+3V3` on In2 under the block |
| Antenna keepout | In U1's footprint, module y 94.9 → 100.0 | It travels. Keep it off the host board |
| SW1 and SW2 keepouts | In the switch footprints | They travel |

**U1's antenna must overhang the host edge.** This follows Espressif HDG §4.2,
Fig. 3 position 1:

1. Put the host's top edge on the module's y 100.0 line. That is footprint
   y −7.7, the line between the antenna and the body.
2. Put U1 at a host corner, not at the middle of an edge.
3. Put the feed side, footprint −X, the pin 1 to 15 column, at 2 mm or less
   from the side edge. The module strip is x 100.0 → 102.0.
4. **Put no copper, tracks, vias or parts under or beside the antenna.** If
   the antenna cannot overhang, keep 15 mm clear around it and cut the board
   away under it.

The antenna overhangs by 5.1 mm. On a panel, nothing may sit under it. Order a
routed gap at that edge, not a V-score.

The reference board at `Modules/MCU-ESP32S3-MINI/` is the worked example. Read
its `Layout-Spec.md` before you change anything the block places.

---

## 5.1 KiCad re-annotates on placement

**The block's `U1` is not your `U1`.** KiCad renumbers the references unless you
tick `keep_annotations` in the design block chooser. The custom rule in §4 names
`SW1` and `SW2`.

Read the net names, not the designators, when you check the placed block against
`Layout-Spec.md`.

## 6. The interface

Twenty-four vias in two staggered rows on the block's bottom edge. Row A is at
y 121.5. Row B is at y 119.9. Each signal via carries a 1.0 mm stub on B.Cu,
toward the edge. A row B stub ends between two row A vias. **The stub has a free
end by design.** DRC calls that `track_dangling`. Land on it. Do not delete it.

An `F.Fab` label names every via.

| x | y | Net | Direction | Stub layer |
|---|---|---|---|---|
| 100.9 | 121.5 | `GND` | stitch | none |
| 103.0 | 121.5 | `/ETH_RST` | out | B.Cu |
| 103.8 | 119.9 | `/ETH_CS` | out | B.Cu |
| 104.6 | 121.5 | `/ETH_MOSI` | out | B.Cu |
| 105.4 | 119.9 | `/ETH_CLK` | out | B.Cu |
| 106.2 | 121.5 | `/ETH_MISO` | in | B.Cu |
| 107.0 | 119.9 | `/ETH_INT` | in | B.Cu |
| 107.8 | 121.5 | `/CC1101_GDO0_TX` | out | B.Cu |
| 108.6 | 119.9 | `/CC1101_GDO2_RX` | in | B.Cu |
| 109.4 | 121.5 | `GND` | USB guard | none |
| 110.2 | 119.9 | `/USB_DM` | both | B.Cu |
| 111.0 | 121.5 | `/USB_DP` | both | B.Cu |
| 111.8 | 119.9 | `GND` | USB guard | none |
| 112.6 | 121.5 | `/LED_RF_TX` | out | B.Cu |
| 113.4 | 119.9 | `/LED_LEARN` | out | B.Cu |
| 114.2 | 121.5 | `/LED_FAULT` | out | B.Cu |
| 115.0 | 119.9 | `/CC1101_SCK` | out | B.Cu |
| 115.8 | 121.5 | `/CC1101_MOSI` | out | B.Cu |
| 116.6 | 119.9 | `/CC1101_MISO` | in | B.Cu |
| 117.4 | 121.5 | `/CC1101_CS` | out | B.Cu |
| 119.0 | 121.5 | `+3V3` | in | none |
| 119.8 | 119.9 | `+3V3` | in | none |
| 121.0 | 121.5 | `GND` | stitch | none |
| 124.0 | 121.5 | `GND` | stitch | none |

Every signal net arrives on F.Cu. The two `+3V3` vias join C2.1 on F.Cu and the
In2 plane. They carry no stub.

**A differential pair crosses this block boundary.** `/USB_DM` and `/USB_DP`
land at 110.2 and 111.0, with a GND guard on each side. Continue the pair at
0.20 / 0.20 over In1 GND. It runs at Full Speed, so the 0.8 mm stagger does not
matter.

The order follows the U1 pin order, so no two tracks cross.
