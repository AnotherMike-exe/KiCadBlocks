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
