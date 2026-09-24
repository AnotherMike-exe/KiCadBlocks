# 0002. A block's footprint library is registered globally

Date: 2026-09-24. Status: accepted. Supersedes a project-scoped attempt.

## Context

The PoE block uses four custom footprints. They were first vendored into the
module and registered in the module's own `fp-lib-table` with `${KIPRJMOD}`.

Placing the block into a host then failed with four "footprint not found"
errors. A host project cannot read another project's library table, and
`${KIPRJMOD}` resolves to the host.

## Decision

A footprint a block depends on lives in `${PLUM_SOLUTIONS}/Footprints/` and is
registered in the **global** table.

## Consequences

The Plum volume must be mounted to place a block. A project row never shadows a
global one, so a nickname must not be reused. The module keeps its own copy so
it still opens offline, but the global row is what resolves.
