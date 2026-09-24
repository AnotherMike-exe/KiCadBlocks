# Design Blocks Runbook

How the nine Plum design blocks were built from Plum-RFBridge, and what remains.

Written 2026-09-21. Source: `_resources/Examples/Plum-RFBridge/Plum-RFBridge.kicad_pro`, netlist export of
2026-09-01, 167 components, 152 nets. KiCad 10.0.6.

**Status: 9 of 9 schematic blocks built and verified. Module boards are next, see section 7.3.**

---

## 1. What a design block is

KiCad 10 stores a design block as a directory.

| Level | Name | Holds |
|---|---|---|
| Library | `PlumBlocks.kicad_blocks` | one directory for each block |
| Block | `<Block>.kicad_block` | the three files below |
| Files | `<Block>.kicad_sch` | the circuit fragment |
| | `<Block>.kicad_pcb` | the layout fragment, optional |
| | `<Block>.json` | description, keywords, default fields |

A design block must not contain a hierarchical subsheet. All five sheets in this
project are flat, so all five qualify.

The metadata file holds three keys, no indent, and no trailing newline. The block
name comes from the directory, not from the JSON.

```json
{
"description": "…",
"keywords": "…",
"fields": {}
}
```

## 2. Where it lives

```
${PLUM_SOLUTIONS}/Blocks/PlumBlocks.kicad_blocks
```

`PLUM_SOLUTIONS` is set in KiCad. It resolves to:

```
/Users/michaelprice/Library/Application Support/Mountain Duck/
  Volumes.noindex/SyncIn.localized/personal/Plum Solutions/KiCAD
```

The library sits in the **global** design block table.

**Warning.** Mountain Duck is a network mount. Mount the volume before you open a
project that places these blocks. If it is offline, KiCad reports a broken
library.

## 3. The nine blocks

| Block | Source | Parts | Built by |
|---|---|---|---|
| `PoE-PD-Si3402-Class1` | PoE_PD sheet | 45 | whole sheet save |
| `RF-CC1101-433` | RF sheet | 25 | whole sheet copy |
| `Ethernet-W5500-Magjack` | Ethernet sheet | 37 | whole sheet copy |
| `PowerMux-TPS2121` | Power sheet | 14 | prune |
| `Buck-5V-3V3-TPS563208` | Power sheet | 13 | prune |
| `LDO-RF-3V3-AP2112K` | Power sheet | 3 | selection save, then repair |
| `MCU-ESP32S3-MINI` | MCU sheet | 11 | prune |
| `USBC-Device-ESD` | MCU sheet | 4 | prune |
| `LED-Status-x3` | MCU sheet | 6 | prune |

### Parts in each pruned block

```
PowerMux-TPS2121        U10 C107 C108 C109 C110 C111 R70 R71 R72 R73 R74 R75 R76 TP1
Buck-5V-3V3-TPS563208   U8 C100 C101 C102 C103 C104 L30 R60 R61 R62 D22 TP2 TP3
LDO-RF-3V3-AP2112K      U9 C105 C106
MCU-ESP32S3-MINI        U1 C1 C2 C3 C4 R3 R7 R8 R9 SW1 SW2
USBC-Device-ESD         J1 U2 R1 R2
LED-Status-x3           D1 D2 D3 R4 R5 R6
```

### Rules used to draw the boundaries

1. A test point that probes a node inside the block stays in the block.
   Example: TP1 on V5_SYS, TP3 on VFB_33.
2. A test point that probes an interface signal stays out.
   Example: TP7 and TP8 probe the CC1101 lines.
3. Fiducials and mounting holes stay out of every block. They belong to a board.
4. A decoupling capacitor follows the pin it decouples, not the rail it sits on.
   V5_SYS carries capacitors from three different blocks.

## 4. The two build methods

### Whole sheet

`Save Current Sheet as Design Block` writes the sheet file **byte for byte**. No
transform. Every sheet here carries a self referential project entry keyed to its
own schematic UUID, which is what a standalone block needs.

| Sheet | Schematic UUID | Self entries |
|---|---|---|
| PoE_PD | `8c848a88…` | 58 |
| RF | `f5d5df3b…` | 38 |
| Ethernet | `b6492045…` | 64 |
| MCU | `0c5f2975…` | 43 |
| Power | `bfc24bce…` | 68 |

So a whole sheet block is a file copy plus a JSON file.

### Prune

Do **not** use `Save Selection as Design Block`. It drops items. See section 6.

Instead:

1. Copy the source sheet into the block directory.
2. Delete the components that do not belong, through Konnect
   `batch_delete_schematic_components`.
3. Compute the wires, labels, junctions, no-connect flags and power symbols that
   nothing holds any more. Delete them with Konnect `batch_delete`.
4. Delete the text notes that belong to another block. A note is prose, so
   assign it by reading it, not by geometry.
5. Run `kicad-cli sch erc --severity-all`.
6. Write the JSON.
7. Render the block to SVG and look at it. ERC does not read a note.

Step 3 uses two helper scripts in `_resources/Examples/Plum-RFBridge/analysis/helpers/`:

- `kschem.py` reads symbol geometry and maps each library pin onto the sheet.
  Validated against Konnect `get_component_nets` for rotation 0, 90 and 180.
- `prune.py` marks an item live when it sits on a kept wire or touches a pin of a
  kept component. Pins often meet with no wire between them, so both tests are
  needed. A no-connect flag lives only while its own pin lives.

## 5. Verification

Both checks ran on all nine blocks.

**KiCad ERC.** Zero real defects. These items remain, and all are normal for a
fragment:

| Item | Why |
|---|---|
| `power_pin_not_driven` | no PWR_FLAG inside a fragment |
| `pin_not_driven` | an input whose driver sits in another block |
| `isolated_pin_label` | a label that reaches one pin inside the block |
| hierarchical label, no parent | a fragment has no parent sheet |
| `footprint_link_issues` | the broken global table entry, section 7.1 |
| `lib_symbol_issues` | the same broken entry. The symbol still resolves from the block's own `lib_symbols` |

**Net membership.** Each block's netlist was exported with `kicad-cli sch export
netlist --format kicadxml` and compared net by net to
`_exports/Plum-RFBridge.net`.

```
block                         nets  exact  split  MERGED
Buck-5V-3V3-TPS563208            7      7      0       0
Ethernet-W5500-Magjack          49     49      0       0
LDO-RF-3V3-AP2112K               4      4      0       0
LED-Status-x3                    7      7      0       0
MCU-ESP32S3-MINI                44     44      0       0
PoE-PD-Si3402-Class1            37     37      0       0
PowerMux-TPS2121                10     10      0       0
RF-CC1101-433                   20     20      0       0
USBC-Device-ESD                 10     10      0       0
```

188 nets. Every one holds exactly the pins the board gives it.

## 6. The trap: a selection save drops items

`LDO-RF-3V3-AP2112K` was saved by hand, from a canvas selection of three parts.
The saved file lost:

- `#PWR025`, the GND symbol at (63.50, 121.92). C105 ground floated.
- all four junctions in the region, at (63.50, 110.49), (74.93, 110.49),
  (106.68, 110.49) and (63.50, 66.04).

KiCad ERC caught the result:

```
[pin_not_connected] @(106.68, 110.49): Symbol C106 Pin 1 [Passive, Line]
```

C106 is the output capacitor. A mid wire pin needs a junction dot.

The block was repaired through Konnect: a GND power symbol, a junction at
(106.68, 110.49), and a trim of the V5_SYS rail stub that dangled at (104.14,
66.04).

**Always run ERC on a block made from a selection.**

## 6.1 The trap ERC cannot catch: a stale note

The first pruned `PowerMux-TPS2121` carried notes about the TPS563201 buck, about
U9 the LDO, and about the mounting holes. None of them belong to a power mux. ERC
passed. The render showed it.

A text note has no electrical connection, so nothing marks it as orphaned. Read
each note and assign it by hand. Then render the block and look at the image.

## 7. What remains

### 7.1 Repoint two global library entries

Konnect cannot do this. `register_symbol_library` reports success and leaves an
existing nickname untouched, so it never updates the URI. Use the dialog.

The global `sym-lib-table` and `fp-lib-table` both point `PlumRFBridge` at
`/Users/michaelprice/Downloads/Plum-ESPHome-RfBridge/hardware/pcb/libraries/`.
That path went away with the repository split.

The libraries are now in the shared location:

```
${PLUM_SOLUTIONS}/Symbols/PlumRFBridge.kicad_sym
${PLUM_SOLUTIONS}/Footprints/PlumRFBridge.pretty
${PLUM_SOLUTIONS}/3dshapes/PlumRFBridge.3dshapes
```

The blocks need 6 symbols and 6 footprints. All of them resolve there.

1. Open **Preferences → Manage Symbol Libraries…**.
2. Change the `PlumRFBridge` row to `${PLUM_SOLUTIONS}/Symbols/PlumRFBridge.kicad_sym`.
3. Open **Preferences → Manage Footprint Libraries…**.
4. Change the `PlumRFBridge` row to `${PLUM_SOLUTIONS}/Footprints/PlumRFBridge.pretty`.

### 7.2 Remove one broken design block entry

The global design block table holds a stray from a first attempt:

```
(lib (name "${PLUM_SOLUTIONS}:Blocks")
     (uri ".../SyncIn.localized/${PLUM_SOLUTIONS}:Blocks.kicad_blocks"))
```

The variable landed inside the path. Open **Preferences → Manage Design Block
Libraries…** and delete that row. Keep the `PlumBlocks` row below it.

### 7.3 Build a standalone board for each block

Decided 2026-09-21. A layout fragment cannot carry what matters here.

A design block `.kicad_pcb` holds footprints, tracks, vias, zones, graphics and
groups. It does not hold the board outline, the netclasses or the stackup. The
Si3402-B 2 in² heat spreader and the PoE inner plane void are board wide zones, so
no fragment carries them.

The next session builds a standalone board for each block instead, to that
block's own spec. The brief, with the spec for every block, is
`Block-Modules-Handoff.md`.

### 7.4 Reversed 2026-09-24. Ship both

The module board and the block fragment are not alternatives. Ship both.

| Artefact | Carries | Role |
|---|---|---|
| `Modules/<Block>/` | everything, outline included | the worked example and the test bed |
| `PlumBlocks.kicad_blocks/<Block>.kicad_block/` | footprints, tracks, vias, zones | the droppable asset |
| `Modules/<Block>/docs/Host-Setup.md` | stackup, net classes, minimums, rules | what the fragment cannot carry |

§7.3 was right that a fragment carries no outline, net classes or stackup. It was
wrong that this makes a fragment useless. **Write those down instead.**

The `PoE-Ethernet-Si3402-W5500` zones are bounded rectangles, not board wide, so
they travel. `Host-Setup.md` names the two that do not: the inner plane void and
the isolation slot.

**The fragment is a copy of the module board, so it carries the module's own
outline.** Remove it once, in the block copy. See `GUI-Runbook.md` job 8.

**Tested 2026-09-24 and it works.** `PoE-Ethernet-Si3402-W5500` placed into an
empty project brought 82 footprints with their placement, 401 segments, 103
vias, 7 zones, 12 `F.Fab` labels, 16 `Edge.Cuts` slot lines and the `Dwgs.User`
outline reference. Connectivity held. `Modules/PoE-Ethernet-Si3402-W5500/docs/
Layout-Spec.md` §16 records the measurement.

### Before you copy a module schematic into a fragment

1. **Strip the stale group definitions.** A module assembled from blocks keeps
   one `(group ...)` for each block it was built from. They multiply on every
   placement and the wrong block gets named in the error. `grep -c '^	(group '`
   must return 0.
2. **Register the footprint library globally.** A host project cannot read
   another project's `fp-lib-table`. A project row never shadows a global one.
3. **Copy with `cp -X` onto the synced volume.** `cp -p` writes AppleDouble
   `._` sidecars, and KiCad tries to parse each one as a footprint.
4. **Move the module outline to `Dwgs.User`, do not delete it.** A host then
   sees the area the block occupies.
5. **Check the file path, not the file name.** The fragment and the module are
   both called `<Block>.kicad_pcb`.

KiCad re-annotates references on placement unless `keep_annotations` is ticked.
Never compare a placed block to its module by reference designator.

## 8. Do not change these

**C20 and C21 in `RF-CC1101-433`.** The 12 pF and 15 pF crystal load capacitors
are asymmetric on purpose. TI's SWRR046 reference sets them. This project already
made that mistake once.

**Izunia cross-check for `Ethernet-W5500-Magjack`.** Izunia hub sheet 2 uses the
same Wiznet reference with a discrete transformer, and notes that RX and TX swap
for an easier layout. Read it before you reuse this block with discrete
magnetics. See `_resources/Examples/Izunia_hub_v0.1-RC1/INDEX.md`.

## 9. The trap a design block placement springs

Found 2026-09-22, while the first module board merged two blocks.

**A pin that sits on a wire's interior connects when you place the block.**

KiCad does not connect a wire interior to a pin. It needs a junction dot. So a
sheet that routes a wire straight through a pin is correct where it stands, and
its netlist proves it.

The Design Blocks panel does not copy the sheet. It splits every crossed wire at
the pin and inserts a junction. The junction connects them. The net changes, and
nothing reports it.

### What it did

| Block | Pin | Wire through it | Result on placement |
|---|---|---|---|
| `Ethernet-W5500-Magjack` | R32.1 | a GND stub to U3 pin 23 | `XO` to GND. The 25 MHz drive dies. |
| `Ethernet-W5500-Magjack` | R30.2 | `V1V2O`, U3.22 to C60.1 | `V1V2O` to GND. The W5500 1.2 V regulator shorts. |
| `PoE-PD-Si3402-Class1` | U7.2 | `OPTO_LED_A`, R55.2 to U7.1 | The optocoupler LED shorts across. |

KiCad ERC catches the result, as `multiple_net_names` and `pin_to_pin`. It does
not catch the cause, because the source sheet is correct.

### The check

```
python3 _resources/Examples/Plum-RFBridge/analysis/helpers/pin_on_wire.py
```

It reads every block, maps each library pin onto the sheet through `kschem.py`,
and reports a pin that lies on a wire's interior with no junction. Run it after
any schematic edit, and before you save a sheet as a design block.

### The repair

Move the wire or the part until nothing crosses. Then prove it: export the
netlist before and after, and compare net by net. All three repairs above
reproduce the original netlist exactly.

**Two of the three repairs broke something on the first attempt, and only the
netlist diff showed it.** Deleting the GND stub cut U3 pin 23 off its ground,
because the stub looked dead and was not. Rerouting `OPTO_LED_A` left its label
behind on empty canvas, so the net lost its name. Neither showed up in the
pin-on-wire check. Run the diff.
