# Layout Spec — Ethernet-W5500-Magjack

The geometry of the module reference board, carried over from the
finished `PoE-Ethernet-Si3402-W5500` module. Every number is a decision, and
each one carries its reason.

Board: 42 x 55 mm, 4 layers, 1.6 mm, PCBWay. Written 2026-09-24.

**This board keeps the PoE module's coordinates.** Every part lands where its
counterpart sits on the PoE board. The outline shrinks around them. That
makes a direct comparison of the two boards possible, and it lets the placed
routing be copied rather than redrawn.

Nothing here is measured yet. Re-derive every figure from the files after
placement.

---

## 0. What exists

| Item | State, 2026-09-24 |
|---|---|
| `Ethernet-W5500-Magjack.kicad_sch` | byte-identical to the block's `.kicad_sch` |
| `Ethernet-W5500-Magjack.kicad_pcb` | empty: stackup set, 0 footprints, no outline |
| Stackup | the PoE module's. F.Cu / 0.10 prepreg / In1 `GND` / 1.24 core / In2 `PWR` / 0.10 / B.Cu |
| Net classes | `Default`, `MDI`, `Power_1`, `GND_SYS`, `Chassis`, `Line_Side` |
| `.kicad_dru` | PoE rules without the barrier. Adds `J2 line side clearance`, 0.4 mm |

The net class patterns use plain net names, so they bind on a module board.

| Class | Track | Clearance | Diff pair | Nets |
|---|---|---|---|---|
| `Default` | 0.20 | 0.20 | 0.20 / 0.25 | — |
| `MDI` | 0.20 | 0.20 | 0.20 / 0.20 | 10 MDI nets |
| `Power_1` | 0.3048 | 0.1524 | — | `+3V3`, `/3V3A` |
| `GND_SYS` | — | 0.1524 | — | `GND` |
| `Chassis` | — | 0.40 | — | `/CGND` |
| `Line_Side` | — | 0.40 | — | `/POE_VC1P` `/POE_VC1N` `/POE_VC2P` `/POE_VC2N` |

## 1. Reference mapping

37 parts. Each block reference is matched to its PoE module counterpart by
value, footprint **and** the net on every pin. The match comes from the two
exported netlists, not from the drawings.

| Block | PoE | Value | Nets that fix the match |
|---|---|---|---|
| J2 | J1 | ARJM11C7-114-BA-EW2 | all 16 pins identical |
| U3 | U4 | W5500 | all 48 pins identical |
| Y1 | Y1 | 25.000 MHz CL=12pF | XI, XTAL_B, GND |
| FB2 | FB5 | 120R@100MHz | +3V3 → /3V3A |
| C50 | C23 | 100nF | /3V3A–GND, see note |
| C51 | C24 | 100nF | /3V3A–GND, see note |
| C52 | C26 | 100nF | /3V3A–GND, see note |
| C53 | C27 | 100nF | /3V3A–GND, see note |
| C54 | C28 | 100nF | /3V3A–GND, see note |
| C55 | C29 | 100nF | /3V3A–GND, see note |
| C56 | C30 | 10uF 16V 0805 | /3V3A–GND |
| C57 | C35 | 100nF | +3V3–GND |
| C58 | C38 | 10uF 16V 0805 | +3V3–GND |
| C59 | C33 | 4.7uF 0805 | /TOCAP |
| C60 | C37 | 10nF | /V1V2O |
| C61 | C22 | 18pF NP0 | /XI |
| C62 | C25 | 18pF NP0 | /XTAL_B |
| C63 | C36 | 22nF | /TCT |
| C64 | C31 | 6.8nF | /MDI_RDP – /RXP_T |
| C65 | C32 | 6.8nF | /MDI_RDN – /RXN_T |
| C66 | C34 | 10nF | /RCT |
| C67 | C39 | 1nF 2kV 1808 | /CGND |
| R30 | R17 | 12.4k 1% | /EXRES1 |
| R31 | R10 | 1M | /XI – /XO |
| R32 | R12 | 0R | /XO – /XTAL_B |
| R33 | R18 | 49R9 1% | /3V3A – /TXP_MDI |
| R34 | R20 | 49R9 1% | /3V3A – /TXN_MDI |
| R35 | R22 | 10R 1% | /3V3A – /TCT |
| R36 | R19 | 49R9 1% | /RXP_T – /RCT |
| R37 | R21 | 49R9 1% | /RXN_T – /RCT |
| R38 | R24 | 330R | /LED_LINK_K – /LINKLED |
| R39 | R23 | 330R | /LED_ACT_K – /ACTLED |
| R40 | R11 | 4.7k | +3V3 – /ETH_RST |
| R44 | R14 | 0R | /TXP_CHIP – /TXP_MDI |
| R45 | R13 | 0R | /TXN_CHIP – /TXN_MDI |
| R46 | R16 | 0R | /RXP_T – /RXP_CHIP |
| R47 | R15 | 0R | /RXN_T – /RXN_CHIP |

**C50 to C55 are interchangeable.** All six have the same value, footprint and
nets. The table pairs them in ascending order. Net membership cannot tell them
apart, and it does not need to.

**J2 differs from J1 in one field only.** The block's footprint nickname is
`PlumRFBridge:`, the PoE module's is `PoEEthModule:`. The two footprints are
byte-identical copies (PoE `Layout-Spec.md` §13.6). Pick one nickname before
placement. Another session emptied this project's `fp-lib-table` on
2026-09-24, so the nickname resolves through the global table.

**The designators collide across the two boards.** Block `FB2` is PoE `FB5`,
not PoE `FB2`. Block `U3` is PoE `U4`, and PoE `U3` is the TLV431. Compare by
net, never by designator.

**The VC nets differ in one respect.** On the PoE board they end on FB1 to
FB4. In the block they end on hierarchical labels, and nothing else. §6 takes
them to the breakout row.

## 2. Outline and regions

| Item | X | Y |
|---|---|---|
| Board outline | 114.0 → 156.0 | 50.0 → 105.0 |
| Jack band | 114.0 → 156.0 | 50.0 → 68.0 |
| Line-side strip | 114.0 → 129.5 | 68.0 → 105.0 |
| Ethernet region | 129.5 → 156.0 | 50.0 → 105.0 |
| Breakout row | 119.3 → 154.5 | 102.5 |

### 2.1 Why these edges

| Edge | Value | Reason |
|---|---|---|
| Top | y 50.0 | Unchanged. J2's courtyard reaches 50.04 |
| Right | x 156.0 | Unchanged. `/LINKLED` runs at x 155.2 on B.Cu |
| Left | x 114.0 | `/LED_LINK_K` passes west of SH2 at x 115.4 on B.Cu. 114.0 leaves 1.3 mm |
| Bottom | y 105.0 | Below R40 (y 95.0) only the SPI descent remains. Its F.Cu window ends at y 97.3. §7 explains 105.0 |

The PoE secondary region was x 129.5 → 155.5. The Ethernet parts still fit
inside it. The strip west of x 129.5 exists because J2 overhangs it and the
four line-side nets must cross it.

### 2.2 J2 overhangs the top edge

J2 sits at (125.0, 64.8), rotation 180. Its courtyard ends at y 50.04. Its
`F.Fab` body runs to local y 17.505, which lands at **y 47.30, 2.7 mm past
the edge**. That is the jack nose.

**The footprint's `F.Fab` body also runs 2.75 mm behind the courtyard**, to
local y −3.995, which lands at y 68.80. The courtyard stops at y 66.05. C65
(PoE C32) at (134.0, 67.0) has its courtyard inside x 132.52 → 135.48, and
the fab body ends at x 132.95. If the real body reaches y 68.8, C65 sits under
it. Check the Abracon ARJM11 drawing before release. It is not in
`_resources/Research/`: abracon.com returned an HTML page to every scripted
fetch on 2026-09-24.

## 3. Placement table

PoE board coordinates, read from the `.kicad_pcb` on 2026-09-24. Rotation
follows KiCad.

| Block | PoE | X | Y | Rot |
|---|---|---|---|---|
| R39 | R23 | 138.5 | 53.0 | 0 |
| R38 | R24 | 142.0 | 53.0 | 0 |
| C67 | C39 | 138.0 | 58.5 | 0 |
| J2 | J1 | 125.0 | 64.8 | 180 |
| C65 | C32 | 134.0 | 67.0 | 0 |
| R37 | R21 | 137.5 | 68.0 | 0 |
| C66 | C34 | 141.0 | 68.0 | 0 |
| R34 | R20 | 151.5 | 68.5 | 90 |
| R46 | R16 | 143.75 | 72.0 | 270 |
| R47 | R15 | 145.3 | 72.0 | 270 |
| R45 | R13 | 146.85 | 72.0 | 90 |
| R44 | R14 | 148.4 | 72.0 | 90 |
| R33 | R18 | 151.5 | 72.0 | 90 |
| C63 | C36 | 154.0 | 72.0 | 270 |
| C64 | C31 | 134.0 | 73.5 | 0 |
| C50 | C23 | 131.0 | 76.0 | 180 |
| R36 | R19 | 136.5 | 76.0 | 0 |
| R35 | R22 | 154.0 | 76.0 | 90 |
| C51 | C24 | 131.0 | 78.25 | 180 |
| U3 | U4 | 143.5 | 80.0 | 270 |
| C52 | C26 | 131.0 | 80.5 | 180 |
| FB2 | FB5 | 153.0 | 83.0 | 0 |
| C60 | C37 | 131.5 | 83.5 | 180 |
| C59 | C33 | 131.5 | 85.5 | 180 |
| C57 | C35 | 153.0 | 86.0 | 0 |
| C53 | C27 | 136.2 | 88.0 | 0 |
| C61 | C22 | 139.5 | 88.0 | 180 |
| Y1 | Y1 | 143.5 | 88.0 | 0 |
| C62 | C25 | 147.5 | 88.0 | 0 |
| C58 | C38 | 153.0 | 89.0 | 0 |
| C54 | C28 | 136.2 | 91.0 | 0 |
| C55 | C29 | 140.0 | 91.5 | 0 |
| R31 | R10 | 143.5 | 91.5 | 0 |
| R32 | R12 | 146.9 | 91.5 | 0 |
| C56 | C30 | 152.0 | 92.0 | 0 |
| R30 | R17 | 139.0 | 94.0 | 270 |
| R40 | R11 | 150.0 | 95.0 | 0 |

37 rows. The westmost Ethernet courtyard is C50 to C52 at x 129.52. That is
0.02 mm inside the old secondary edge, and it holds.

**The PoE `Layout-Spec.md` §3 table is stale.** It gives C23, C24 and C26 at
x 135.5, C37 at (135.5, 85.5), C33 at (132.0, 85.5) and C30 at (150.5, 80.0).
The board has them at the positions above. This table is read from the board.

## 4. What comes off the PoE board

Remove every part that is not in §3: the primary set, the bridges T1, U2, C16,
C17, and the PoE output set. On the PoE board three foreign nets have copper
inside the Ethernet region: `/VOUT_RAW` (8 points), `/SEC_A` (12) and
`/SNUB_MID` (2). Delete them with their parts.

Copy the routing of the Ethernet nets unchanged down to y 97.3. It is DRC
clean on the PoE board, and every decision in PoE `Layout-Spec.md` §4 and §12
still holds: the jack fanout, the crystal rebuild, the LED lanes, the SPI via
fanout at y 82.3.

## 5. Widths

| Net | Width | Why |
|---|---|---|
| MDI pairs | 0.20 / 0.20 | `MDI` class |
| `+3V3`, `/3V3A` | 0.3048 | `Power_1` |
| SPI, reset, LEDs | 0.20, 0.15 in the U3 fanout | as on the PoE board, §13.2 there |
| Line-side lanes | 0.20 | §6 |
| `/CGND` | as routed | 0.40 clearance, `Chassis` |

**The MDI pairs are about 84 Ω, not 100 Ω.** 0.20 / 0.20 over In1 at 0.10 mm,
εr 4.5, computes to 84.4 Ω differential (Kirschning–Jansen). 100 Ω needs
about 0.15 / 0.25. The `.kicad_dru` says why it does not matter: 100BASE-TX
has a 100 mm critical length and every run here is under 40 mm. Keep the PoE
geometry.

## 6. The line-side nets

`/POE_VC1P`, `/POE_VC1N`, `/POE_VC2P` and `/POE_VC2N` are **hierarchical
labels** in the block schematic, each on one J2 pin and nothing else. A host
that adds a PoE PD takes them from the block. So they break out.

They carry PSE voltage whenever the cable comes from a PoE switch, whether or
not anything uses them. The `Line_Side` class and the `J2 line side
clearance` rule keep 0.4 mm from everything else.

| Net | Pad | Lane | Via x |
|---|---|---|---|
| `/POE_VC2N` | J2.1 (119.285, 62.26) | F.Cu straight down, x 119.285 | 119.3 |
| `/POE_VC1N` | J2.2 (120.555, 64.80) | F.Cu straight down, jog east at y 100 | 120.9 |
| `/POE_VC2P` | J2.6 (125.635, 64.80) | F.Cu straight down, jog west at y 100 | 125.1 |
| `/POE_VC1P` | J2.7 (126.905, 62.26) | F.Cu down between J2.6 and J2.8, jog west at y 100 | 126.7 |

These are the PoE board's own escapes, continued south. None crosses another
net.

**Two lanes pass between pads, with 0.42 mm each side.** `/POE_VC2N` passes
west of J2.2. `/POE_VC1P` passes between J2.6 and J2.8, the one clear gap the
PoE spec names. The barrel gap is 1.04 mm. A 0.20 mm lane leaves 0.42 mm, and
the rule asks 0.40. **A 0.30 mm lane fails.** So the lanes are 0.20 mm
throughout. 0.20 mm of 35 µm outer copper carries the 350 mA of an 802.3af
pair with a small rise.

**The strip carries no other copper.** No pour on any layer, and a keepout on
In1.Cu and In2.Cu:

| Item | Value |
|---|---|
| Rectangle | 113.0, 49.0 → 129.5, 106.0 |
| Layers | In1.Cu, In2.Cu |
| Forbids | copper pour |
| Allows | tracks, vias |

This is PoE `Layout-Spec.md` §7 cut to this board. It is not required by the
0.4 mm rule. It is there so a host can put a PD beside this block and still
draw the PoE module's 2.5 mm barrier at x 127.0 → 129.5. `/POE_VC1P`'s via at
x 126.7 ends at x 127.0 for that reason.

## 7. The breakout row

Via 0.6 mm pad on 0.3 mm drill. Row at **y = 102.5**, 2.5 mm above the bottom
edge, as on the PoE module. Each signal via carries a 1.0 mm stub on the far
layer, ending at y 103.5.

| x | Offset from GND 131.0 | Net | Direction | Arrives on | Stub |
|---|---|---|---|---|---|
| 119.3 | −11.7 | `/POE_VC2N` | both | F.Cu | B.Cu |
| 120.9 | −10.1 | `/POE_VC1N` | both | F.Cu | B.Cu |
| 125.1 | −5.9 | `/POE_VC2P` | both | F.Cu | B.Cu |
| 126.7 | −4.3 | `/POE_VC1P` | both | F.Cu | B.Cu |
| 131.0 | 0.0 | `GND` | stitch | pour | both |
| 134.0 | 3.0 | `GND` | stitch | pour | both |
| 137.0 | 6.0 | `GND` | stitch | pour | both |
| 140.0 | 9.0 | `GND` | stitch | pour | both |
| 143.3 | 12.3 | **vacant** | — | — | — |
| 144.9 | 13.9 | `/ETH_CS` | in | B.Cu | F.Cu |
| 146.5 | 15.5 | `/ETH_CLK` | in | B.Cu | F.Cu |
| 148.1 | 17.1 | `/ETH_MISO` | out | B.Cu | F.Cu |
| 149.7 | 18.7 | `/ETH_MOSI` | in | B.Cu | F.Cu |
| 151.3 | 20.3 | `/ETH_INT` | out | B.Cu | F.Cu |
| 152.9 | 21.9 | `/ETH_RST` | in | B.Cu | F.Cu |
| 154.5 | 23.5 | `+3V3` | in | B.Cu | F.Cu |

**The offsets from 131.0 onward are PoE `Host-Setup.md` §6, unchanged.** A host
laid out for the PoE block takes this block without a new landing pattern.
The `/POE_5V` slot at 12.3 stays empty, because this block has no 5 V output.

**Why y 102.5 and not 98.** The five SPI lanes leave the F.Cu window at y 97.3
at 1.2 mm pitch, x 142.6 → 147.4. They must reach x 144.9 → 151.3 at 1.6 mm
pitch. The largest shift is 3.9 mm, and a 45° jog needs the same in y.
97.3 + 3.9 = 101.2. The row at 102.5 leaves 1.3 mm of slack. Jog in the PoE
order: `/ETH_INT` first, `/ETH_CS` last.

The VC vias sit at 1.6 mm pitch within each pair. A PSE puts up to 57 V
between the pairs. The VC2P–VC1N gap is 4.2 mm.

`/ETH_RST` keeps its 4.7 k pull-up, R40, inside the block. `/CGND` does not
break out. No MDI pair crosses the block boundary.

## 8. Zones

| Zone | Layer | Net | Rectangle |
|---|---|---|---|
| Top pour | F.Cu | `GND` | 129.5, 50.5 → 155.5, 104.5 |
| Bottom pour | B.Cu | `GND` | 129.5, 50.5 → 155.5, 104.5 |
| Ground plane | In1.Cu | `GND` | 129.5, 50.5 → 155.5, 104.5 |
| Power plane, upper | In2.Cu | `/3V3A` | 136.0, 68.0 → 155.0, 94.0 |
| Power plane, lower | In2.Cu | `GND` | 129.5, 95.0 → 155.5, 104.5 |
| Inner keepout | In1.Cu, In2.Cu | — | 113.0, 49.0 → 129.5, 106.0 |

The PoE board's zones, with the bottom edge moved from y 133.5 to 104.5 and
the primary zones gone. In1 stays whole under the Ethernet region. In2 splits
for U3's six AVDD pins, for the reason in PoE `Layout-Spec.md` §9.

## 9. PCBWay edge rule

**PCBWay needs break-away rails when copper sits within 3.5 mm of an edge**
(`docs/Block-Modules-Handoff.md` §4.5). This board trips it on all four:

| Edge | Nearest copper |
|---|---|
| Top | `/LED_LINK_K` via at (141.175, 51.5), 1.5 mm |
| Right | `/LINKLED` at x 155.2 on B.Cu, 0.8 mm |
| Left | `/LED_LINK_K` at x 115.4 on B.Cu, 1.4 mm |
| Bottom | breakout stubs, 1.5 mm |

**The rails go on the left and right edges.** J2's nose overhangs the top edge
by 2.7 mm, so a top rail collides with the jack. Confirm the rail width and the
V-score copper clearance on the PCBWay quote. The right lane at 0.8 mm is the
one to watch.

## 10. Checks before you believe a number

1. `kicad-cli pcb drc --severity-all --schematic-parity --refill-zones`.
2. Canary: append a 3 mm clearance rule, confirm the count explodes, restore
   and diff.
3. Net class column: every VC net reads `Line_Side`, `/CGND` reads `Chassis`.
   An unbound class makes the 0.4 mm rule pass with zero hits.
4. Net membership: compare `(ref, pin)` sets with the block netlist. 37 parts.
5. Count segments from each of the 15 interface nets to its breakout via.
   DRC hides single-pad nets from `unconnected`, and the four VC nets are
   single-pad nets.
6. Render and look at the line-side strip.

## 11. Closing state, 2026-09-25

| Item | Value |
|---|---|
| Board | 42 x 55 mm, outline 114,50 to 156,105 |
| Copper | 242 segments, 72 vias. 207 segments and 57 vias replayed from the PoE module, then 35 segments and 15 vias for the line-side lanes, the SPI jog and the breakout row |
| Zones | 5, as section 8, less the keepout |
| DRC | 0 errors, 0 unconnected, 0 parity |
| `track_dangling` | 11, the 11 signal stubs, expected |
| Canary | 20 → 543 |

Changes from the draft:

1. **No inner keepout.** Konnect cannot write a rule area, so the In1/In2
   keepout of sections 6 and 8 is not on the board. The strip west of x 129.5
   still carries no pour, because every zone starts at x 129.5. A host that
   needs the 2.5 mm barrier draws the keepout itself. `Host-Setup.md` says so.
2. **`/POE_VC2N` via at x 119.285**, on J2 pin 1's own line, not 119.3.
3. **Rules.** The MDI skew rule is gone: it compared unlike segments across
   series parts and could never pass. The line-side rule stops at J2's
   courtyard, where the carried-over MDI_RDP escape passes pad 7 at 0.26 mm.
   A 0.35 mm hole-to-hole rule covers the SPI fanout under U3.
