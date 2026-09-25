# TODO

## Eight layout blocks: laid out, fragments written

Status 2026-09-24. Detail in `_resources/Notes/LayoutJobs/STATE.md` (not in git).

| Block | Board | Fragment | Placement test | Host-Setup.md |
|---|---|---|---|---|
| `Ethernet-W5500-Magjack` | done | done | open | open |
| `RF-CC1101-433` | done | done | open | open |
| `MCU-ESP32S3-MINI` | done | done | open | open |
| `PowerMux-TPS2121` | done | done | open | open |
| `Buck-5V-3V3-TPS563208` | done | done | open | open |
| `LDO-RF-3V3-AP2112K` | done | done | open | open |
| `USBC-Device-ESD` | done | done | open | open |
| `LED-Status-x3` | done | done | passed | open |

"Board done" means DRC 0 errors, 0 unconnected, 0 parity, with a canary that
fired and every interface stub counted.

Still open for these blocks:
1. Placement test in `BlockBuilder` for seven fragments.
2. `Host-Setup.md` for each block, and an independent review of each board.
3. `docs/Power-Architecture.md` gives a 1.19 V PR1 reference. SLVSEA3F gives
   1.06 V, so OV trips at 5.98 V, not 6.7 V.
4. Fab questions: plugged vias for the RF exposed pad, the 0.10 mm prepreg
   (the RF_50 and USB widths depend on it), break-away rails.

## Open on the PoE block

1. `Modules/PoE-Ethernet-Si3402-W5500/libraries/PoEEthModule.pretty` duplicates
   the global copy on the Plum volume. Keep it for offline opening, or delete it
   and rely on the global row. Decide once, apply to every block.
2. `README-FAB.md` is not written. Phase 3 work, not needed to reuse the block.
3. The slot corners are drawn sharp. A 1.0 mm router bit rounds them. Confirm
   with the fab before ordering.

## Repository

1. No CI. Nothing checks that a board still passes DRC after an edit.
2. `Modules/analysis/` has no tests. `check_plan.py` modelled a via at the wrong
   size for most of the first block.
