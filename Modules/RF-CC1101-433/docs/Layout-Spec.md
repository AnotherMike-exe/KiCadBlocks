# Layout Spec — RF-CC1101-433

The geometry of the module reference board. Every number is a decision, and each
one carries its reason.

Board: 25 x 30 mm, 4 layers, 1.6 mm, PCBWay. Written 2026-09-24. Placed and
routed 2026-09-24 over IPC. Sections 3, 6, 7, 8 and 12 describe the board file as it
is now. Where they differ from the draft, the change and its reason are listed
under each table. KiCad is right where this page and the board disagree.

---

## 0. Sources

| Doc | Revision | What it gives | Local copy |
|---|---|---|---|
| TI SWRR046, CC1101EM 434 MHz reference design | 2.0.0, 2010-02-15 (project 02552) | BOM, Cadstar layout, Gerbers, pick-and-place, NC drill | `_resources/Research/CC1101/swrr046/` |
| TI SWRS061I, CC1101 data sheet | I, 2013-11-05 (package addendum 4226714/A 04/2021) | §7.8 layout rules, Table 21 BOM, RGP0020H land pattern | `_resources/Research/CC1101/cc1101.pdf` |
| KiCad 10 library `Connector_Coaxial:SMA_Amphenol_132289_EdgeMount` | KiCad 10.0 install | J3 pads and the flange line | `/Applications/KiCad/.../Connector_Coaxial.pretty` |
| `Plum-RFBridge.kicad_pcb` | local example | the routed parent board | `_resources/Examples/Plum-RFBridge/` |

The Amphenol 132289 drawing is not stored locally. amphenolrf.com returned 403 to
every download attempt. Distributors list the part as "SMA end launch jack for
0.062 in PCB, round post contact".

The SWRR046 pick-and-place is in mil. The origin is the board's bottom-left corner,
and Y points up. This file converts it to KiCad mm with Y pointing down and U1 as
the origin: `dx = (X - 2760) * 0.0254` and `dy = -(Y - 2440) * 0.0254`. The NC
drill file is offset from the pick-and-place by (-518.1, -381.7) mil. The five
14 mil vias under U1 fix that offset.

## 1. Outline and regions

All coordinates are KiCad board millimetres.

| Item | X | Y |
|---|---|---|
| Board outline | 100.0 → 125.0 | 100.0 → 130.0 |
| J3 edge (top) | 105.8 → 117.0 | 100.0 |
| RF chain band | 108.5 → 114.5 | 105.1 → 115.2 |
| Chip and decoupling | 106.3 → 122.0 | 113.7 → 123.1 |
| Breakout row | 101.5 → 121.5 | 127.5 |

J3 sits on the top edge and the breakout row on the bottom edge, as the brief
requires. The RF chain runs straight from U4 to J3, the way TI runs it. The
straight line makes a short feed possible: about 1.0 mm of bare trace from C35 to J3 as built.
`Plum-RFBridge` uses a feed of about 8 mm with a diagonal jog.

Board size comes from the part extents. The courtyards span x 105.8 → 121.9 and
y 105.7 → 123.1. The outline adds 3 mm on the right for the Y2 fence and 5 mm at
the bottom for the SPI fan-out and the breakout row.

## 2. What TI's reference layout does

SWRR046 is a 2-layer, 0.8 mm FR4 board with εr 4.5, 8 mil track and 8 mil
isolation. L2 is a solid ground plane. U1 is at rotation 90 in Cadstar. With that
rotation the RF pins (12, 13) face P3, the crystal pins (8, 10) face X1, and the
digital pins face the connectors.

**U4 at KiCad rotation 90 gives the same orientation.** A pad at local (x, y) lands
at `(fx + y, fy - x)`. So pins 11–15 face up (−y), pins 6–10 face right, pins 1–5
face down and pins 16–20 face left. Pin 1 is bottom-left, as in TI's assembly
drawing.

| U4 pin | Net | Position, U4-relative |
|---|---|---|
| 1 SCLK, 2 SO, 3 GDO2, 4 DVDD, 5 DCOUPL | bottom row | x −1.0 … +1.0, y +1.89 |
| 6 GDO0, 7 CSn, 8 XOSC_Q1, 9 AVDD, 10 XOSC_Q2 | right column | x +1.89, y +1.0 … −1.0 |
| 11 AVDD, 12 RF_P, 13 RF_N, 14 AVDD, 15 AVDD | top row | x +1.0 … −1.0, y −1.89 |
| 16 GND, 17 RBIAS, 18 DGUARD, 19 GND, 20 SI | left column | x −1.89, y −1.0 … +1.0 |

### 2.1 TI part positions, mapped to this block

Each ref maps by schematic net, and each value matches the SWRR046 BOM.

| This block | TI | Value | dx | dy | TI rot | Function |
|---|---|---|---|---|---|---|
| U4 | U1 | CC1101 | 0.00 | 0.00 | 90 | |
| C31 | C131 | 3.9 pF | −0.89 | −3.01 | 180 | balun, RF_N shunt |
| L20 | L121 | 27 nH | +1.65 | −3.00 | 0 | balun, RF_P shunt L |
| C36 | C124 | 220 pF | +2.24 | −4.43 | 270 | L121 AC ground |
| C30 | C121 | 3.9 pF | +1.14 | −4.42 | 90 | balun, RF_P series |
| L21 | L131 | 27 nH | −0.38 | −4.42 | 270 | balun, RF_N series |
| L22 | L122 | 22 nH | +0.38 | −6.12 | 270 | LC section 1 |
| C33 | C122 | 8.2 pF | −1.02 | −6.68 | 180 | LC section 1 shunt |
| L23 | L123 | 27 nH | −0.49 | −8.09 | 270 | LC section 2 |
| C34 | C123 | 5.6 pF | +0.93 | −8.64 | 0 | LC section 2 shunt |
| C35 | C125 | 220 pF | +0.38 | −10.06 | 90 | DC block |
| J3 | P3 | SMA | +0.38 | −15.11 | 0 | TI uses a vertical SMA_SMD |
| C24 | C91 | 10 nF | +3.76 | −0.18 | 0 | AVDD pin 9 |
| C25 | C111 | 220 pF | +3.10 | −3.40 | 90 | AVDD pin 11 |
| C26 | C141 | 10 nF | −3.63 | −2.69 | 180 | AVDD pin 14 |
| C27 | C151 | 220 pF | −3.63 | −1.93 | 180 | AVDD pin 15 |
| R20 | R171 | 56 k | −3.53 | −0.30 | 180 | RBIAS pin 17 |
| C28 | C181 | 220 pF | −3.53 | +0.53 | 180 | DGUARD pin 18 |
| C22 | C41 | 100 nF | +0.50 | +3.91 | 270 | DVDD pin 4 |
| C23 | C51 | 100 nF | +1.26 | +3.91 | 270 | DCOUPL pin 5 |
| C21 | C101 | 15 pF | +5.84 | −1.47 | 270 | XOSC_Q2 load |
| C20 | C81 | 12 pF | +5.84 | +1.37 | 90 | XOSC_Q1 load |
| Y2 | X1 | 26 MHz | +8.81 | +1.19 | 90 | crystal |
| FB1 | L1 | bead | +11.86 | +2.90 | 90 | supply filter |
| C29 | C1 | 1 µF | +11.86 | +6.30 | 270 | bulk, chip side of bead |

The TI rotations are Cadstar angles. TI's pad-1 side is not recorded, so do not
copy them. Section 3 gives KiCad rotations derived from the nets.

### 2.2 The rules TI's layout follows

1. **The chain is one straight column, 4.4 to 10.1 mm above the chip centre.** The
   balun (C30, C31, L20, L21, C36) sits in the first 4.5 mm. Then the two LC
   sections alternate left and right: L22/C33, then L23/C34. C35 is in line with
   the connector. Each node is pad to pad, and no node is longer than about 1 mm.
2. **Every shunt ground pad has its own via, about 0.6 mm from the pad.** The TI
   drill file shows vias beside C131 (−1.54, −4.16), C122 (−1.46, −6.06), C123
   (+1.38, −8.14) and C124 (+3.21, −5.07), with a second via on most. They are
   10 mil (0.25 mm) drill.
3. **A via fence lines both sides of the chain.** The TI vias sit at x −2.2 to −4.2
   and x +2.2 to +4.7, from y −4 to −10.7. The pitch is 0.8 to 2.5 mm.
4. **The exposed pad has 5 vias, 14 mil (0.36 mm) drill:** one at the centre and
   four at (±0.81, ±0.81) mm. The vias are tented on the component side
   (SWRS061I §7.8), so paste coverage stays under 100 % and solder cannot wick
   into the vias.
5. **Each supply pin has its own cap, placed at that pin.** The note on the block
   schematic gives the map: C24 → pin 9, C25 → 11, C26 → 14, C27 → 15, C22 → 4,
   C23 → 5, C28 → 18. SWRS061I §7.8 gives the routing order: the plane feeds the
   cap, and the cap feeds the pin. Each cap connects to the plane and to ground
   through its own vias. Do not join neighbouring supply pins directly.
6. **The crystal is to the right of the chip.** Its load caps sit between the chip
   and the crystal. SWRS061I §7.8: do not route digital signals near the
   XOSC_Q1 track or under the Q1 pad.
7. **The ground plane has no routing under the chip or under the balun and match**
   (SWRS061I §7.8).

## 3. Placement table

Rotation follows KiCad. A pad at local (x, y) lands at
`(fx + x cos t + y sin t, fy - x sin t + y cos t)`. Pad positions were read back
from the saved board with `pads.py`. `check_courtyards.py`: no overlap. The
smallest gaps are 0.02 mm (C28/R20, C31/L21, C33/L22, C33/L23).

U4 is at (111.00, 117.50), rotation 90.

| Ref | X | Y | Rot | Pad 1 side, net |
|---|---|---|---|---|
| U4 | 111.00 | 117.50 | 90 | pin 1 bottom-left |
| C31 | 110.11 | 114.09 | 180 | right, RF_N (GND left) |
| L20 | 112.65 | 114.10 | 180 | right, RF_P_SHUNT (RF_P left) |
| C30 | 112.14 | 112.68 | 90 | bottom, RF_P |
| L21 | 110.62 | 112.68 | 90 | bottom, RF_N |
| C36 | 113.24 | 112.67 | 270 | top, GND |
| L22 | 111.38 | 110.78 | 90 | bottom, BALUN_OUT |
| C33 | 109.98 | 110.22 | 0 | left, GND |
| L23 | 110.51 | 108.81 | 90 | bottom, LC_A |
| C34 | 111.93 | 108.26 | 180 | right, GND |
| C35 | 111.38 | 106.84 | 90 | bottom, LC_B (ANT_433 top) |
| J3 | 111.38 | 102.56 | 90 | pad 1 x 110.63 → 112.13, y 100.02 → 105.10 |
| C25 | 114.60 | 115.20 | 180 | right, GND |
| C24 | 115.30 | 116.75 | 180 | right, GND |
| C26 | 107.30 | 114.65 | 0 | left, GND |
| C27 | 107.30 | 115.60 | 0 | left, GND |
| R20 | 107.30 | 117.05 | 180 | right, RBIAS |
| C28 | 107.30 | 118.00 | 0 | left, GND |
| C22 | 111.30 | 121.75 | 90 | bottom, GND |
| C23 | 112.25 | 121.75 | 270 | top, DCOUPL |
| C21 | 116.84 | 116.03 | 270 | top, XTAL2 |
| C20 | 116.84 | 118.87 | 270 | top, XTAL1 |
| Y2 | 119.81 | 117.55 | 180 | pin 1 XTAL2 top-right, pin 3 XTAL1 bottom-left |
| C29 | 116.00 | 122.10 | 0 | left, GND |
| FB1 | 119.10 | 122.10 | 180 | right, +3V3_RF |

Rotated with `rotate_component` (20): U4, C31, L20, C30, L21, C36, L22, L23, C34,
C35, J3, C25, C24, R20, C22, C23, C21, C20, Y2, FB1. DRC reports
`lib_footprint_mismatch` on U4 only.

**Changes from the draft table, and why:**

- **The whole RF chain (C31 … C35) moved up 0.25 mm.** At the draft positions,
  the pin 14 VDD track has no room between the pin 14/15 pad ends (y 115.125) and
  the C31 pad bottom (y 114.65). With the chain 0.25 mm higher, the track runs at
  y 114.80 with 0.30 mm to C31 and 0.225 mm to the pin 15 pad. The C35-to-J3 gap
  becomes about 1.0 mm of bare trace.
- **C24 moved from (114.76, 117.15) to (115.30, 116.75).** At the draft position
  the C24 pads (y 116.84 → 117.46) block XOSC_Q1. Q1 cannot drop below them
  because the CSn pad sits 0.5 mm under pin 8. C24 now sits between XOSC_Q2
  (y 116.0) and XOSC_Q1 (y 117.5), with at least 0.34 mm to each.
- **C22 and C23 moved down 0.30 mm to y 121.75.** SCLK, SO and GDO2 fan out left
  under the chip. GDO2 needs the extra 0.3 mm to clear C22's VDD pad, and the C22
  feed via needs it too.
- **J3 moved down 0.02 mm, to y 102.56.** With the pads ending exactly on the
  edge, DRC reports 5 `copper_edge_clearance` errors even with the J3
  `edge_clearance min 0` rule, because touching counts as a collision. A scratch
  copy showed 0 errors at 0.02 mm inboard. The rule was not changed. Pad 1 still
  sits inside the In1 notch (x 110.38 → 112.38, y ≤ 105.33).

### 3.1 Node lengths as routed

| Node | Routed copper |
|---|---|
| RF_N | 2.57 mm (U4.13 → C31.1 → L21.1) |
| RF_P | 2.75 mm (U4.12 → L20.2 → C30.1) |
| RF_P_SHUNT | 0.96 mm |
| BALUN_OUT | 2.41 mm (two legs into L22.1) |
| LC_A | 1.85 mm |
| LC_B | 1.88 mm |
| ANT_433 | 0.17 mm track, C35.2 → J3.1 centre. About 1.0 mm is bare, between the C35 pad and the J3 pad end |
| XOSC_Q1 | 6.19 mm, U4.8 → C20.1 → Y2.3 |
| XOSC_Q2 | 10.79 mm, U4.10 → C21.1 → over Y2 at y 114.7 → Y2.1 |

## 4. The 50 Ω feed, C35 to J3

### 4.1 Result

| Item | Value | Reason |
|---|---|---|
| Structure | grounded coplanar waveguide: F.Cu over In1 GND, F.Cu GND pour both sides | the F.Cu pour exists anyway, and it carries the fence vias |
| Track width `w` | **0.17 mm** | about 49 Ω as microstrip on 0.10 mm, 35 µm Cu, εr 4.5 |
| Gap to F.Cu pour `s` | **0.25 mm** | s = 2.5 h, so the side grounds move Z by only a few ohms |
| Plain microstrip for comparison | 0.16 mm = 50.8 Ω, 0.17 mm = 49.2 Ω, 0.18 mm = 47.8 Ω | Hammerstad–Jensen with thickness correction |
| εeff | 3.37 | same model |
| λ at 433 MHz on this line | 377 mm | 692.8 mm / √3.37 |
| Feed length | 1.2 mm = 1.1° | far below any length where Z matters |

### 4.2 Method

- **Microstrip:** Hammerstad–Jensen with the Wheeler thickness correction, as in
  the KiCad calculator's microstrip model. Inputs: h 0.10, t 0.035, εr 4.5.
- **CPWG:** Ghione–Wadell conformal mapping, `Z = 60π / √εeff / (K(k)/K(k') +
  K(k3)/K(k3'))`, with `k = w/(w+2s)` and `k3 = tanh(πw/4h) / tanh(π(w+2s)/4h)`.
  For w 0.17 and s 0.25, it gives 54.6 Ω at t = 0 and 43.2 Ω with the
  Gupta thickness correction. The two results bracket the microstrip value. With
  s/h = 2.5 and t/s = 0.14, neither closed form is reliable to better than about
  ±5 Ω. Check the value in the KiCad Calculator (Coplanar wave guide with ground
  plane), and with PCBWay's impedance calculator on their confirmed stackup.
- **Why the uncertainty does not matter here:** the line is 1.1° long. A 1.2 mm
  section of 40 Ω or 60 Ω between 50 Ω ends gives a return loss better than
  −35 dB. The match components and pads have far more effect.

**If PCBWay's real prepreg is not 0.10 mm, compute the width again.** Their stock
1.6 mm 4-layer build often uses a thicker L1–L2 prepreg. At 0.20 mm, 50 Ω is
about 0.35 mm wide.

### 4.3 Stitching

| Where | Pitch | Reason |
|---|---|---|
| Both sides of ANT_433 and the chain, on the pour edge | **2.0 mm**, at 0.6 mm from track edge | λ/20 = 19 mm, so 2.0 mm is practical, not electrical. It matches TI's 0.8–2.5 mm fence. 0.6 mm = 0.25 gap + 0.3 via pad radius + 0.05 |
| Each J3 GND pad (F.Cu and B.Cu both have one) | 3 vias per pad at y 101.0, 102.5, 104.0 | joins the top and bottom leg pads to In1 at the launch |
| Each shunt GND pad (C31, C33, C34, C36) | 1 via within 0.6 mm, a second where it fits | TI rule 2 |
| Board perimeter | 3.0 mm | same as the GND breakout pitch |

Vias are 0.6/0.3 throughout. That is the standard for this board, and it is
larger than TI's 0.25 mm drill.

## 5. J3, Amphenol 132289

### 5.1 The KiCad footprint

`Connector_Coaxial:SMA_Amphenol_132289_EdgeMount`, KiCad 10 library.

| Pad | Local (x, y) | Size | Layers |
|---|---|---|---|
| 1, signal | (0, 0) | 5.08 along x, 1.5 across | F.Cu |
| 2, GND | (0, ±4.25) | 5.08 x 1.5 | F.Cu **and** B.Cu |

Pads run from local x −2.54 to +2.54. The F.Fab drawing puts the body flange face
at **local x = +2.54**, where the ground legs end and the barrel starts. The legs
reach 4.45 mm onto the board, to local x −1.91.

**The board edge sits at local x = +2.54, the outer end of the pads.**

At rotation 90, local +x points to −y. So J3's origin is 2.54 mm inside the top
edge: y = 100.00 + 2.54 = **102.54**. Pad 1 runs y 100.00 → 105.08. As built, J3 sits at 102.56, 0.02 mm inboard (§3), because a pad that touches the edge fails DRC. The GND pads
are at x 107.13 and 115.63.

The courtyard reaches 14.47 mm past the origin, to y 88.07, off the board. This
is correct for an edge launch.

### 5.2 Board thickness

The 132289 fits a 0.062 in (1.575 mm) board. The stackup here is 4 × 0.035 Cu +
0.10 + 1.24 + 0.10 = 1.58 mm, plus about 0.02 mm of mask on each side. Ask PCBWay
for **1.6 mm finished**. The legs grip a board that is 1.57–1.65 mm thick.

### 5.3 Two actions on J3

1. **A `.kicad_dru` rule so J3's pads can reach the edge.** The pads end at the
   edge by design. The general copper-to-edge clearance would flag them. Write one
   rule for `A.Parent == 'J3'`, `edge_clearance` min 0. Use nothing else for
   this requirement (standing rule 2).
2. **Cut In1 under J3 pad 1: pad plus 0.25 mm, x 110.38 → 112.38, y 100.0 →
   105.33.** Pad 1 has 7.6 mm² of area. Over 0.10 mm it forms about 3.0 pF to
   In1 (ε0·4.5·A/h). At 433 MHz that is a 122 Ω shunt, a return loss of about
   14 dB at the connector. With In1 cut, the reference is In2 GND at 1.375 mm,
   about 0.2 pF. In2 stays solid GND under J3. This cut is at the connector. It
   is not under the chip or the match, so it does not break TI rule 7.

## 6. Zone plan (as built)

The zones were written before placement. This page does not change them.

| Layer | Net | Area | Notes |
|---|---|---|---|
| F.Cu | GND | 100.5,100.5 → 124.5,129.5 | thermal-relief pads (gap 0.5, spoke 0.5). The shunt pads are made solid by a short track to their own via |
| In1.Cu | GND | same rectangle, notch x 110.38 → 112.38, y 100.5 → 105.33 under J3 pad 1 | no track on In1 |
| In2.Cu | GND | whole rectangle | **no VDD island** |
| B.Cu | GND | whole rectangle | holds the VDD jumpers (see §7) and the breakout stubs |

**Changed from the draft:** there is no In2 VDD island. SWRR046 carries VDD on
top-layer copper, with short bottom-layer jumpers where a signal crosses. This
board does the same.

## 7. Routing as built

- **U4 exposed pad:** 5 GND vias, 0.6 pad / 0.3 drill, at the centre and at
  (±0.81, ±0.81). The vias have no per-via mask override, so the board default
  applies: `tenting (front yes) (back yes)`. **They sit inside the EP's 2.4 mm
  F.Mask opening, and the four corner vias are inside the 0.97 mm paste windows at
  (±0.6, ±0.6).** The pad aperture exposes them on F.Cu whatever the via tenting
  says. D1 is still open: the footprint needs a split mask and paste round the
  vias, or the fab must fill and cap them.
- **GND pins:** pin 16 has its own via at (108.45, 116.35). Pin 19 is joined on
  F.Cu to the EP corner via at (110.19, 118.31). There is no space for a separate
  via between the pin 18 and pin 20 tracks.
- **VDD (Power_1).** F.Cu tracks, 0.3048 mm, and 0.2 mm at the QFN pads.
  FB1.2 → C29.2 → feed via (116.95, 123.35). Four crossings are unavoidable on
  F.Cu. Pins 8 and 10 (the XOSC tracks) enclose pin 9. The SPI fan-out and the RF
  chain split the left caps from the source. So a 0.3048 mm **B.Cu jumper tree**
  joins five VDD vias, the way SWRR046 uses L2:
  - (116.95, 123.35) feed at C29 → (113.95, 116.75) C24/pin 9 → (114.12, 114.35) C25/pin 11
  - branch → (111.50, 120.40) C22/pin 4 → (107.78, 118.95) C28/pin 18 and the left ring
  - The left ring is F.Cu: (107.78, 118.95) → x 104.9 → y 113.9 → C26.2 → C27.2.
    Pin 14 → C26 and pin 15 → C27 are separate tracks. Pin 18 → C28.
  - No two supply pins are joined pin to pin. The pin 9 and pin 4 vias sit on the
    short track between pin and cap, because there is no other room.
  - The B.Cu jumpers stay out from under the chip and the match. They pass under
    XOSC_Q1, which has In1 and In2 GND between.
- **XOSC_Q1:** U4.8 → (114.10, 117.50) → 45° → C20.1 (116.84, 118.39) → Y2.3. It
  runs straight, with no digital track parallel to it. CSn drops at x 113.75,
  0.40 mm from the Q1 diagonal.
- **XOSC_Q2:** U4.10 → up to y 116.0 → C21.1 → over Y2 at **y 114.7** → Y2.1.
  With the track at 115.3, as first routed, the 0.5 mm thermal gap left Y2 pad 2
  with one spoke (DRC `starved_thermal`). At 114.7 it gets two.
- **Digital lines:** MOSI leaves pin 20 and runs down x 108.7. SCLK, SO and GDO2
  fan out at 1:2 slopes to x 109.4, 109.9 and 110.4. GDO0 runs down x 113.1 and
  CSn down x 113.75. None passes under the match chain or the crystal.
- **Stitching:** 5 fence vias along the chain (110.3/112.45 at y 106.1, 109.3 at
  108.2, 112.6 at 110.3, 109.3 at 112.2), with 4 shunt vias (C31, C33, C34, C36),
  one per GND pad and each on its own track. 3 vias in each J3 GND pad. A
  perimeter ring on 3 mm pitch. One via for each decap GND pad and each Y2 GND pad.

## 8. The breakout row

Eleven vias on the bottom edge at **y = 127.5** (2.5 mm inside the edge). The
signal vias arrive on F.Cu. Each carries a 1.0 mm B.Cu stub to y 128.5. The F.Fab
labels are at y 126.3, rotation 90, size 0.7.

| x | Net | Direction | Source |
|---|---|---|---|
| 101.5 | `GND` | stitch | pour |
| 104.5 | `GND` | stitch | pour |
| 105.6 | `/CC1101_MOSI` | in | U4.20 |
| 107.2 | `/CC1101_SCK` | in | U4.1 |
| 108.8 | `/CC1101_MISO` | out | U4.2 |
| 110.4 | `/CC1101_GDO2_RX` | out | U4.3 |
| 112.0 | `/CC1101_GDO0_TX` | in | U4.6 |
| 113.6 | `/CC1101_CS` | in | U4.7 |
| 115.2 | `/+3V3_RF` | in | FB1.1 via y 124.6 |
| 118.5 | `GND` | stitch | pour |
| 121.5 | `GND` | stitch | pour |

**Changed from the draft:** the row is at y 127.5, not 128.5. The procedure puts it
2.5 mm inside the edge. The signal vias moved 0.8 mm left, onto 1.6 mm pitch from
105.6, so GDO2 lands straight below its fan-out column and +3V3_RF clears C29's
GND via. No signal track crosses another.

## 9. The reference board, for comparison

`Plum-RFBridge.kicad_pcb`: U4 at (136, 136), rotation 0. The refs and values match
this block. The nets match too: `/RF/...` there is `/...` here.

| Ref | X | Y | Rot | dx | dy |
|---|---|---|---|---|---|
| U4 | 136.000 | 136.000 | 0 | 0.00 | 0.00 |
| C20 | 132.520 | 141.850 | 180 | −3.48 | +5.85 |
| C21 | 138.900 | 141.400 | 0 | +2.90 | +5.40 |
| C22 | 133.100 | 132.420 | −90 | −2.90 | −3.58 |
| C23 | 132.420 | 137.400 | 180 | −3.58 | +1.40 |
| C24 | 140.600 | 132.520 | −90 | +4.60 | −3.48 |
| C25 | 139.200 | 132.520 | −90 | +3.20 | −3.48 |
| C26 | 132.420 | 138.600 | 0 | −3.58 | +2.60 |
| C27 | 132.420 | 136.200 | 0 | −3.58 | +0.20 |
| C28 | 136.000 | 132.420 | −90 | 0.00 | −3.58 |
| C29 | 132.200 | 130.300 | 0 | −3.80 | −5.70 |
| C30 | 141.000 | 136.900 | 0 | +5.00 | +0.90 |
| C31 | 139.200 | 134.920 | 90 | +3.20 | −1.08 |
| C33 | 144.800 | 137.480 | 90 | +8.80 | +1.48 |
| C34 | 148.000 | 137.480 | 90 | +12.00 | +1.48 |
| C35 | 149.500 | 136.250 | 0 | +13.50 | +0.25 |
| C36 | 139.200 | 139.680 | 90 | +3.20 | +3.68 |
| FB1 | 134.500 | 132.415 | −90 | −1.50 | −3.59 |
| J3 | 150.900 | 144.200 | −90 | +14.90 | +8.20 |
| L20 | 139.200 | 137.685 | 90 | +3.20 | +1.69 |
| L21 | 141.000 | 135.600 | 0 | +5.00 | −0.40 |
| L22 | 143.100 | 136.250 | 0 | +7.10 | +0.25 |
| L23 | 146.300 | 136.250 | 0 | +10.30 | +0.25 |
| R20 | 137.400 | 132.390 | 90 | +1.40 | −3.61 |
| Y2 | 135.600 | 141.000 | 180 | −0.40 | +5.00 |

All parts are on F.Cu. **This block does not copy these positions.** Three
reasons:

1. **The per-pin decoupling map is broken.** At rotation 0, pins 11–15 face right
   and pin 9 faces down. But C24 (pin 9) is top-right, C25 (pin 11) is top-right,
   and C26 and C27 (pins 14 and 15) are on the left, the side opposite their
   pins. C22 (pin 4) is 4.3 mm away. Only C23, C28 and R20 are at their pins. The
   seven caps share one net, so ERC and DRC pass.
2. **The feed is long.** C35 to J3 is a diagonal track of about 8 mm, 0.15 mm
   wide, from (149.98, 136.25) to (150.90, 144.20).
3. **J3 is 1.74 mm outside the board.** The edge is y 145.0. J3's flange line (local
   x +2.54 at rotation −90) is at y 146.74, so the pads overhang the edge.

## 10. Schematic and footprint findings

| # | Item | Finding | Action |
|---|---|---|---|
| D1 | U4 footprint `Texas_RGP0020H_…_ThermalVias` | 9 vias, 0.2 mm drill and 0.5 mm pad, on a 0.95 mm grid. All 9 are **inside the 2.4 mm F.Mask opening, so they are not tented.** The 0.85 mm paste windows at (±0.6, ±0.6) overlap the corner vias. The schematic note and TI require 5 tented vias. The 0.2 mm drill is below the board's 0.3 mm standard. | Make a project-local variant with no vias in the footprint, the EP mask split round 5 board vias (0.6/0.3, TI pattern), and paste windows clear of the vias. The alternative is PCBWay via-in-pad fill and cap. Decide before placement. |
| D2 | C20 / C21 vs SWRS061I Table 21 | The data sheet lists 27 pF / 27 pF. SWRR046 rev 2.0.0 changed them to 12 pF / 15 pF for the NX3225GA. The schematic follows SWRR046, which is correct. | None. **Never change C20 or C21.** |
| D3 | C22, C23 value text | "100nF X5R". The MPN CL05B104KB54PNC is a Samsung `B` dielectric, X7R. | Cosmetic. Correct the value text on the next schematic edit. |
| D4 | C29 value text | "1uF X7R 16V". CL21B105KBFNNNE is voltage code `B`, 50 V. | Cosmetic. Better than specified. |
| D5 | All RF values | C30/C31 3.9 pF, L20/L21 27 nH, L22 22 nH, L23 27 nH, C33 8.2 pF, C34 5.6 pF, C35/C36 220 pF, R20 56 k, FB1 1 k bead, C29 1 µF on the chip side. All match the SWRR046 434 MHz BOM, and the netlist topology matches the TI schematic node for node. | None. |
| D6 | J3 132289 | Made for a 0.062 in board. 1.6 mm finished is compatible. | Specify 1.6 mm finished to PCBWay. |

The netlist check used `kicad-cli sch export netlist` on a copy of the block
schematic in the scratchpad. The block file was not touched.

## 11. Before this spec is trusted

1. Build the board, then run ERC and DRC. Use the 3 mm clearance canary.
2. Render F.Cu and In1, and look at the chain, the EP vias and the J3 launch.
3. Run `check_courtyards.py` on the real board.
4. Check ANT_433 w/s in the KiCad Calculator and against PCBWay's stackup.
5. Count arrivals at the breakout: 7 signal vias and 4 GND vias.

## 12. Closing state (2026-09-24)

`kicad-cli pcb drc --severity-all --schematic-parity --refill-zones`:

| Item | Count |
|---|---|
| Errors | 0 |
| Unconnected | 0 |
| Schematic parity | 0 |
| `track_dangling` | 7, one per signal stub (the interface) |
| `lib_footprint_mismatch` | 1, U4, from `rotate_component`; the GUI pass restores it |
| `silk_overlap` / `silk_over_copper` | 97 / 44, left for the GUI silk pass |

- Copper: 110 segments, 67 vias (5 VDD, 55 GND, 7 signal breakout).
- Canary (`check_import.py`): PASS, DRC 149 → 661 with the 3 mm rule.
- Every interface net has segments and reaches its breakout via: MOSI 5, SCK 6,
  MISO 6, GDO2 4, GDO0 5, CS 5 and +3V3_RF 4 segments, 1 via each.
- Rendered F.Cu, B.Cu and F.Fab from a zone-refilled scratch copy, and looked at
  them. The chain is one straight column. The B.Cu VDD tree is the only B.Cu copper
  apart from the stubs.
- Open: D1 (EP vias under the paste windows). The value text on F.Fab overlaps
  everywhere (GUI pass). ANT_433 impedance is still unconfirmed against PCBWay's
  stackup (§4.2).
