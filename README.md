# Plum KiCAD Blocks

Reusable PCB layout blocks for Plum Solutions boards. Nine schematic design
blocks exist. Each one gets a matching **layout** so a host project can drop in
the parts, the routing and the copper pours already proven on a reference board.

## What a block ships as

| Artefact | Where | Role |
|---|---|---|
| Reference board | `Modules/<Block>/` | the worked example, and the test bed |
| Design block fragment | `PlumBlocks.kicad_blocks/<Block>.kicad_block/` | the droppable asset |
| Host setup document | `Modules/<Block>/docs/Host-Setup.md` | the stackup, net classes and rules a fragment cannot carry |

The fragment lives outside this repository, in the shared library on the Plum
volume. See `docs/ARCHITECTURE.md`.

## Status

| Block | Schematic | Layout | Fragment |
|---|---|---|---|
| `PoE-Ethernet-Si3402-W5500` | done | **done** | **done, placement tested** |
| `Ethernet-W5500-Magjack` | done | not started | — |
| `RF-CC1101-433` | done | not started | — |
| `MCU-ESP32S3-MINI` | done | not started | — |
| `PowerMux-TPS2121` | done | not started | — |
| `Buck-5V-3V3-TPS563208` | done | not started | — |
| `LDO-RF-3V3-AP2112K` | done | not started | — |
| `USBC-Device-ESD` | done | not started | — |
| `LED-Status-x3` | done | not started | — |

`PoE-PD-Si3402-Class1` is retired. PoE always arrives on an Ethernet cable, so a
PoE block with no jack was never a drop-in part.

## Start here

1. `docs/ARCHITECTURE.md` — how the repository fits together
2. `docs/CONTEXT.md` — the domain words this project uses
3. `docs/Design-Blocks-Runbook.md` — how a block is built and what breaks
4. `Modules/PoE-Ethernet-Si3402-W5500/docs/Layout-Spec.md` — the worked example

## Requirements

KiCad 10.0.6 or later. The Plum volume must be mounted, because the design block
library and the shared footprints live on it.
