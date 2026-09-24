# Working in this repository

Read `ARCHITECTURE.md` and `CONTEXT.md` first. This page is the operating rules.

## Before you touch a board

1. **Mount the Plum volume.** The design block library and the shared footprints
   live on it.
2. **Check the locks.** `ls ~*.lck`. Both `~*.kicad_pro.lck` and
   `~*.kicad_pcb.lck` must exist before any Konnect IPC write. A project manager
   open gives only the first, and every IPC call fails.
3. **Re-derive the state from the files.** Run ERC and DRC. Do not trust a
   document, including this one.

## The standing rules

1. **State a non-zero canary before you believe a check.** Append a 3 mm
   clearance rule to the `.kicad_dru`, re-run DRC, confirm the count explodes,
   then restore the file and diff it. A fall in violations is a suspect event.
2. **One requirement, one mechanism.** A `.kicad_dru` rule overrides a net class
   in both directions. Never write the same requirement twice.
3. **When your tooling and KiCad disagree, KiCad is right.** The geometry
   checkers in `Modules/analysis/` cannot see thermal spokes, pad-to-zone
   connections or dangling ends. DRC can.
4. **Render the image and look at it.** Coordinate arithmetic hides collisions.
5. **Verify by net membership, not net count.** Export the netlist before and
   after, and compare the sets of `(ref, pin)` pairs.

## Which tool

| Job | Tool |
|---|---|
| Placement, routing, vias, one at a time | Konnect MCP over IPC, KiCad open |
| Schematic edits | Konnect MCP file engine, eeschema **closed** |
| Zones | Konnect `add_copper_pour`, KiCad **closed**, then reload |
| ERC, DRC, exports, renders | `kicad-cli` |
| Edge.Cuts, layer types, net class patterns | the KiCad GUI, from a written runbook |

Never edit a `.kicad_sch`, `.kicad_pcb` or `.kicad_sym` with a text tool. A
`.kicad_dru` and an `fp-lib-table` are flat files and may be edited precisely,
with the result verified.

## Konnect signatures that cost time

```
route_trace   board, x1, y1, x2, y2, layer, width, net_name
add_via       board, x, y, net_name, pad_size, drill
delete_trace  board, uuid          # also deletes vias
```

`add_via` defaults to a 0.8 mm pad, not 0.6 mm. `add_zone` reports success and
writes nothing. `register_footprint_library` will not update an existing row.

## Building the next layout block

`Design-Blocks-Runbook.md` §7.4 holds the five checks that must pass before a
fragment is copied. The traps that cost the most on the first block:

1. A module schematic assembled from blocks keeps their `(group ...)`
   definitions. Strip them, or every placement produces extra groups.
2. A vendored footprint library must be registered **globally**.
3. `cp -X` onto the Plum volume. `cp -p` writes AppleDouble sidecars.
4. The fragment and the module share a file name. Check the path.
5. KiCad re-annotates references on placement. Never compare by designator.

## Finishing a block

A block is done when all of these hold:

- DRC: 0 errors, 0 unconnected, 0 schematic parity
- Every remaining warning classified in writing
- Every interface net reaches a breakout via, checked by counting segments
- The heat or area requirement measured on the **filled** zone
- `Host-Setup.md` written
- The fragment placed into `BlockBuilder/` and the arrivals counted
