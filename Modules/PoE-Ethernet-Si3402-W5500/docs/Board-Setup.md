# Board Setup — PoE-Ethernet-Si3402-W5500

The stackup, the net classes and the patterns are already written into
`PoE-Ethernet-Si3402-W5500.kicad_pro`. Your job is to open the dialogs, read
what is there, and confirm section 5.

Time: about 5 minutes.

**How the file was written.** The net class block was edited as JSON, directly,
not through Konnect. Konnect offers no tool for net classes, and its
`create_netclass` appends a node to the board file that KiCad 10 does not keep
there. A `.kicad_pro` net class block holds no UUID and no cross reference, so
JSON is safe where an s-expression edit is not. Section 4 records the tests.

---

## 1. Physical stackup

Open **File → Board Setup → Physical Stackup**.

| Field | Value |
|---|---|
| Copper layers | 4 |
| Board thickness | 1.6 mm |
| In1.Cu | power, user name `GND` |
| In2.Cu | power, user name `PWR` |

The layer order must be F.Cu, In1.Cu, In2.Cu, B.Cu. This matches
`Plum-RFBridge.kicad_pcb`, which uses layer ids 0, 4, 6 and 2.

## 2. Net classes

Open **Board Setup → Net Classes**. The project file already carries
eight classes beside `Default`. Read them, do not type them again.

| Class | Clearance | Track | Via dia | Via drill |
|---|---|---|---|---|
| `Default` | 0.2 | 0.2 | 0.6 | 0.3 |
| `GND_PRI` | 0.2 | — | — | — |
| `GND_SYS` | 0.1524 | — | — | — |
| `PoE_Load` | 0.2 | — | — | — |
| `PoE_Primary` | 0.2 | — | — | — |
| `Power_1` | 0.1524 | 0.3048 | 0.6 | 0.3 |
| `Power_2` | 0.1524 | 0.508 | 0.6 | 0.3 |
| `MDI` | 0.2 | 0.2 | 0.6 | 0.3 |
| `Chassis` | 0.4 | — | — | — |

Every via on this module is 0.3 mm drill and 0.6 mm diameter.

`MDI` also carries a differential width of 0.2 mm and a gap of 0.2 mm. That is
not a 100 ohm pair, and it does not claim to be. The reason is in the design
rules file, under "MDI pairs".

`Chassis` holds `/CGND` alone. That net carries J2's shield, tied to GND only
through C67, a 1 nF 2 kV capacitor. It is not a ground.

Net class priority breaks a tie when a net matches two patterns. No net on this
module matches two, so the priority column has no effect here.

## 3. Net class patterns

Add these patterns in the same dialog.

**The prefix matters.** On `Plum-RFBridge` the PoE nets carry a sheet path, for
example `/PoE_PD/VPOS`. On this module the block is the root sheet, so the same
net is `/VPOS`. A pattern copied from the parent board binds to nothing, and an
unbound net class makes the isolation barrier rule pass with zero hits.

The project file already carries all 38 patterns. Open **Board Setup → Net
Classes → Patterns** and read them rather than typing them again.

The 18 PoE nets are unchanged from the retired `PoE-PD-Si3402-Class1` module,
with one correction:

| Pattern | Net class | Note |
|---|---|---|
| `/SWO` | PoE_Primary | Letter O, not zero. `SWO` is the switch output. |

The Ethernet side adds:

| Pattern | Net class |
|---|---|
| `+3V3`, `/3V3A` | Power_1 |
| `/TXP_MDI`, `/TXN_MDI` | MDI |
| `/RXP_T`, `/RXN_T` | MDI |
| `/TXP_CHIP`, `/TXN_CHIP` | MDI |
| `/RXP_CHIP`, `/RXN_CHIP` | MDI |
| `/MDI_RDP`, `/MDI_RDN` | MDI |
| `/CGND` | Chassis |

The four PoE taps `/POE_VC1P`, `/POE_VC1N`, `/POE_VC2P` and `/POE_VC2N` reach
J2 pins 7, 2, 6 and 1. They stay in `PoE_Primary`. They are line side
conductors and they carry the full PSE voltage.

**Do not widen the three T1 entries to `unconnected-(T1-*)`.** T1 is a bridge
and its pads straddle the barrier. Pads 1 to 5 sit on the primary row. Pads 6
to 10 sit on the secondary row. Pad 6 is a MECH_NC on the SECONDARY row.
Coilcraft Document 608 rev 2021-12-22 labels pins 1 and 2 "Pri" and pins 7 to
10 "Sec", and the recommended land pattern puts 1 to 5 on one row. A wildcard
sweeps pad 6 into PoE_Primary and manufactures a false violation against its
legitimate secondary neighbour.

The 18 primary nets and the 3 T1 entries reproduce the measured fix from
`Plum-RFBridge`. That fix took the barrier rule from 29 violations to 0.

## 3.0 The one pattern to change after the 2026-09-22 placement

Open **Board Setup → Net Classes → Patterns**. Change one row.

| From | To | Class |
|---|---|---|
| `unconnected-(U5-*)` | `unconnected-(U1-*)` | PoE_Primary |

The Si3402-B moved from U5 to U1. Six floating pads hang on that wildcard:
`ISOSSFT_NC-Pad4`, `PLOSS-Pad5`, `SSFT_NC-Pad2`, `VPOSS_NC-Pad16`,
`VSS1_NC-Pad17` and `VSSA-Pad15`.

A floating pad lands in `Default`, and the isolation barrier rule reads
`Default` as secondary. So every genuinely primary pad within 2.5 mm of one
trips. On the parent board that produced 29 false violations. This pattern is
the measured fix.

Every other pattern binds. Checked against the netlist: 38 patterns, 81 nets,
one unbound.

`unconnected-(T1-MECH_NC-Pad6)` stays unclassed on purpose. Pad 6 sits on the
SECONDARY row. Section 3 says why.

## 3.1 Reference map, placement of 2026-09-22

**The Design Blocks panel renumbers on placement.** Every reference below comes
from the placement of 2026-09-22. A re-placement moves them, and the design
rules file names them one by one.

| Part | Old | New |
|---|---|---|
| Si3402-B | U5 | **U1** |
| Optocoupler VO618A | U7 | **U2** |
| TLV431 | U6 | **U3** |
| W5500 | U3 | **U4** |
| Magjack ARJM11C7 | J2 | **J1** |
| Y2 safety capacitors | C89, C90 | **C16, C17** |
| Shield capacitor | C67 | **C39** |
| Output inductor | L31 | **L1** |
| Transformer FA2924-AL | T1 | T1 |
| Crystal 25 MHz | Y1 | Y1 |

**Read the W5500 row twice.** It moved from U3 to U4, and U3 now holds the
TLV431. A stale `insideCourtyard('U3')` would scope the fine-pitch relaxation
onto a SOT-23 and leave the W5500 with none.

After any re-placement, export the netlist and check every pattern binds:

```
kicad-cli sch export netlist --format kicadxml -o _exports/module.xml <sheet>
```

Then compare the pattern list against the net names. An unbound pattern makes
the isolation barrier rule pass with zero hits.

## 4. Why the GUI, and not Konnect

Tested in this project on 2026-09-22, against KiCad 10.0.6.

| Konnect tool | Result |
|---|---|
| `create_project` | Writes KiCad 9 layer numbering. B.Cu becomes 31, Edge.Cuts 44. KiCad 10 uses 2 and 25. |
| `add_layer` | Writes broken s-expression. It nested `In1.Cu` inside the unclosed `F.Cu` node and gave it id 1, which already belongs to F.Mask. |
| `create_netclass` | Appends a `(netclass …)` node to the board root. KiCad 10 keeps net classes in the `.kicad_pro` file, not in the board. |
| `set_board_size` | Reports `source: ipc`. It writes to whatever board the PCB editor has open, and it ignores the `board` path you give it. |

The last one is the important one. **Open the target board in the PCB editor
before you call any Konnect geometry tool.** Otherwise the write lands on
another board.

## 5. Design rules

The file `PoE-Ethernet-Si3402-W5500.kicad_dru` is ready. KiCad loads it
automatically because it sits beside the project and shares its name.

Open **Board Setup → Custom Rules** and confirm the editor reports no error.

**This step is not optional, and the command line cannot replace it.** Measured
on KiCad 10.0.6: a control board reported "Found 1 violations", and the same
board with an unterminated rule appended to its `.kicad_dru` reported "Found 1
violations" again. No error, no warning, no exit code change. `kicad-cli pcb
drc` gives you nothing. KiCad drops the whole file and falls back to built-in
defaults, so DRC returns FEWER violations, which reads as progress.

The GUI dialog does report the error. Use it.

## 6. Library tables

Already done. The project carries its own `fp-lib-table` and `sym-lib-table`,
each with a `PlumRFBridge` row that points at `${PLUM_SOLUTIONS}`.

**A project row does not shadow a global row of the same nickname.** I wrote
the opposite here earlier and it is wrong. Measured 2026-09-22: this module had
a correct project row, the global row pointed at a dead path, and KiCad used
the global one. Four footprints failed to load, J1, T1, U1 and L1.

Both global rows now point at `${PLUM_SOLUTIONS}` and all 82 footprints load.
The project rows stay, because they help on a machine whose global table has no
`PlumRFBridge` row at all.

## 7. Save this project as a template

Do this after steps 1 to 5 pass. It is what makes the next eight modules cheap.

1. Copy the project to
   `${PLUM_SOLUTIONS}/Templates/PlumModule4L/`.
2. Rename the four files to `PlumModule4L.*`.
3. Delete the schematic contents and the board outline.
4. Add `meta/info.html` with a one-line description.

KiCad then offers it under **File → New Project from Template**.
