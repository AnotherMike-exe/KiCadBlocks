# GUI Runbook — PoE-Ethernet-Si3402-W5500

Four jobs that Konnect must not do. Each one is a measured trap, not a
preference. Time: about 15 minutes.

Do job 1 before any zone work. A zone fill clips to the board outline, so a
zone drawn to x 155.5 against an outline at x 154.0 fills short and reports
nothing.

---

## Job 1 — replace the board outline

The board is 56 x 84 mm. The file still carries the old 54 x 94 mm rectangle,
and that rectangle cuts through C21, FB5, C35 and C38.

**Why the GUI.** Konnect `set_board_size` reports `source: ipc` and writes to
whatever board the PCB editor has open. It ignores the board path you give it.
Konnect `add_board_outline` appends a rectangle. It does not replace one. The
parent board carried a stale rectangle under the real one for days.

1. Open the PCB editor on `PoE-Ethernet-Si3402-W5500.kicad_pcb`.
2. Select the Edge.Cuts layer.
3. Select the four existing Edge.Cuts lines. Delete them.
4. Draw a rectangle on Edge.Cuts from **(100.0, 50.0)** to **(156.0, 134.0)**.
5. Confirm the count. `Edit → Find` is not enough. Open the Appearance panel,
   hide every layer but Edge.Cuts, and look. Four lines, one closed rectangle.

## Job 2 — cut the isolation slot (DONE 2026-09-24)

Cut through Konnect. Kept here as the record. See `Layout-Spec.md` §8.1.


Four NPTH slot segments on the barrier centre line, x = 128.25, width 1.0 mm.

Draw each one on Edge.Cuts as a rounded slot, or place an NPTH pad with
`Hole_Size_X` 1.0 mm and `Hole_Size_Y` set to the length.

| Segment | Y from | Y to | Length |
|---|---|---|---|
| 1 | 68.5 | 86.75 | 18.25 mm |
| 2 | 93.75 | 97.0 | 3.25 mm |
| 3 | 113.0 | 115.2 | 2.2 mm |
| 4 | 122.8 | 124.25 | 1.45 mm |

`Layout-Spec.md` section 8 says why the slot breaks, and why it stops at
y 68.5.

## Job 3 — reload the board after a zone write

The six zones are already in the file. Konnect `add_copper_pour` wrote them.
Konnect `add_zone` does not work: it reports success and writes nothing.

`add_copper_pour` writes the FILE. `route_trace`, `add_via` and
`move_component` write the board pcbnew holds in MEMORY, and `save_project`
writes that copy over the file.

**So close the board in pcbnew and open it again after every
`add_copper_pour`, before the next Konnect geometry call.** Otherwise the next
`save_project` writes the stale copy back and every pour is gone.

1. Close the board in the PCB editor.
2. Open it again.
3. Press `B` to fill the zones.
4. Confirm six zones: F.Cu VPOS, B.Cu VNEG, and GND on F.Cu, B.Cu, In1.Cu and
   In2.Cu.

| Zone | Layer | Net | Rectangle |
|---|---|---|---|
| 1 | F.Cu | `/VPOS` | 100.5, 68.0 to 127.0, 133.0 |
| 2 | B.Cu | `/VNEG` | 100.5, 68.0 to 127.0, 133.0 |
| 3 | F.Cu | `GND` | 129.5, 50.5 to 155.5, 133.5 |
| 4 | B.Cu | `GND` | 129.5, 50.5 to 155.5, 133.5 |
| 5 | In1.Cu | `GND` | 129.5, 50.5 to 155.5, 133.5 |
| 6 | In2.Cu | `GND` | 129.5, 50.5 to 155.5, 133.5 |

No zone needs a priority, and no keepout is needed. No two zones on one layer
overlap. The inner planes stop at x 129.5, the secondary edge of the barrier
band, so the primary side carries no inner copper at all.

## Job 4 — confirm the custom rules loaded

**This step is not optional, and the command line cannot replace it.**

Measured on KiCad 10.0.6: a control board reported "Found 1 violations", and
the same board with an unterminated rule appended to its `.kicad_dru` reported
"Found 1 violations" again. No error, no warning, no exit code change. KiCad
drops the whole file and falls back to built-in defaults, so DRC returns FEWER
violations, which reads as progress.

1. Open **File → Board Setup → Custom Rules**.
2. Confirm the editor reports no error.
3. Open **Board Setup → Net Classes → Patterns**.
4. Confirm `unconnected-(U1-*)` is present and `unconnected-(U5-*)` is gone.
   The Si3402-B is U1 on this board. See `Board-Setup.md` section 3.0.
5. Open the net inspector. Read the class column. Confirm `/VPOS` and `/VNEG`
   report `PoE_Primary`, and that `/RXP_T` reports `MDI`.

An unbound net class makes the isolation barrier rule pass with zero hits.

## Job 5 — re-point the four custom footprints

**Do this before job 6.** It rewrites footprint text, and job 6 tidies that text.

The four custom footprints now live inside the module at
`libraries/PoEEthModule.pretty/`. The files are byte-identical copies of the
`PlumRFBridge` originals. The project `fp-lib-table` carries a `PoEEthModule`
row with a `${KIPRJMOD}` path, so the module opens on any machine with no
network mount.

The schematic already points at the new nickname. The board does not.

1. Open the schematic and the PCB editor.
2. In the PCB editor choose **Tools → Update PCB from Schematic**.
3. **Untick "Reset footprint text items".** Ticking it undoes a silkscreen pass.
4. Leave "Re-link footprints" unticked. The links are already right.
5. Click **Update PCB**, then save.

**Acceptance test.**

```
grep -c 'PlumRFBridge:' PoE-Ethernet-Si3402-W5500.kicad_pcb
```

It must return **0**. Before the job it returns 4.

Then run DRC. `lib_footprint_issues` must fall from 4 to 0, and every other
count must hold. **A fall in another count is a suspect event.**

### Why a new nickname

A project library table does not shadow the global one. A duplicate nickname
resolves to the global row, so reusing `PlumRFBridge` would have changed
nothing. The module needs a name that the global table does not hold.

### What still comes from PlumRFBridge

Five **symbols**: `Si3402-B`, `FA2924-AL`, `ARJM11C7-114-BA-EW2` and `TLV431`.
A `.kicad_sch` caches every symbol it uses, so the schematic opens and ERC runs
with the library absent. Vendor them too if the module ever needs an edit to
one of those symbols.

## Job 6 — move the passive refdes to F.Fab

DRC reports 73 silkscreen warnings. Every one is a reference designator that
touches another designator, a footprint outline or a pad. None is a footprint
outline crossing its own pads.

Thirty parts collide. Move the 25 passive and discrete designators to `F.Fab`.
Keep the other five on the silk, because a rework engineer needs them:
**U1** the Si3402-B, **U2** the optocoupler, **T1** the transformer, and
**TP1** and **TP2**.

Move these 25:

```
C6  C9  C14 C16 C22 C23 C24 C29 C30 C32 C33 C37
D3  L1  R3  R7  R8  R10 R12 R13 R14 R15 R16 R19 Y1
```

1. Open the PCB editor.
2. **Edit → Find**, type the first designator, press Enter, then Escape.
3. Hold Shift and click the other 24 reference texts. Use the Selection Filter
   panel and tick **Text** only, so a click does not take the footprint.
4. Press **E** for Edit Text and Graphic Properties.
5. Set **Layer** to `F.Fab`. Leave the size and the thickness alone.
6. Click OK, then save.

A faster route if the selection is hard: **Edit → Edit Text and Graphic
Properties**, scope **Reference designators**, filter by footprint field, and
set the layer for each group.

**Acceptance test.** Run this and read the count:

```
kicad-cli pcb drc --output /tmp/drc.json --format json --severity-all \
    --schematic-parity --refill-zones PoE-Ethernet-Si3402-W5500.kicad_pcb
```

`silk_over_copper` must fall from 17 to **0**. `silk_overlap` must fall from 56
to **29**, not lower.

Moving a reference cannot clear the other 29. 24 of them are a footprint
outline crossing its own pads, and no designator move touches that. See
`Layout-Spec.md` §14 for the full classification.

**A fall below 25 is a suspect event.** It means the silk layer stopped being
checked.

The assembly drawing is the authority for every designator that moves.

## Job 7 — move the U2 reference off the slot

U2 straddles the barrier, so its reference text sits on the centre line at
**128.25, 122.6**. Slot segment 4 runs from y 122.80 to 124.25 on that line.
DRC reports one `silk_edge_clearance`, and the text prints clipped.

1. In the PCB editor, select the `U2` reference text. Use the Selection Filter
   panel and tick **Text** only.
2. Drag it west to about **124.5, 122.6**. That is the primary side, clear of
   the slot.
3. Save.

**Acceptance test.** `silk_edge_clearance` must fall from 1 to 0, and
`silk_overlap` must hold at 28.

Keep U2 on the silk. It is the optocoupler, and a rework engineer needs it.

## Job 8 — prepare and test the design block fragment

The block sits at:

```
${PLUM_SOLUTIONS}/Blocks/PlumBlocks.kicad_blocks/
    PoE-Ethernet-Si3402-W5500.kicad_block/
```

Its `.kicad_pcb` is a byte copy of the module board, so it carries the module's
own outline: four `Edge.Cuts` lines at 100,50 to 156,134.

### 8a. Move the module outline to Dwgs.User in the block copy

⚠️ **The module board and the block fragment have the same file name.** Check
the path in the title bar before you edit. Editing the module by mistake breaks
its outline and raises `invalid_outline`. It happened once, on 2026-09-24.

Edit **this** file, not the one in `Modules/`:

```
${PLUM_SOLUTIONS}/Blocks/PlumBlocks.kicad_blocks/
    PoE-Ethernet-Si3402-W5500.kicad_block/PoE-Ethernet-Si3402-W5500.kicad_pcb
```

1. Select the four outline lines at 100,50 to 156,134. Do **not** select the 16
   slot lines at x 127.75 to 128.75.
2. Press **E** and set Layer to `Dwgs.User`.
3. Save.

**Move them, do not delete them.** A host then sees the area the block occupies,
which helps when placing it against other blocks. `Dwgs.User` carries no copper
and plots on no fab layer.

**Acceptance test.** `Edge.Cuts` must hold 16 lines, all between x 127.75 and
128.75. `Dwgs.User` must hold 4. Before the job, `Edge.Cuts` holds 20 and
`Dwgs.User` holds 0.

Run it on the block file:

```
python3 - <<'EOF'
import re
s=open("PoE-Ethernet-Si3402-W5500.kicad_pcb").read()
c={}
for m in re.finditer(r'\(gr_line[\s\S]{0,200}?\(layer "([^"]+)"\)', s):
    c[m.group(1)] = c.get(m.group(1), 0) + 1
print(c)
EOF
```

### 8b. Place it and report what arrives

Use `BlockBuilder` as the scratch project.

1. Open BlockBuilder.
2. Place the design block from the Design Blocks panel.
3. Write down what arrived and what did not.

Report on each of these:

| Item | Arrived? |
|---|---|
| 82 footprints | |
| 401 tracks | |
| 103 vias | |
| 7 zones | |
| The 16 `Edge.Cuts` slot lines | |
| The 12 `F.Fab` breakout labels | |
| Net names on the placed tracks | |

**The slot answer decides the next step.** If `Edge.Cuts` does not travel,
convert the slot to four NPTH oval pads inside a footprint, which does travel.
`Layout-Spec.md` §8.1 records why.

Do not build the other eight fragments until this job reports back.

## After all eight

Tell the session. The thermal via array, the stitching vias and the breakout
row follow.
