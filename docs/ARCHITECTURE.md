# Architecture

## What this repository is

A workshop that turns nine schematic design blocks into nine reusable **PCB
layout** blocks. It is not one board. It holds one KiCad project for each block,
plus the documents that make a block safe to reuse.

## Layout

```
├── README.md                  project overview
├── CLAUDE.md                  symlink to docs/CLAUDE.md
├── LICENSE
├── docs/                      repository level documents
│   ├── ARCHITECTURE.md
│   ├── CONTEXT.md             the domain glossary
│   ├── CLAUDE.md
│   ├── TODO.md
│   ├── Modules.md             the module set and how to pick one
│   ├── Design-Blocks-Runbook.md
│   ├── Block-Modules-Handoff.md
│   ├── Power-Architecture.md
│   └── adr/                   decision records
├── Modules/                   one KiCad project for each block
│   ├── analysis/              geometry checkers used by every board
│   └── <Block>/
│       ├── <Block>.kicad_pro / .kicad_sch / .kicad_pcb / .kicad_dru
│       ├── libraries/         footprints this board needs
│       └── docs/              this board's own specification
├── BlockBuilder/              scratch project, used to test a fragment
└── _resources/                never committed
    ├── Examples/              Plum-RFBridge and Izunia reference projects
    └── Notes/
```

## The three artefacts of a block

A KiCad design block carries footprints, tracks, vias, zones and graphics. It
**does not** carry the board outline, the net classes or the stackup. One
artefact cannot do the job, so a block ships as three.

| Artefact | Carries | Lives |
|---|---|---|
| Reference board | everything, outline included | `Modules/<Block>/` |
| Fragment | footprints, tracks, vias, zones, graphics | the shared Plum volume |
| Host setup document | stackup, net classes, minimums, custom rules | `Modules/<Block>/docs/` |

Measured on 2026-09-24: a fragment placed into an empty project brought 82
footprints with their placement, 401 segments, 103 vias, 7 zones, 12 `F.Fab`
labels and 16 `Edge.Cuts` lines. See `adr/0003-ship-three-artefacts.md`.

## Where the shared assets live

```
${PLUM_SOLUTIONS}/Blocks/PlumBlocks.kicad_blocks/     the nine design blocks
${PLUM_SOLUTIONS}/Footprints/PoEEthModule.pretty/     module footprints
${PLUM_SOLUTIONS}/Footprints/PlumRFBridge.pretty/     RF Bridge footprints
```

`PLUM_SOLUTIONS` is a KiCad path variable. It resolves to a Mountain Duck
network mount. **Mount the volume before opening any project here.**

A footprint library a block depends on must be registered **globally**. A host
project cannot read another project's `fp-lib-table`, and a project row never
shadows a global one.

## Deliberate exceptions to the Plum standard

1. **Each module keeps its own `docs/`.** The standard puts every document in
   the repository `docs/`. A module is a self-contained KiCad project that a fab
   receives whole, so its specification travels with it. Repository level
   documents still live in the root `docs/`.
2. **`Modules/analysis/` holds tooling, not documents.** The checkers are used
   from that path by every board, and the specifications cite it.

## Verification model

Every number in a specification comes from a command, not an estimate.

| Check | Command |
|---|---|
| Electrical | `kicad-cli sch erc --severity-all` |
| Physical | `kicad-cli pcb drc --severity-all --schematic-parity --refill-zones` |
| Geometry | `python3 Modules/analysis/check_clearance.py <board> 0.15` |
| Plan, before writing | `python3 Modules/analysis/check_plan.py <board> <plan.json>` |

**State a non-zero canary before you believe a check.** A drop in violations is
a suspect event, not a success. `docs/CLAUDE.md` carries the standing rules.
