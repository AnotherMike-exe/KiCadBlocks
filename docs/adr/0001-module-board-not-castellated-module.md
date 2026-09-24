# 0001. A reference board, not a castellated module

Date: 2026-09-21. Status: accepted.

## Context

A block could ship as a castellated module soldered onto a host, or as a layout
a host copies.

## Decision

Ship a **reference board**. One standalone KiCad project for each block, laid
out to that block's own specification.

## Consequences

A host copies placement and routing rather than buying a part. No module
assembly, no castellation tolerance, no second fab order. The board doubles as
the test bed for the fragment.
