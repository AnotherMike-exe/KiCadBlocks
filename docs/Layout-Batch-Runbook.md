# Layout Batch Runbook

The GUI jobs for the eight new module boards, in batches. Konnect and
`kicad-cli` do everything else. Each batch ends with a script that must pass.

Written 2026-09-24.

| Module | Symbols |
|---|---|
| `Ethernet-W5500-Magjack` | 37 |
| `RF-CC1101-433` | 25 |
| `MCU-ESP32S3-MINI` | 11 |
| `PowerMux-TPS2121` | 14 |
| `Buck-5V-3V3-TPS563208` | 13 |
| `LDO-RF-3V3-AP2112K` | 3 |
| `USBC-Device-ESD` | 4 |
| `LED-Status-x3` | 6 |

Before you start:

1. Mount the Plum volume.
2. Close every KiCad window except the project manager.

---

## Batch 1 — import the footprints. About 45 minutes.

Do these steps for each module in the table.

1. In the project manager, open `Modules/<Block>/<Block>.kicad_pro`.
2. Open the schematic editor.
3. Open **File → Page Settings**. Set these values:
   - Title: `<Block>`
   - Date: `2026-09-24`
   - Revision: `A`
   - Company: `Plum Solutions`
4. Save the schematic. The save also writes this project's instance paths.
5. Close the schematic editor.
6. Open the PCB editor.
7. Select **Tools → Update PCB from Schematic**.
8. Do not tick "Re-link footprints".
9. Click **Update PCB**. Read the report. Every footprint must load. A
   "footprint not found" line stops the batch. Record it.
10. Click **Close**. Save the board.
11. Open **File → Board Setup → Custom Rules**. Make sure that the editor
    shows no error. Close the dialog.
12. Close the PCB editor.

### Acceptance test

```
cd Modules
/opt/homebrew/bin/python3 analysis/check_import.py \
    Ethernet-W5500-Magjack RF-CC1101-433 MCU-ESP32S3-MINI PowerMux-TPS2121 \
    Buck-5V-3V3-TPS563208 LDO-RF-3V3-AP2112K USBC-Device-ESD LED-Status-x3
```

It must print `PASS` for each module. It checks three things:

1. The board references are the same set as the schematic references.
2. Each net class pattern binds to one or more board nets.
3. The canary: a 3 mm clearance rule appended to a copy of the `.kicad_dru`
   makes the DRC count rise. If the count does not rise, the rules file did not
   load.

### IPC check, one time

Do this after the last module.

1. Quit KiCad.
2. Run `open -a /Applications/KiCad/KiCad.app/Contents/Applications/pcbnew.app Modules/LED-Status-x3/LED-Status-x3.kicad_pcb`.
3. Tell the session. It calls Konnect `get_board_info` on that board.

If the call works, the session can change boards and reload after a zone write
without the GUI.

---

## Batch 2 — silkscreen, footprints, fragments. About 90 minutes.

### 2a. Silkscreen and footprint repair, each module board

1. Open the module board in the PCB editor.
2. If the board is in the table below, select each listed footprint.
   Right-click it and choose **Update Footprint…**. Keep "Update text"
   unticked. Click **Update**.

   | Board | Footprints | Why |
   |---|---|---|
   | PowerMux-TPS2121 | U10 | Konnect dropped the `(units)` block |
   | MCU-ESP32S3-MINI | U1, SW1, SW2 | Konnect dropped the `(units)` block |
   | RF-CC1101-433 | as the RF report lists | same |

3. Open **Edit → Edit Text & Graphic Properties**.
4. Set the scope to **Reference designators** only.
5. Set the filter to the passive and discrete references: `C*`, `R*`, `L*`,
   `FB*`, `D*`, `Y*`, `TP*`. Run the dialog once for each pattern.
6. Set **Layer** to `F.Fab`. Leave size and thickness alone. Click **OK**.
7. Keep the ICs, connectors and switches on the silkscreen. A rework
   engineer needs U, J and SW references.
8. Save.

Acceptance test:
```
cd Modules && /opt/homebrew/bin/python3 analysis/check_import.py <Block>
```
It must print PASS. DRC must show 0 errors, 0 unconnected, 0 parity and 0
`lib_footprint_mismatch`. `silk_over_copper` must fall. A fall to 0 in every
silk count is a suspect event: check that the silk layers are still checked.

### 2b. Fragments, each module board

The session does the file work. The GUI does the outline move.

1. The session copies `Modules/<Block>/<Block>.kicad_pcb` and
   `<Block>.kicad_sch` into
   `${PLUM_SOLUTIONS}/Blocks/PlumBlocks.kicad_blocks/<Block>.kicad_block/`
   with `cp -X`, and checks `grep -c '(group '` is 0.
2. Open **the fragment copy**, not the module. Check the path in the title
   bar. The two files have the same name.
3. Open **Edit → Edit Text & Graphic Properties**. Filter the layer to
   `Edge.Cuts`. Set **Layer** to `Dwgs.User`. Click **OK**. Save.
4. Acceptance: the fragment holds 0 `Edge.Cuts` lines and 4 `Dwgs.User`
   lines. The module still holds 4 `Edge.Cuts` lines.

### 2c. BlockBuilder placement test, each fragment

1. Open `BlockBuilder`. Delete everything on the board and in the schematic.
2. Place the design block from the Design Blocks panel.
3. Run **Update PCB from Schematic** with "Apply design block layouts" ticked.
4. Save. The session counts footprints, segments, vias, zones and F.Fab
   labels against the module board, by net name, never by designator.
