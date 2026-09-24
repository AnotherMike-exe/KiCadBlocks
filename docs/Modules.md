# Plum Module Reference Boards

One standalone board for each design block. Reuse happens by copying the
placement and the zones into a host board. See
`Block-Modules-Handoff.md` for the brief and
`Design-Blocks-Runbook.md` for how the blocks were built.

---

## The Ethernet split

Two modules cover every project that carries Ethernet. Pick one.

| Module | Use it when | Parts |
|---|---|---|
| `PoE-Ethernet-Si3402-W5500` | The board takes its power from the cable. | 82 |
| `Ethernet-W5500-Magjack` | The board has its own power supply. | 37 |

Both use the same Abracon ARJM11C7 magjack and the same W5500. The combined
module adds the Si3402-B converter, the Coilcraft FA2924-AL flyback
transformer, the 2.5 mm isolation barrier, the slot and the heat spreader.

**`PoE-PD-Si3402-Class1` is retired.** PoE always arrives on an Ethernet cable,
so a PoE block with no jack was never a drop-in part. Its contents live in
`PoE-Ethernet-Si3402-W5500` now.

### A warning that applies to the Ethernet only module

J2's VC1 and VC2 taps are LINE SIDE conductors. A PoE switch puts its voltage
on them whether or not the board uses it. The `Ethernet-W5500-Magjack` module
keeps those nets in their own `Line_Side` net class with a 0.4 mm clearance
rule for that reason.

That rule is a working voltage figure. It is **not** the 2.5 mm isolation
barrier. Do not add a PoE converter to that board. Use the combined module.

## Every module carries

| File | Holds |
|---|---|
| `*.kicad_pro` | 4-layer stackup, net classes, net class patterns |
| `*.kicad_dru` | PCBWay rules and the module rules, each one commented |
| `*.kicad_sch` | The design block, as the root sheet |
| `fp-lib-table`, `sym-lib-table` | Project rows for `PlumRFBridge` |
| `docs/Board-Setup.md` | The GUI values, and why the GUI |
| `docs/Layout-Spec.md` | Outline, regions, zones, via arrays, clearances |

Each module also carries its own `fp-lib-table` and `sym-lib-table`.

**A project row does NOT shadow a global row of the same nickname.** Measured
2026-09-22: the module carried a correct project row for `PlumRFBridge`, the
global row pointed at a path that no longer existed, and KiCad used the global
one. Four footprints failed to load, J1, T1, U1 and L1. The global row wins.

So the global tables must be right. Both now point at `${PLUM_SOLUTIONS}`. The
project rows stay, because they help on a machine whose global table has no
`PlumRFBridge` row at all.

## Net class patterns use a bare net name

On `Plum-RFBridge` a PoE net carries a sheet path, for example `/PoE_PD/VPOS`.
On a module the block is the root sheet, so the same net is `/VPOS`. A pattern
copied from the parent board binds to nothing, and an unbound class makes the
isolation barrier rule pass with zero hits.

## Two traps this work measured

**Konnect damages KiCad 10 board files.** `add_layer` writes broken
s-expression. `create_netclass` appends a node KiCad 10 keeps elsewhere.
`create_project` emits KiCad 9 layer ids. `set_board_size` ignores the `board`
argument and writes to whatever the PCB editor has open. Each one returns
success. Do board setup in the GUI. Open the target board before any Konnect
geometry call.

**A broken `.kicad_dru` is silent.** Measured on KiCad 10.0.6: a control board
reported "Found 1 violations", and the same board with an unterminated rule
appended reported "Found 1 violations". No error, no exit code change. KiCad
drops the whole file and falls back to defaults, so DRC returns FEWER
violations.

Prove the rules loaded by making a rule fire and counting the hits. Or open
Board Setup, Custom Rules, which does report the error.
