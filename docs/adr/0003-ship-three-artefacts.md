# 0003. A block ships as three artefacts

Date: 2026-09-24. Status: accepted. Supersedes 2026-09-21 "no fragment".

## Context

An earlier session found that a design block fragment carries no board outline,
no net classes and no stackup, and concluded a fragment was not worth building.

A fragment was then built and placed. It brought 82 footprints with their
placement, 401 segments, 103 vias, 7 zones, 12 `F.Fab` labels and 16
`Edge.Cuts` lines. Connectivity held.

## Decision

Ship three artefacts for each block: the reference board, the fragment, and a
`Host-Setup.md` that lists what the fragment cannot carry.

## Consequences

The earlier conclusion was half right. A fragment does carry no stackup. The
answer is to write the stackup down, not to drop the fragment. `Edge.Cuts`
travels, so an isolation slot needs no conversion to NPTH pads.
