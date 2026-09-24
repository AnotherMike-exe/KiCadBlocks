# Block Modules Handoff

For the next session. Build a standalone board for each design block, in a temp
folder, to that block's own spec. Then commit the results as block resources.

Written 2026-09-21.

---

## 1. The plan

1. Make a temp folder. Put the two KiCad projects in it.
2. Make a blank project for one block.
3. Place the block from the Design Blocks panel.
4. Build the board around the block's spec. Outline, stackup, planes, netclasses.
5. Run ERC and DRC. Render and look.
6. Save the layout back into the design block, or keep the board as its own
   module project.

The blocks already exist. Section 4 lists what each one needs.

## 2. Why a standalone board, and not a layout fragment

A design block `.kicad_pcb` holds footprints, tracks, vias, zones, graphics and
groups. It does **not** hold the board outline, the netclasses or the stackup.

The Plum-RFBridge board keeps its hardest geometry in board wide zones:

| Zone | Layers | Extent |
|---|---|---|
| copper pour | F.Cu | 100.5-164.5 x 50.5-144.5 |
| copper pour | B.Cu | 100.5-164.5 x 50.5-144.5 |
| copper pour | In1.Cu | 100.5-164.5 x 50.5-144.5 |
| copper pour | In2.Cu | 100.5-164.5 x 50.5-144.5 |
| second pour | B.Cu | 100.5-130.0 x 50.5-118.0 |
| PoE primary, inner plane void | In1.Cu, In2.Cu | 100.5-133.4 x 50.5-119.5 |

A fragment cannot carry those. A standalone board can, and it also removes the
area conflict described in section 4.1.

## 3. What already exists

| Item | Path |
|---|---|
| Nine schematic blocks | `${PLUM_SOLUTIONS}/Blocks/PlumBlocks.kicad_blocks` |
| Shared symbols | `${PLUM_SOLUTIONS}/Symbols/PlumRFBridge.kicad_sym` |
| Shared footprints | `${PLUM_SOLUTIONS}/Footprints/PlumRFBridge.pretty` |
| Shared 3D models | `${PLUM_SOLUTIONS}/3dshapes/PlumRFBridge.3dshapes` |
| Method and traps | `Design-Blocks-Runbook.md` |
| Durable record | `docs/PCB-Design-Record.md`, section "Design block library" |

All nine blocks passed ERC and a net membership check. 188 nets, all exact.

## 4. Spec requirements for each module

### 4.1 PoE-PD-Si3402-Class1

**The thermal plane is the reason to make this a separate board.**

- The Si3402-B thermal pad connects to VNEG, pin 9, and to a **2 in² heat
  spreader plane**, with at least **nine thermal vias**.
- 2 in² is **1290 mm²**. On the 65 x 95 mm Plum-RFBridge board that is 21% of the
  area, and it must sit on the isolated primary side. A module board removes that
  conflict.
- **The plane must be on an OUTER layer.** AN956 measures 44 °C/W for 2 in² on an
  outer layer, and 54 °C/W for 1 in² on an inner layer. Inner layer copper is not
  a substitute.
- Class 1 budget is 3.84 W. Worst case dissipation is about 0.85 W. Thermal
  shutdown is 160 °C junction.

**Isolation barrier.**

- Five things cross it: `T1`, `U7`, `C89`, `C90` and `J2`.
- The primary domain is **18 nets and 26 components**: U5, C70-C82, C87, C88,
  D30, D31, FB3-FB6, R50, R51, R57, R58.
- Barrier clearance **2.5 mm**. This is practice derived. No vendor document we
  hold gives a PCB spacing figure. Enforce it with a `.kicad_dru` rule.
- Slot width **1.0 mm or more**. PCBWay minimum NPTH slot is 0.8 mm at ±0.2 mm.
- **The slot cannot run all the way across.** It terminates at the `J2` body. See
  section 4.5.
- Keep an inner plane void across In1 and In2 on the primary side.

### 4.2 RF-CC1101-433

- **Do not change C20 and C21.** 12 pF and 15 pF are asymmetric on purpose. TI
  SWRR046 sets them. This project already made that mistake once.
- Every balun and match value comes from SWRR046. The record holds the full
  comparison table.
- Give `J3` a 50 ohm feed and dense ground stitching around it.
- Keep any flyback switching node away from this front end.

### 4.3 Buck-5V-3V3-TPS563208

- The input loop area sets the noise. Put C100 and C101 at the VIN pin.
- Keep the SW_NODE copper small.
- C102 bootstraps the high side gate drive. It connects SW to VBST, nothing else.
- Vout = 0.768 V x (1 + R60/R61) = 0.768 x (1 + 33k/10k) = 3.30 V.

### 4.4 MCU-ESP32S3-MINI

**The PCB antenna needs the board cut away, not a copper keepout.** From the
ESP32-S3 Hardware Design Guidelines, section 1.4.7:

| Rule | Value |
|---|---|
| alongside the meander | 15 mm or more |
| inward from the antenna end edge | 6 mm |
| module edge inside the board outline | 1 mm or less |
| feed side inside the side edge | 2 mm or less |
| shape | a corner notch flush to two outer edges |

Never hollow an island on four sides. Ground copper and dense stitching vias are
required next to the cut-out.

MINI-1-N8 is rated -40 to +85 °C.

### 4.5 Ethernet-W5500-Magjack

- **PCBWay needs break-away rails when edge to copper is under 3.5 mm.** An RJ45
  at the board edge trips this.
- `J2` carries the PoE centre taps. Its line side pins 1, 2, 6, 7 interleave with
  its chip side pins 3, 4, 5, 8, 9, 10 in one pad field. The tightest primary to
  secondary pair is 2 to 3 at **2.84 mm centre to centre, about 1.3 mm copper to
  copper**. Abracon's land pattern fixes this. Layout cannot improve it.
  Abracon's 1500 Vrms construction is the isolation there.
- 49R9 terminations. 25 MHz crystal.

### 4.6 The four small blocks

`PowerMux-TPS2121`, `LDO-RF-3V3-AP2112K`, `USBC-Device-ESD` and `LED-Status-x3`
carry no special layout constraint. Keep the mux input capacitors at their pins.
Keep the LDO output capacitor at its pin.

## 5. Rules that apply to every module board

- **Assign nets to netclasses.** On Plum-RFBridge no net binds to any netclass, so
  the isolation classes bind to nothing. Do not repeat that.
- Vias: 0.3 mm drill, 0.6 mm diameter. `Default`, `Power_1` and `Power_2` all use
  these.
- A `.kicad_dru` condition must not contain a newline. It silently kills every
  rule in the file.
- `kicad-cli pcb drc` grades the saved zone fill unless you pass `--refill-zones`,
  and that flag refills in memory only. It never writes back.
- Refill before you believe a clearance number. One run on Plum-RFBridge showed 61
  errors, and 53 were stale zone fills.
- The FA2924-AL land pattern is 10 SMD pads 2.03 x 1.27 mm, **X = ±8.51 mm**,
  Y = ±5.00, ±2.50, 0. The datasheet's 14.99 mm figure is an inner edge gap, not a
  centre spacing. A third party Olimex footprint uses ±8.008 mm and is wrong.

## 6. Do these two things first

1. **Repoint `PlumRFBridge`** in Preferences, Manage Symbol Libraries and Manage
   Footprint Libraries, to `${PLUM_SOLUTIONS}`. Both still point at
   `/Users/michaelprice/Downloads/Plum-ESPHome-RfBridge/hardware/pcb/libraries/`,
   which does not exist. Konnect cannot do this. Its register tool reports success
   and leaves an existing nickname untouched.
2. **Delete the stray row** `${PLUM_SOLUTIONS}:Blocks` in Manage Design Block
   Libraries. The variable landed inside the path. Keep the `PlumBlocks` row.

Also turn on the IPC API under Preferences, Plugins, and open pcbnew. Konnect
writes to the PCB only through IPC, and the handshake fails while pcbnew is
closed:

```
KiCad IPC error: no handler available for request of type
kiapi.common.commands.GetOpenDocuments (AS_UNHANDLED)
```

## 7. Open question for the next session

"The two PCB projects" is read here as:

| Project | Path |
|---|---|
| Plum-RFBridge | `_resources/Examples/Plum-RFBridge/Plum-RFBridge.kicad_pro` |
| Plum-ESPHome-RFBridge, the earlier prototype | `_resources/Tests/pcb/Plum-ESPHome-RFBridge.kicad_pro` |

Confirm this at the start of the session, or name the second project.
