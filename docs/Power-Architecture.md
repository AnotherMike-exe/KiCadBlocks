# Power Architecture Across the Blocks

How the two reference projects feed a PoE board, and what that means for every
block. Written 2026-09-22.

Sources: `Plum-RFBridge/_exports/Plum-RFBridge.net`, netlist of 2026-09-01, and
`Izunia_hub_v0.1-RC1/HW/Schematic Prints.PDF`, sheets 3 and 4.

---

## 1. The two reference chains

### Plum RF Bridge

```
RJ45 -> Si3402-B -> VOUT_RAW -> L31 -> POE_5V --+
                                                +-- TPS2121 -> V5_SYS --+
USB-C J1 -------------------------- VBUS -------+                       |
                                                                        |
                          +3V3 <- TPS563208 (U8) <------------------ ---+
                       +3V3_RF <- AP2112K  (U9) <------------------ ----+
```

`+3V3` feeds the W5500 pin 28, the ESP32-S3 pin 3, and FB2 into the W5500
analog rail. `+3V3_RF` feeds FB1 into the CC1101 alone.

### Izunia hub

```
RJ45 -> TPS23753A -> flyback -> +5V25_POE --+
                                            +-- DMP3099L PMOS -> VSYS
USB-C -> STUSB4500L -------- +5V_USB -------+                     |
                                                                  |
                                       +3V3 <- TLV62568A <--------+
```

### What they agree on

| Point | Both projects |
|---|---|
| The PoE stage outputs 5 V, nothing else | Yes |
| The Ethernet PHY takes 3.3 V from the SYSTEM rail | Yes |
| The 3.3 V rail sits downstream of the source selector | Yes |
| The PoE stage contains no 3.3 V regulator | Yes |

### What they disagree on

| Point | Plum RF Bridge | Izunia hub |
|---|---|---|
| USB-C | plain 5 V sink, 5.1 k CC pull-downs | STUSB4500L, full PD sink |
| Source selection | TPS2121 priority mux | DMP3099L PMOS ORing |
| PoE controller | Si3402-B, integrated bridge and switch | TPS23753A plus discrete flyback |
| 3.3 V | TPS563208 | TLV62568A |

`_resources/Examples/Izunia_hub_v0.1-RC1/INDEX.md` section 3 already names sheet 4 as "the upgrade
path" for our USB-C stage.

## 2. Neither reference shares power

The word "share" does not describe either design. Both **select one source**.

- The TPS2121 is a priority multiplexer. One input drives the output. The other
  is off.
- A PMOS ORing pair behaves like an ideal diode OR. The higher input wins and
  the lower one stops conducting.

If a board must draw from PoE and USB at the same time, neither reference
covers it, and neither block does.

## 3. The TPS2121 configuration on Plum RF Bridge

Read from the netlist. The resistor ratios are measured. The trip points are
derived, and they depend on the comparator reference.

| Pin | Divider | Ratio | From |
|---|---|---|---|
| PR1 | R70 118 k / R71 51.1 k | 0.3022 | POE_5V |
| OV1 | R75 46.4 k / R76 10 k | 0.1773 | POE_5V |
| OV2 | R72 46.4 k / R73 10 k | 0.1773 | VBUS |
| ILIM | R74 80.6 k | — | to GND |
| SS | C107 | — | soft start |
| ST | pin 9 | — | not connected |

PoE reaches IN1 and USB reaches IN2. PR1 is driven from IN1, so **PoE has
priority and USB-C is the fallback**.

At a 1.19 V comparator reference the OV inputs trip at 6.71 V and the priority
handover happens at 3.94 V on IN1.

**Check the 1.19 V figure against the TPS2121 datasheet before you rely on it.**
We do not hold that document. The ratios above are certain. The volts are not.

## 4. The decisions, taken 2026-09-22

| Question | Answer |
|---|---|
| Source selector | Keep the TPS2121. `PowerMux-TPS2121` stays the one selector block. |
| USB-C front end | Add `USBC-PD-Sink-STUSB4500L`, redrawn from Izunia sheet 4. |
| PMOS ORing | Does **not** come across. Izunia pairs it with the STUSB4500L, and we do not. |
| Negotiated profile | 5 V. |

The TPS2121 keeps current limit, soft start, overvoltage and priority in one
part. A PMOS ORing pair gives none of those and adds discrete parts to verify.

**The profile is a setting, not a structure.** The STUSB4500L holds its PDO
table in NVM and takes a new one over I2C. So the block brings SDA, SCL, ALERT
and ATTACH out, and a future project changes the profile without a redraw.

**A future project may request more than 5 V, and the subsystem rail stays at
5 V.** That is a second regulation stage, from the negotiated voltage down to
5 V, feeding the mux. It is a new block and it does not exist yet. Do not solve
it inside the PD sink block. Section 5 below still holds: the mux output is
V5_SYS at 5 V, and the buck below it makes 3.3 V.

## 5. The constraint a PD sink puts on the mux

This is the one cross-block trap in the chain.

A USB PD sink negotiates a voltage. The profiles are 5, 9, 12, 15 and 20 V. The
OV2 divider above trips at about 6.7 V. **So a PD sink that requests 9 V or more
shuts the mux input off.**

**We take the first option. The sink requests 5 V, and the OV2 divider does not
move.** That is not a wasted PD controller: a 5 V PD contract carries 3 A, which
is 15 W. The plain 5.1 k sink on Plum RF Bridge gets 500 mA. The Si3402-B Class
1 budget is 3.84 W, so USB gives about four times the PoE budget.

If a later project raises the profile, two things change together. Re-set the
OV2 divider for the new voltage, and confirm the buck input range covers it.
The TPS563208 takes 4.5 V to 17 V, so 9 V and 12 V are inside its range. The
Si3402-B output stays at 5 V, so OV1 never moves. OV1 and OV2 are the same
value today only because both sources are 5 V.

## 6. What this means for each block

**The PoE stage never makes 3.3 V.** Both references agree, and the reason is
not style. A second 3.3 V regulator inside the Ethernet module would give the
board two 3.3 V rails, because the MCU needs one anyway. Two rails cost parts,
sequencing and a ground return question, and they buy nothing.

So `PoE-Ethernet-Si3402-W5500` takes `+3V3` as an **input** and gives `POE_5V`
as an **output**.

| Block | Gives | Takes | Change needed |
|---|---|---|---|
| `PoE-Ethernet-Si3402-W5500` | POE_5V, SPI | +3V3 | none |
| `Ethernet-W5500-Magjack` | SPI | +3V3 | none |
| `USBC-Device-ESD` | VBUS at 5 V | — | none |
| `USBC-PD-Sink-STUSB4500L` | VBUS at a negotiated voltage | — | **new block** |
| `PowerMux-TPS2121` | V5_SYS | POE_5V, VBUS | OV2 divider, see section 4 |
| `Buck-5V-3V3-TPS563208` | +3V3 | V5_SYS | none |
| `LDO-RF-3V3-AP2112K` | +3V3_RF | V5_SYS | none |

## 7. The new block

`USBC-PD-Sink-STUSB4500L` does not exist yet, and it cannot be extracted.
`_resources/Examples/Izunia_hub_v0.1-RC1/INDEX.md` states the reason: the package holds no
`.SchDoc`, so KiCad imports nothing. The block comes from a redraw against
`DOC/STUSB4500L/stusb4500l.pdf` and Izunia sheet 4.

Parts on that sheet: STUSB4500LQTR, a USB4105 connector, DMP3099L PMOS,
ESDA25L, USBLC6, 5.1 k CC resistors, and the ADDR0, ADDR1, ALERT, ATTACH,
VBUS_EN_SNK and VBUS_VS_DISCH support network.

Izunia pairs the STUSB4500L with PMOS ORing. We keep the TPS2121, so **the
DMP3099L and its gate network do not come across**. Decided 2026-09-22.

The block must bring out SDA, SCL, ALERT and ATTACH. The PDO table lives in
NVM, and those four pins are how a project changes it later.
