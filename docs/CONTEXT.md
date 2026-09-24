# Context

The words this project uses, and what each one means here.

## The block family

| Term | Meaning |
|---|---|
| **Design block** | A KiCad 10 reusable unit. A directory holding a schematic, an optional board and a JSON file. |
| **Fragment** | The `.kicad_pcb` inside a design block. Carries footprints, tracks, vias, zones and graphics. Carries no outline, net classes or stackup. |
| **Module** or **reference board** | A standalone KiCad project, one for each block. The worked example and the test bed. Lives in `Modules/`. |
| **Host** | The project a block is placed into. |
| **Breakout row** | The vias on a block's edge that a host lands on. Each signal via has a 1.0 mm stub on the far layer. |

## PoE and isolation

| Term | Meaning |
|---|---|
| **PD** | Powered Device. The board takes power from the Ethernet cable. |
| **Class 1** | A PoE power class. Up to 3.84 W at the device. |
| **Line side** | Copper galvanically tied to the cable. Hazardous. |
| **Chip side** or **secondary** | Copper on the isolated side of the transformer. |
| **Isolation barrier** | The 2.5 mm keep-out band between line side and chip side. Runs vertically at x 127 to 129.5 on the PoE module. |
| **Bridge** | A part that deliberately crosses the barrier: the transformer, the optocoupler and the two Y2 capacitors. |
| **Isolation slot** | A routed slot on the barrier centre line. Raises creepage. It does not replace the 2.5 mm clearance. |
| **Heat spreader** | The copper pour that cools the Si3402-B. AN956 asks for 2 in². Measure it on the filled zone, never on an estimate. |

## Ethernet

| Term | Meaning |
|---|---|
| **MDI** | Medium Dependent Interface. The four differential pairs between the magjack and the PHY. |
| **Magjack** | An RJ45 jack with the magnetics inside. This project uses the Abracon ARJM11C7. |
| **CT** | Centre tap. The mid-point of a transformer winding. |
| **CGND** | Chassis ground. Reaches signal ground through one capacitor only. |

## KiCad terms that mislead

| Term | What it really means here |
|---|---|
| **`track_dangling`** | On a breakout stub this is the interface, not a defect. A stub with a free end is what a host lands on. |
| **`0 unconnected`** | Proves nothing about a block's interface. A net with one pad cannot be unconnected. Count segments per net instead. |
| **Canary** | A deliberately strict rule added before a check, to prove the check runs. A count that falls to zero is a suspect event. |
| **`${KIPRJMOD}`** | Resolves to the project being opened, not to the project a library was registered from. |
| **AppleDouble** | A `._name` sidecar macOS writes when `cp -p` targets a network volume. KiCad tries to parse each one as a footprint. Use `cp -X`. |

## Layers on a module board

| Layer | Type | Carries |
|---|---|---|
| `F.Cu` | signal | routing, and the primary side pours |
| `In1.Cu` | power, `GND` | the return path for every MDI pair |
| `In2.Cu` | power, `PWR` | `GND` and `/3V3A` split |
| `B.Cu` | signal | routing, and the `VNEG` heat spreader |
| `Dwgs.User` | — | in a fragment, the block's own area outline |
