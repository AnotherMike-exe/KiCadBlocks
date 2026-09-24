# Board Setup — PoE-PD-Si3402-Class1

Enter these values once, in the KiCad GUI. Konnect cannot write KiCad 10 board
setup. Two of its tools produce broken files, and section 4 records the test.

Time: about 10 minutes.

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

Open **Board Setup → Net Classes**. Add five classes beside `Default`.

| Class | Clearance | Track width | Via dia | Via drill | Priority |
|---|---|---|---|---|---|
| `Default` | 0.1524 | 0.1524 | 0.6 | 0.3 | — |
| `GND_PRI` | 0.2 | — | — | — | 2 |
| `GND_SYS` | 0.1524 | — | — | — | 1 |
| `PoE_Load` | 0.2 | — | — | — | 0 |
| `PoE_Primary` | 0.2 | — | — | — | 3 |
| `Power_2` | 0.1524 | 0.508 | 0.6 | 0.3 | 5 |

Every via on this module is 0.3 mm drill and 0.6 mm diameter.

## 3. Net class patterns

Add these patterns in the same dialog.

**The prefix matters.** On `Plum-RFBridge` the PoE nets carry a sheet path, for
example `/PoE_PD/VPOS`. On this module the block is the root sheet, so the same
net is `/VPOS`. A pattern copied from the parent board binds to nothing, and an
unbound net class makes the isolation barrier rule pass with zero hits.

| Pattern | Net class |
|---|---|
| `/VPOS` | PoE_Primary |
| `/VDD_PRI` | PoE_Primary |
| `/CLAMP_MID` | PoE_Primary |
| `/COMP_PRI` | PoE_Primary |
| `/CT1_NET` | PoE_Primary |
| `/CT2_NET` | PoE_Primary |
| `/EROUT` | PoE_Primary |
| `/RCL` | PoE_Primary |
| `/RDET` | PoE_Primary |
| `/SP1_NET` | PoE_Primary |
| `/SP2_NET` | PoE_Primary |
| `/SWO` | PoE_Primary |
| `/POE_VC1P` | PoE_Primary |
| `/POE_VC1N` | PoE_Primary |
| `/POE_VC2P` | PoE_Primary |
| `/POE_VC2N` | PoE_Primary |
| `/VNEG` | GND_PRI |
| `/VSS_PRI` | GND_PRI |
| `unconnected-(U5-*)` | PoE_Primary |
| `unconnected-(T1-MECH_NC-Pad3)` | PoE_Primary |
| `unconnected-(T1-MECH_NC-Pad4)` | PoE_Primary |
| `unconnected-(T1-MECH_NC-Pad5)` | PoE_Primary |
| `/POE_5V` | PoE_Load |
| `/VOUT_RAW` | PoE_Load |
| `GND` | GND_SYS |

**Do not widen the three T1 entries to `unconnected-(T1-*)`.** T1 is a bridge
and its pads straddle the barrier. Pads 1 to 5 sit on the primary row. Pads 6
to 10 sit on the secondary row. Pad 6 is a MECH_NC on the SECONDARY row.
Coilcraft Document 608 rev 2021-12-22 labels pins 1 and 2 "Pri" and pins 7 to
10 "Sec", and the recommended land pattern puts 1 to 5 on one row. A wildcard
sweeps pad 6 into PoE_Primary and manufactures a false violation against its
legitimate secondary neighbour.

The 18 primary nets and the 3 T1 entries reproduce the measured fix from
`Plum-RFBridge`. That fix took the barrier rule from 29 violations to 0.

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

The file `PoE-PD-Si3402-Class1.kicad_dru` is ready. KiCad loads it
automatically because it sits beside the project and shares its name.

Open **Board Setup → Custom Rules** and confirm the editor reports no error.
A syntax error anywhere disables the whole file and KiCad stays silent about it.

## 6. Library tables

Already done. The project carries its own `fp-lib-table` and `sym-lib-table`,
each with a `PlumRFBridge` row that points at `${PLUM_SOLUTIONS}`.

A project row shadows the global row, so this module does not depend on the
global tables. Both global rows still point at
`/Users/michaelprice/Downloads/Plum-ESPHome-RfBridge/hardware/pcb/libraries/`,
which no longer exists. Fix them when convenient, in
**Preferences → Manage Footprint Libraries** and **Manage Symbol Libraries**.

## 7. Save this project as a template

Do this after steps 1 to 5 pass. It is what makes the next eight modules cheap.

1. Copy the project to
   `${PLUM_SOLUTIONS}/Templates/PlumModule4L/`.
2. Rename the four files to `PlumModule4L.*`.
3. Delete the schematic contents and the board outline.
4. Add `meta/info.html` with a one-line description.

KiCad then offers it under **File → New Project from Template**.
