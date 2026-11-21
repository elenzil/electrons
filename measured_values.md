# LED Soft-Fade Circuit — Measured Values

**Reference date:** November 15, 2026  
**Circuit:** 5 V analog soft-fade circuit with a single IRLZ44N MOSFET, three LED branches, and individual 10 Ω series resistors.

This record consolidates the electrical measurements and calculations discussed on November 19, 2026. Values marked **calculated** or **estimated** were not measured directly in the stated configuration.

## Latest three-LED configuration

| Measurement | Value | Notes |
|---|---:|---|
| USB-C power module output | 4.989 V | Measured |
| Voltage at breadboard LED rails, initially | ~4.6 V | Measured |
| Improved rail voltage | ~4.77–4.78 V | Measured after wiring improvements |
| Voltage across each 10 Ω resistor | ~1.5 V | Measured, approximate |
| Voltage across each LED | ~3.05 V | Measured, approximate |
| MOSFET drain-to-source voltage | 0.007 V | Measured in the fully-on condition |
| Current through each LED branch | ~150 mA | **Calculated** from 1.5 V / 10 Ω |
| **Total current through three LEDs** | **~450 mA** | **Calculated**, 3 × 150 mA; not a direct USB supply current measurement |
| Power dissipated per 10 Ω resistor | ~0.225 W | **Calculated**, (0.15 A)² × 10 Ω |

### Calculations

Per LED branch:

```text
I_LED = V_R / R = 1.5 V / 10 Ω = 0.150 A
```

For three branches:

```text
I_total = 3 × 0.150 A = 0.450 A
```

Per resistor:

```text
P_R = I²R = (0.150 A)² × 10 Ω = 0.225 W
```

The approximately 450 mA figure is inferred from individual resistor drops; it should not be treated as an independently measured total input current. Approximate readings and measurements made at different times may not close perfectly in a voltage or current budget.

## Breadboard voltage losses

| Location | Approximate measured drop |
|---|---:|
| Positive supply wiring | 0.08 V |
| Ground return wiring | 0.14 V |
| **Combined wiring loss** | **0.22 V** |

At 4.989 V module output, subtracting 0.22 V predicts approximately **4.77 V** at the LED rails, consistent with the improved rail reading. The MOSFET's ~0.007 V fully-on drop was small by comparison.

## Earlier resistor comparisons

These are included only as comparison measurements, not as alternative circuit designs to be used going forward.

| Three-LED configuration | Approximate total current | Basis |
|---|---:|---|
| Individual 20 Ω resistors | ~300 mA | Reported measured current |
| One shared 5.5 Ω resistor | ~260 mA | Reported measured current |
| Individual 10 Ω resistors | ~420–450 mA | Approximate/calculated from observations; **450 mA** from 1.5 V per 10 Ω branch |

The current reference circuit uses **a separate 10 Ω resistor for every LED**.

## Eight-output PCB: estimated currents

The latest PCB provides up to eight independent LED branches. Unconnected outputs draw no LED-branch current. Assuming each connected branch behaves like the measured three-LED test (~150 mA per branch):

| Connected LEDs | Estimated total LED current |
|---|---:|
| 1 | 0.15 A |
| 2 | 0.30 A |
| 3 | 0.45 A |
| 4 | 0.60 A |
| 5 | 0.75 A |
| 6 | 0.90 A |
| 7 | 1.05 A |
| 8 | 1.20 A |

**These are extrapolations, not measurements on the eight-output PCB.** Actual values depend on the supply, LED forward voltages, circuit wiring, temperature, and simultaneous load. Total supply current also includes any control-circuit current.

## Practical implications

- Each 10 Ω resistor dissipated approximately **0.225 W**, calculated from the resistor-voltage readings. A nominal ¼ W resistor would have little power margin; a higher-rated resistor is preferable, especially in an enclosed lamp.
- The supply and wiring should be evaluated for the maximum intended number of connected LEDs, not just the initial three-LED test.
- Verify the actual resistor voltage drops, total input current, and temperatures on the assembled eight-output PCB before treating the extrapolated numbers as operating specifications.
- The fade controller remains the **single IRLZ44N MOSFET**, **SPDT ON–ON switch**, **300 kΩ fade resistance**, and **10 µF gate capacitor** configuration.
