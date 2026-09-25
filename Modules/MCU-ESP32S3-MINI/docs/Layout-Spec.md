# Layout Spec — MCU-ESP32S3-MINI

The geometry of the module reference board. Every number is a decision,
and each one carries its reason and its source.

Board: 27 x 24 mm, 4 layers, 1.6 mm, PCBWay. In1 GND, In2 PWR. Vias 0.6 / 0.3.
Written 2026-09-24 as a draft. Laid out 2026-09-24. Section 6 holds the real
placement, section 6.1 the changes from the draft, and section 11 the closing
state. Two DRC error groups stay open (section 11.2).

---

## 0. Sources

| Doc | Version | Where |
|---|---|---|
| ESP32-S3 Hardware Design Guidelines (HDG) | "Release master", 2024-05-14 | `_resources/Examples/Izunia_hub_v0.1-RC1/DOC/ESP32-S3/esp-hardware-design-guidelines-en-master-esp32s3.pdf` |
| ESP32-S3 Series Datasheet | v1.8, 2023-11-24 | same folder, `esp32-s3_datasheet_en.pdf` |
| ESP32-S3-MINI-1 & MINI-1U Datasheet | v1.7, 2026-03-02 | `_resources/Research/ESP32-S3-MINI-1/esp32-s3-mini-1_mini-1u_datasheet_en.pdf`, downloaded 2026-09-24 from espressif.com |
| Footprint `PlumRFBridge:ESP32-S3-MINI-1` | `version 20221018`, Espressif official | Plum volume, `KiCAD/Footprints/PlumRFBridge.pretty` |
| Reference board | Plum-RFBridge | `_resources/Examples/Plum-RFBridge/Plum-RFBridge.kicad_pcb` |

In this HDG copy, the antenna rules are in **section 4.2 "Positioning a Module
on a Base Board"**, figures 2, 3 and 4. They are not in a section 1.4.7. The
MINI-1 datasheet v1.7 (§3.1 note) points to an HDG section named "General
Principles of PCB Layout for Modules". The 2024 copy has no section with that
name. Before layout, get the current HDG from docs.espressif.com and compare
the three figures. If the numbers changed, update this file.

## 1. The antenna rule, from HDG §4.2

1. **Put the PCB antenna outside the base board.** Put the antenna feed point
   nearest to the board. The ✓ positions in Fig. 2 and Fig. 3 are corners only.
   The positions at the middle of an edge have no ✓. Espressif does not
   recommend them.
2. **If the antenna cannot be outside the board**, keep at least **15 mm**
   clear around the antenna area: no copper, no tracks, no components. Cut the
   base board away under the antenna.
3. **Fig. 4 gives the cut-out dimensions** for a module at a corner, feed point
   toward the near side edge:
   - The cut-out extends **min 15 mm** past the antenna on the side away from
     the feed point.
   - The board edge on the feed-point side is **max 2 mm** from the module side.
   - The rest of the board top edge is **max 1 mm** past the antenna end.
   - The cut-out goes the full depth of the antenna area, so no board is under
     the antenna.
4. Test the RF in the housing (HDG §4.2, last paragraph).
5. HDG §4.5 says to keep USB, UART traces, vias, test points and headers "as far
   away from the antenna as possible".

**The HDG has no rule for GND stitching at the cut-out edge.** Do not quote
one. This spec adds perimeter GND vias from the Plum breakout convention
(section 7), not from Espressif.

### 1.1 Where the feed point is

The MINI-1 cover photo (datasheet v1.7, page 1, top view) shows the two feed
legs of the meander at the **pin 1 side** of the antenna. The pin diagram
(datasheet Fig. 3-1, top view) puts pin 1 at the top left. So the feed point is
at footprint **−X**, near (−6.5, −7.7). This comes from a photo. Before you
freeze the outline, confirm it against the Espressif land-pattern source file
(datasheet §11.1 link).

MINI-1 therefore matches HDG **Fig. 3, "antenna feed point on the left"**. The
✓ positions are 1 (top-left corner, antenna out of the top edge) and 5
(bottom-left corner, antenna out of the left edge).

## 2. Does a plain rectangle satisfy Espressif? Yes, with conditions

A rectangle satisfies HDG §4.2 when all four of these are true:

1. The antenna is **fully outside** the outline. The board edge sits on the
   antenna/body line, footprint y = −7.7.
2. The module sits at a **corner**, not at the middle of an edge.
3. The **feed side** (footprint −X, the pin 1 to 15 column) faces the near side
   edge, at **≤ 2 mm** from it (Fig. 4 limit).
4. Nothing on the board extends beside the antenna. With a straight top edge
   this is true automatically.

This is Fig. 3 position 1. It is the "strongly recommended" case. A notch is
only needed when board material must continue beside the antenna. That case
does not apply here. **Use the rectangle.** It is easier to draw with our
tooling, and it is the better RF layout.

**Why the reference board's notch does not comply.** On Plum-RFBridge, U1 is at
(151.9, 100) rot −90. Its antenna occupies x 159.6 → 164.7, y 92.3 → 107.7.
The notch is x 159.8 → 165, y 90 → 110. That puts:

- 0.2 mm of board under the antenna (x 159.6 → 159.8).
- 2.3 mm of board on **each** side of the antenna. Fig. 4 needs 15 mm on the
  non-feed side.
- The module at the middle of the right edge, which is a position without ✓.

Do not copy the reference outline.

**Two cautions for the rectangle.**

- The antenna overhangs by 5.1 mm. On a PCBWay panel, the neighbouring board or
  the rail must not be under it. Order a routed gap at that edge, not a V-score,
  and tell PCBWay the part overhangs.
- `Edge.Cuts` travels with a design block (see PoE-Ethernet Layout-Spec §8). The host
  board must also keep the antenna outside its own outline. Record this in
  `Host-Setup.md`.

## 3. The footprint

`PlumRFBridge:ESP32-S3-MINI-1`, read 2026-09-24.

| Item | Value | Source |
|---|---|---|
| Pad count | 73 pads, 65 pin numbers | file |
| Perimeter pads | 60 x 0.4 x 0.8 mm, 0.85 mm pitch | file, datasheet Fig. 11-1 |
| Corner pads 62 to 65 | 4 x 0.8 x 0.8 mm at (±7, ±7), all GND | file |
| Pin 61 (EPAD, GND) | 9 squares of 1.2 x 1.2 mm on a 1.65 mm pitch, 4.5 mm overall. The (−1.65, −1.65) square is a custom pad with a chamfered corner | file. Fig. 11-1 dimension 4.5 = 3 x 1.2 + 2 x 0.45 gap |
| Body | 15.4 x 20.5 mm. x −7.7 → 7.7, y −12.8 → 7.7 | file, datasheet Fig. 10-1 |
| Pad field | x −7.4 → 7.4, y −7.4 → 7.4 | file |
| Antenna area | footprint **−Y**. y −12.8 → −7.7, 5.1 mm deep. Datasheet says 5.05 | file, Fig. 10-1 |
| Antenna keepout | Yes. Zone "antenna keepout", `*.Cu`, x ±7.7, y −12.8 → −7.7. Tracks, vias, pads, pours and footprints not allowed | file |
| Thermal vias | None in the footprint. The module board adds them | file |
| Courtyard | x ±8.0, y −13.1 → 8.0 | file |
| Silk | Top pad row sits at y −7.4. The edge at −7.7 gives **0.3 mm**, which equals `edge_clearance` 0.3 in the PoE `.kicad_dru` | file |

The keepout covers the antenna footprint only. It is not the 15 mm clearance of
HDG §4.2. The rectangle in section 2 puts the whole zone outside the outline,
so the zone never has board copper to act on.

**`PlumRFBridge.pretty/README.md` is wrong about pin 61.** It says the
official file has "nine 0.6 x 0.6 mm" thermal pads and that 1.2 is the spacing.
The file has eight 1.2 x 1.2 rects and one custom pad with a 0.6 anchor and a
1.2 x 1.2 chamfered polygon. Fig. 11-1 gives 4.5 mm overall, which only fits
1.2 mm pads on a 1.65 mm pitch. The file is right. The README is not. Fix the
README. Do not change the footprint.

### 3.1 EPAD vias

HDG §4.3.1: connect the chip ground pad to the GND plane "through at least nine
ground vias". Use a square grid on the EPAD, put paste on the gaps and put the
vias in the gaps. Datasheet §9: soldering the EPAD is optional, but it helps
the thermal path.

The gaps between the 1.2 mm squares are 0.45 mm. A 0.6 mm via does not fit
inside a gap. Put the vias at the gap crossings, where they touch the corners
of the squares. All the copper is GND, so the contact does no harm.

| Group | Footprint (x, y) | Count |
|---|---|---|
| Inner crossings | (±0.825, ±0.825) | 4 |
| Outer gap ends | (±0.825, ±2.6) and (±2.6, ±0.825) | 8 |

That gives 12 vias, at least the nine that HDG §4.3.1 asks for. Tent both faces, as on the PoE block.

## 4. Schematic facts that drive the layout

From the block schematic, netlist exported with kicad-cli 10.0.6 and compared
by `(ref, pin)`.

| Net | Members | Layout consequence |
|---|---|---|
| `+3V3` | U1.3, C2.1, C3.1, C4.1, R3.1 | One supply pin, on the feed side |
| `EN` | U1.45, R3.2, C1.1, R9.2 | Right side, top |
| `IO0` | U1.4, R8.2 | Left side, top |
| `Net-(R8-Pad1)` | R8.1, SW1.1 | **R8 is the 220 Ω series resistor between BOOT and IO0** |
| `Net-(R9-Pad1)` | R9.1, SW2.1 | **R9 is the 220 Ω series resistor between RESET and EN** |
| `IO3` | U1.7, R7.1 | R7.2 goes to **GND** |
| `GND` | U1 1, 2, 42, 43, 46 to 65; C1 to C4 .2; R7.2; SW1/SW2 pin 2 and SH | |

R8 and R9 each connect a button to a strap or reset pin. Each button shorts its
pin to GND through 220 Ω.

- Pressing RESET gives EN = 3.3 x 220 / 10 220 = 0.071 V. The limit is
  0.25 x VDD = 0.825 V (HDG §3.2). The resistor also limits the C1 discharge
  current to 15 mA.
- Pressing BOOT gives IO0 at about 0.016 V against the internal pull-up.

The layout keeps each 220 Ω at the pin end or at the button end. Section 5
explains the choice.

Interface pins, in footprint coordinates:

| Side | Pins → nets |
|---|---|
| Left (x −7) | 13 ETH_RST, 14 ETH_CS, 15 ETH_MOSI |
| Bottom (y 7) | 16 ETH_CLK, 17 ETH_MISO, 18 ETH_INT, 19 CC1101_GDO0_TX, 20 CC1101_GDO2_RX, 23 USB_DM, 24 USB_DP, 25 LED_RF_TX, 27 LED_LEARN, 30 LED_FAULT |
| Right (x 7) | 34 CC1101_SCK, 35 CC1101_MOSI, 36 CC1101_MISO, 37 CC1101_CS |

All 17 signals are at the bottom half, or the sides below the antenna. So the
breakout goes on the **bottom edge**, opposite the antenna.

## 5. Outline and regions

All coordinates are KiCad board millimetres. The board starts at (100, 100).
U1 is at **(109.7, 107.7), rot 0**, antenna toward −Y.

Outline vertices, clockwise. It is one closed rectangle:

| # | X | Y |
|---|---|---|
| 1 | 100.0 | 100.0 |
| 2 | 127.0 | 100.0 |
| 3 | 127.0 | 124.0 |
| 4 | 100.0 | 124.0 |

| Item | X | Y | Why |
|---|---|---|---|
| Antenna, off board | 102.0 → 117.4 | 94.9 → 100.0 | Top edge on footprint y −7.7 (§2 rule 1) |
| Module body on board | 102.0 → 117.4 | 100.0 → 115.4 | |
| Feed-side strip | 100.0 → 102.0 | 100.0 → 115.4 | 2.0 mm, the Fig. 4 maximum. It holds C3 and R7 |
| EN / button column | 117.7 → 127.0 | 100.0 → 115.9 | Non-feed side. Board beyond the antenna tip along the top edge is Fig. 3 position 1 |
| Fanout band | 100.5 → 126.5 | 115.7 → 119.6 | 4 mm for the diagonal shifts of section 7 |
| Breakout rows | 100.9 → 124.0 | 119.9 and 121.5 | Section 7 |

Why 27 mm wide: 15.4 module + 2.0 strip + 9.6 for the EN parts and the
side-push buttons. The buttons need 4.35 mm of courtyard depth at the edge.
Why 24 mm tall: 15.4 body + 4.5 fanout + two rows + 2.5 to the edge.

## 6. Placement table

As placed and saved, read back from the board file. Rotation follows KiCad.
Pad positions are from `pads.py` on the saved board. An 0603 resistor pad sits
at ±0.825, an 0603 capacitor pad at ±0.775.

| Ref | X | Y | Rot | Pad 1 | Pad 2 | Reason |
|---|---|---|---|---|---|---|
| U1 | 109.7 | 107.7 | 0 | — | — | Section 5. Antenna keepout at y 94.9 → 100.0, fully off board |
| C3 100 nF | 100.96 | 102.675 | 90 | (100.96, 103.45) +3V3 | (100.96, 101.9) GND | Level with pin 3. Courtyard 0.01 mm clear of U1 |
| R7 10 k | 100.96 | 108.9 | 270 | (100.96, 108.075) IO3 | (100.96, 109.725) GND | Below pin 7 |
| C1 1 µF | 119.35 | 101.75 | 0 | (118.575, 101.75) EN | (120.125, 101.75) GND | Faces pin 45 |
| R3 10 k | 119.35 | 103.8 | 180 | (120.175, 103.8) +3V3 | (118.525, 103.8) EN | EN inboard, +3V3 to an In2 via at (121.2, 103.8) |
| R9 220 | 119.35 | 105.775 | 180 | (120.175, 105.775) → SW2.1 | (118.525, 105.775) EN | Level with SW2.1, straight track |
| SW2 RESET | 124.7 | 107.0 | 90 | (123.8, 105.775) and (123.8, 108.225) | (123.8, 107.0) GND | Actuator to the right edge |
| SW1 BOOT | 124.7 | 113.0 | 90 | (123.8, 111.775) and (123.8, 114.225) | (123.8, 113.0) GND | Actuator to the right edge |
| R8 220 | 121.15 | 111.775 | 180 | (121.975, 111.775) → SW1.1 | (120.325, 111.775) IO0 | Level with SW1.1, straight track |
| C2 22 µF 0805 | 122.0 | 118.2 | 0 | (121.05, 118.2) +3V3 | (122.95, 118.2) GND | Bulk at the +3V3 entry |
| C4 100 nF | 125.0 | 118.2 | 90 | (125.0, 118.975) +3V3 | (125.0, 117.425) GND | HF partner to C2, own In2 via at (125.0, 120.0) |

Rotated through Konnect (each loses its `(units)` block until a GUI pass
restores it): C3 90, R7 270, R3 180, R9 180, R8 180, C4 90, SW1 90, SW2 90.

### 6.1 Changes from the draft

| Item | Draft | Placed | Why |
|---|---|---|---|
| C3, R7 X | 100.85 | 100.96 | Board setup copper-to-edge is 0.5 mm for pads. At 100.85 the pad edge is 0.375 mm. At 100.96 the courtyard clears U1 by 0.01 mm and the pad edge is 0.485 mm. The 2.0 mm strip cannot meet both limits (section 11.2) |
| R9 Y | 105.85 | 105.775 | Level with SW2.1, so the track is straight |
| R8 | (121.2, 111.5) rot 90 | (121.15, 111.775) rot 180 | Pad 1 level with SW1.1 (straight track). 0.05 mm left to clear the SW1 courtyard (0.03 mm overlap at 121.2) |
| Strip +3V3 vias | (101.0, 104.8), (101.0, 105.9) | (100.96, 104.6), (100.96, 105.5) | On the C3.1 column, one straight 0.3 mm track |
| IO0 far via | about (121.2, 109.4) | (120.325, 110.7) | Directly above R8.2. B.Cu path (104.4, 104.3) → (119.6, 104.3) → (119.6, 109.975) → via |
| R7.2 GND via | (101.0, 110.85) | (100.96, 110.85) | Same column as R7 |
| Switch pad 1 pairs | not stated | Loop tracks at x 121.9 (SW2) and x 121.975 (SW1) | The two pad 1s of each switch are separate copper. DRC needs both joined. Pad 2 (GND) sits between them, so the loop goes round it on the inboard side |
| Switch GND | pour only | Tracks + vias at (122.75, 107.0), (122.75, 113.0), (125.75, 103.5), (125.75, 110.0), (125.75, 116.3) | The pour gave 1 spoke to each switch GND pad (starved_thermal) |
| U1 pads 63, 64 | pour only | 45° track to an inboard via at (104.0, 113.4) and (115.4, 113.4) | The fanout walls in both corner pads. They were unconnected islands |
| Extra GND | — | C1.2 via (121.2, 101.75), C2.2 via (122.95, 119.7) | Short return for the EN cap and the bulk cap |
| Perimeter GND stitch at 3.0 mm | proposed | Not added | Only the breakout-row GND vias. Left for a later pass |

**Why R8 sits at the button end.** The feed-side strip is 2.0 mm. After C3 and
R7 there is no room for R8 and its via. The pins 4 to 6 pad gaps are 0.45 mm,
which is less than 0.2 track + 2 x 0.2 clearance. So IO0 leaves pin 4 inboard to
a tented via at about (104.4, 104.3) under the module. It then runs on B.Cu
(HDG §4.1 allows a few signals on layer 4) to a via at (120.325, 110.7), and on
to R8.2. This is the only long net in the block.

**Why C4 is not beside pin 3.** A second 100 nF next to C3 has no GND via
anywhere in a 2 mm strip. At the entry it has one. Pin 3 gets C3 on the pin and
the In2 plane behind it.

**+3V3 to pin 3.** C3.1 → two In2 vias in the strip at (100.96, 104.6) and
(100.96, 105.5). HDG §4.3.1 asks for at least two vias where main power changes
layer. The pin 3 track is 0.3 mm (Power_1 class). The 25 mil (0.635 mm)
main power width of HDG §4.3.2 applies to the plane feed, not to the stub.

**GND for R7.2.** A via at (100.96, 110.85), above the pin 13 exit.

**The reference placement, for comparison.** Reference U1 is at
(151.9, 100, rot −90). Designators and nets match the block.

| Ref | Ref global (x, y, rot) | Offset in U1 frame | Rel rot |
|---|---|---|---|
| C1 | 157.54, 109.55, −90 | (+9.550, −5.640) | 0 |
| R3 | 155.78, 109.56, 90 | (+9.560, −3.880) | 180 |
| R9 | 154.05, 109.75, 90 | (+9.750, −2.150) | 180 |
| C3 | 156.925, 91.2, 0 | (−8.800, −5.025) | 90 |
| C4 | 153.832, 91.161, 180 | (−8.839, −1.932) | 270 |
| R7 | 150.775, 91.008, 180 | (−8.992, +1.125) | 270 |
| C2 | 156.15, 88.65, 90 | (−11.350, −4.250) | 180 |
| R8 | 154.103, 88.886, −90 | (−11.114, −2.203) | 0 |
| SW2 | 162.7, 78, 90 | (−22.0, −10.8) | 180 |
| SW1 | 162.7, 68, 90 | (−32.0, −10.8) | 180 |

Map with `global = (fx − ly, fy + lx)` for U1 at rot −90. The reference had
board on the feed side, so C2 and R8 sat 3.6 mm out from the module. Here they
cannot, because the feed-side edge is at 2 mm.

## 7. The breakout rows

Nineteen signal and GND positions in **one left-to-right order that follows
the pin order**, so no two tracks cross. They fold into two staggered rows.
Even positions go to row A (outer, y 121.5) and odd positions to row B (inner,
y 119.9). Each row is on a 1.6 mm pitch. The stagger is 0.8 mm.

Via 0.6 mm pad on 0.3 mm drill. As on the PoE block, each signal via carries a
1.0 mm stub on the opposite layer toward the edge. Row A stubs end at y 122.5.
Row B stubs end at y 120.9, between the row A vias.

| # | X | Row | Net | From pin |
|---|---|---|---|---|
| — | 100.9 | A | `GND` | pour |
| 0 | 103.0 | A | `ETH_RST` | 13, left |
| 1 | 103.8 | B | `ETH_CS` | 14, left |
| 2 | 104.6 | A | `ETH_MOSI` | 15, left |
| 3 | 105.4 | B | `ETH_CLK` | 16 |
| 4 | 106.2 | A | `ETH_MISO` | 17 |
| 5 | 107.0 | B | `ETH_INT` | 18 |
| 6 | 107.8 | A | `CC1101_GDO0_TX` | 19 |
| 7 | 108.6 | B | `CC1101_GDO2_RX` | 20 |
| 8 | 109.4 | A | `GND` | USB guard |
| 9 | 110.2 | B | `USB_DM` | 23 |
| 10 | 111.0 | A | `USB_DP` | 24 |
| 11 | 111.8 | B | `GND` | USB guard |
| 12 | 112.6 | A | `LED_RF_TX` | 25 |
| 13 | 113.4 | B | `LED_LEARN` | 27 |
| 14 | 114.2 | A | `LED_FAULT` | 30 |
| 15 | 115.0 | B | `CC1101_SCK` | 34, right |
| 16 | 115.8 | A | `CC1101_MOSI` | 35, right |
| 17 | 116.6 | B | `CC1101_MISO` | 36, right |
| 18 | 117.4 | A | `CC1101_CS` | 37, right |
| — | 119.0 | A | `+3V3` | In2 |
| — | 119.8 | B | `+3V3` | In2, second via (HDG §4.3.1) |
| — | 121.0 | A | `GND` | pour |
| — | 124.0 | A | `GND` | pour |

**Why the order.** Pins 13 to 15 leave the left side and turn down the strip.
The lowest pin (15) takes the inner lane, so it lands rightmost of the three.
Pins 34 to 37 do the same on the right. The lowest pin (34, SCK) takes the inner
lane and lands leftmost. The bottom pins shift right by ≤ 1.65 mm, apart from
LED_FAULT, which shifts left 1.45 mm under the corner. The result is planar.

**Why two rows.** 17 signals at 1.6 mm need 25.6 mm in one row. The module
bottom is 15.4 mm. Two rows fit the signals in 14.4 mm, below the module.
A row A track passes between row B vias with 1.0 mm between the pads. It needs
0.2 + 2 x 0.2 = 0.6 mm.

**Why the USB pair is not in one row.** Pins 23 and 24 are 0.85 mm apart, so
the pair lands at 110.2 / 111.0, nearly straight below. The stagger adds about
1.6 mm to DM. At USB full speed (12 Mb/s, 4 ns or slower edges) that is about
10 ps of skew and does not matter. GND vias at 109.4 and 111.8 flank the pair.

**The GND pitch.** GND stitch vias are 3.0 mm apart at the right end
(121.0, 124.0). The two USB guards sit on the 0.8 mm grid, not the 3.0 mm grid,
because their job is the pair return. Add more GND vias on a 3.0 mm pitch
along the right and bottom perimeter where the copper is free. That is Plum
practice, not an Espressif rule (section 1).

A second edge is not needed. If the rows do not route, move the four CC1101 SPI
nets to the right edge below SW1, where they already exit.

### 7.1 USB routing

HDG §4.8: put the RC near the chip, route the pair in parallel at equal length,
and give it a complete reference plane with GND copper around it.

- Target **90 Ω differential**, referenced to In1 GND. Take the width and gap
  from PCBWay's calculator for the ordered stackup. Do not reuse the `MDI`
  class (0.2 / 0.2). It targets 100 Ω.
- Length is about 5 mm from pin to via. At full speed that length is
  electrically short, and the impedance is secondary to symmetry and the
  continuous plane.
- Keep the pair at the bottom, away from the antenna (HDG §4.5).

## 8. Zones

| Layer | Net | Area | Why |
|---|---|---|---|
| F.Cu | GND | whole outline, 0.3 mm edge pull-back | Returns for the strip parts, pins 1/2 and 42/43 |
| In1.Cu | GND | whole outline, solid | HDG §4.1: layer 2 is a complete GND plane with no tracks |
| In2.Cu | +3V3 | whole outline | Board spec "In2 PWR". Only one rail, so a full plane |
| B.Cu | GND | whole outline | Stitch return. IO0 is the only track on it |

The antenna keepout is all outside the outline, so no zone has to avoid it.
Pour clearance to `Edge.Cuts` is 0.3 mm, from the PoE `.kicad_dru`
`edge_clearance`. Fill the zones, then measure. Do not trust the unfilled
outline.

HDG §4.1 prefers GND on layer 3 as well, to isolate the RF and the crystal.
Those parts are inside the module here, so +3V3 on In2 is acceptable. Record
this as a deliberate deviation.

## 9. Schematic defects and deviations found

1. **R7 is a pull-down, but the block description says pull-up.**
   `MCU-ESP32S3-MINI.json` says "the IO3 strapping pull-up". The netlist has
   R7 from IO3 to GND. GPIO3 has no internal pull (Series Datasheet v1.8
   §2.6.4). With default eFuses GPIO3 is ignored. If `EFUSE_STRAP_JTAG_SEL` is
   ever burned, GPIO3 = 0 selects pad JTAG on MTCK/MTDO/MTDI (IO39 to IO41).
   Those pins carry CC1101 MOSI, MISO and CS. A pull-up to +3V3 selects USB
   JTAG instead, which is the safer default. Decide which is intended, then fix
   the circuit or the description.
2. **No USB series 0 Ω and no capacitor footprints.** HDG §3.11 recommends
   both on D+/D−, close to the chip. HDG §4.8 refers to "the RC circuit". The
   block has neither. Add them before layout, or record the deviation.
3. `USB_DP`, `USB_DM`, `LED_FAULT`, `LED_LEARN` and `LED_RF_TX` are local
   labels. They must become hierarchical before the module is assembled.
4. UART0 (TXD0 pin 39, RXD0 pin 40) is not connected. USB is the only
   programming and recovery path. That is acceptable, but record it.
5. The ERC on a scratch copy gives 14 errors and 17 warnings. All are block
   artefacts: 12 hierarchical labels without a parent, 2 undriven power pins,
   and 17 single-pin labels. There is no circuit error.

Checked and correct: EN RC is R3 10 k / C1 1 µF (datasheet v1.7 §9), bulk
C2 22 µF (HDG §4.3.2 asks ≥ 10 µF), and switch SH pins go to GND.

## 10. Checks before you believe a number

1. Render F.Cu and look at the strip and the top edge. The pads at y 100.3 are
   0.3 mm from the edge.
2. Canary the `.kicad_dru` before the first DRC (see `CLAUDE.md`).
3. After fill, count the arrivals at each breakout via by segment, not by net
   count.
4. Confirm the feed-point side (§1.1) against Espressif's land-pattern source
   before you freeze the outline.

## 11. Closing state

Measured 2026-09-24 on the saved board with
`kicad-cli pcb drc --severity-all --schematic-parity --refill-zones`.

### 11.1 Counts

| Item | Count |
|---|---|
| Segments | 110 (17 of them are the 1.0 mm B.Cu breakout stubs) |
| Vias | 52, all 0.6 / 0.3 |
| EPAD thermal vias | 12, at the section 3.1 positions |
| Unconnected | 0 |
| Schematic parity | 0 |
| `track_dangling` | 17, one per signal stub, as intended |
| `copper_edge_clearance` (error) | 21. Open, see 11.2 |
| `hole_clearance` (error) | 8. Open, see 11.2 |
| `lib_footprint_mismatch` | 3: U1, SW1, SW2 |
| Silkscreen warnings | 27 (silk_overlap 15, silk_over_copper 6, silk_edge_clearance 6). Left for the GUI pass |
| Canary `check_import.py` | PASS. DRC 76 → 567 with the 3 mm rule |

Every signal breakout via has exactly one F.Cu arrival and one B.Cu stub,
counted by segment end points.

### 11.2 Errors closed by two scoped rules, 2026-09-24

The layout left 29 DRC errors that needed a rule decision. Two rules at the end
of the `.kicad_dru` close them. DRC now shows 0 errors, and the canary rises
from 47 to 535.

1. **"Pad to Outline", 0.30 mm, closes 21 `copper_edge_clearance`.**
   Espressif puts the board edge at footprint y −7.7, so U1 pads 46 to 60, 62
   and 65 sit 0.30 mm from the top edge. C3 and R7 sit 0.485 mm from the left
   edge. The board setup figure of 0.50 mm is a template value. 0.30 mm is the
   PCBWay routed-edge limit, and "Trace to Outline" already uses it for tracks.
2. **"SW own pads to own pegs", 0.09 mm, closes 8 `hole_clearance`.** The Alps
   SKRTLAE010 land pattern puts pad 1 and the SH pads 0.099 and 0.150 mm from
   the switch's own locating holes. The rule applies only when both items
   belong to one switch.

The GUI pass also restored U1, SW1 and SW2 from the library. Konnect IPC writes
had dropped their `(units)` block, so DRC showed 3 `lib_footprint_mismatch`.

### 11.3 Breakout table

Row A at y 121.5 (2.5 mm inside the bottom edge), row B at y 119.9. F.Fab labels
at 1.2 mm inboard (y 120.3 and 118.7), size 0.7, rotation 90.

| X | Row | Net | From U1 pin |
|---|---|---|---|
| 100.9 | A | GND | — |
| 103.0 | A | ETH_RST | 13 |
| 103.8 | B | ETH_CS | 14 |
| 104.6 | A | ETH_MOSI | 15 |
| 105.4 | B | ETH_CLK | 16 |
| 106.2 | A | ETH_MISO | 17 |
| 107.0 | B | ETH_INT | 18 |
| 107.8 | A | CC1101_GDO0_TX | 19 |
| 108.6 | B | CC1101_GDO2_RX | 20 |
| 109.4 | A | GND | USB guard |
| 110.2 | B | USB_DM | 23 |
| 111.0 | A | USB_DP | 24 |
| 111.8 | B | GND | USB guard |
| 112.6 | A | LED_RF_TX | 25 |
| 113.4 | B | LED_LEARN | 27 |
| 114.2 | A | LED_FAULT | 30 |
| 115.0 | B | CC1101_SCK | 34 |
| 115.8 | A | CC1101_MOSI | 35 |
| 116.6 | B | CC1101_MISO | 36 |
| 117.4 | A | CC1101_CS | 37 |
| 119.0 | A | +3V3 | In2, tied to C2.1 |
| 119.8 | B | +3V3 | In2, tied to C2.1 |
| 121.0 | A | GND | — |
| 124.0 | A | GND | — |

The order follows section 7 exactly and is planar. The render shows no
crossing. The 20 unconnected U1 GPIO nets are not routed.
