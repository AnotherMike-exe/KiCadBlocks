# TODO

## Eight layout blocks: done

Finished 2026-09-25. Each block has a module board, a fragment on the Plum
volume and a `Host-Setup.md`. Every board: DRC 0 errors, 0 unconnected, 0
parity, a canary that fires, every interface stub counted. Every fragment
passed the BlockBuilder placement test, copper equal by net. Two independent
reviews ran. `docs/Review-2026-09-25.md` holds the findings and dispositions.

Known limits, by scope decision (review R1-4, R1-5, R1-6): on the Ethernet and
PoE boards the W5500 decoupling caps sit 7 to 12 mm from their pins, the TX
MDI pairs have no In2 copper under them, and the crystal loop is long.

## Fab questions

1. Plugged, capped vias for the RF exposed pad (review R1-7).
2. Confirm the 0.10 mm F.Cu to In1 prepreg. The RF_50 and USB widths depend
   on it.
3. Break-away rails for boards with copper within 3.5 mm of an edge.
4. Hole-to-hole 0.35 mm under U3 and U4, and surface finish (ENIG).

## Open on the PoE block

1. Done 2026-09-24: global library rows only. The vendored copy is gone.
2. `README-FAB.md` is not written. Phase 3 work, not needed to reuse the block.
3. The slot corners are drawn sharp. A 1.0 mm router bit rounds them. Confirm
   with the fab before ordering.

## Repository

1. No CI. Nothing checks that a board still passes DRC after an edit.
2. Done 2026-09-24: `Modules/analysis/tests/` holds 16 pytest cases.
