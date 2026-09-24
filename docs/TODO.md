# TODO

## Eight layout blocks remain

Build each one to the pattern proven on `PoE-Ethernet-Si3402-W5500`. Read
`Design-Blocks-Runbook.md` §7.4 first.

| Block | Parts | Notes |
|---|---|---|
| `Ethernet-W5500-Magjack` | 37 | Shares the jack and the W5500. Most layout carries over. Start here. |
| `RF-CC1101-433` | 25 | C20 and C21 load caps are asymmetric on purpose. Do not balance them. |
| `MCU-ESP32S3-MINI` | 11 | |
| `PowerMux-TPS2121` | 14 | |
| `Buck-5V-3V3-TPS563208` | 13 | |
| `LDO-RF-3V3-AP2112K` | 3 | |
| `USBC-Device-ESD` | 4 | |
| `LED-Status-x3` | 6 | |

Each one needs a reference board, a fragment and a `Host-Setup.md`.

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
