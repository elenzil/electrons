# Analog LED Soft-Fade Lamp — Discussion Summary

**Discussion dates:** November 15–19, 2026  
**Project:** 5 V USB-C-powered porcelain lamp, analog soft-on/soft-off LED control  
**Current reference:** User-edited KiCad design with **eight optional LED outputs** (`lamp01_100`)

## 1. Goal and decisions

Build a compact, reliable LED circuit for a porcelain lamp that fades smoothly on and off, without PWM, a microcontroller, or an LED-driver IC. The user prefers through-hole components and external wiring to the LEDs, USB-C power module, and panel-mounted switch.

The working electrical topology is a **single IRLZ44N N-channel MOSFET** controlled by an **SPDT ON–ON toggle** and a simple RC network. The design began with three tested LED branches, was expanded in a generated KiCad draft to seven outputs, and was subsequently redesigned by the user to provide **eight outputs**. **Not all eight outputs need to be connected or used**; an unused LED branch can remain open.

Earlier, different MOSFET/switch arrangements were investigated, but the user explicitly chose to set those aside. This document describes the final single-MOSFET approach rather than the superseded experiments.

## 2. Working circuit topology

| Part or connection | Working reference configuration |
|---|---|
| Power | Nominal 5 V DC supplied by an external Adafruit HUSB238 USB-C PD breakout |
| Switching transistor | One IRLZ44N logic-level N-channel MOSFET, low-side switch |
| Control switch | External, three-terminal SPDT ON–ON toggle |
| Timing resistor | 300 kΩ between switch common and MOSFET gate |
| Timing capacitor | 10 µF from gate to ground; positive lead at gate, negative at ground |
| LED branches | Each LED has its **own** 10 Ω series resistor |
| Outputs in current KiCad design | Eight independently resistor-limited LED connection pairs |
| Control method | Analog gate charge/discharge; no PWM |

**Functional wiring:**

- One SPDT throw connects to **+5 V** (fade on); the other connects to **GND** (fade off). The switch common goes through the **300 kΩ** resistor to the MOSFET gate.
- The **10 µF** capacitor is wired between the MOSFET **gate** and **ground**.
- Each populated LED branch follows **+5 V → its own 10 Ω resistor → LED anode → LED cathode → common MOSFET drain**.
- The MOSFET **source** connects to ground. The MOSFET switches the shared LED return.
- In the intended TO-220 package, viewing the marked front with leads downward, the IRLZ44N pins are **Gate–Drain–Source** from left to right. The metal tab is connected to **Drain**, **not ground**. Verify the actual device and footprint before assembly.

The nominal gate RC time constant is **300 kΩ × 10 µF = 3 seconds**. Visible fades need not last exactly three seconds because LED light output and MOSFET conduction are nonlinear functions of gate voltage. The single-resistor arrangement provides charging and discharging through the same nominal 300 kΩ resistance.

## 3. Breadboard behavior and measurements

The **three-LED** version was tested and reported to produce satisfactory, smooth fading. The measurements below came from different tests and should **not** be treated as one simultaneous, internally balanced set of voltage readings.

| Measurement | Reported approximate result |
|---|---|
| Three-LED total current | About **0.42–0.45 A** in representative tests |
| Per-LED branch current | About **0.14–0.15 A** |
| Voltage across each 10 Ω resistor | About **1.4–1.5 V** |
| LED forward voltage | Approximately **2.7–3.05 V**, depending on test |
| USB meter voltage | Around **4.89 V** in one test |
| Breadboard rails | Around **4.6–4.8 V**, depending on wiring/test |
| MOSFET drain–source drop when fully on | Approximately **0.007 V** at roughly 0.42 A |

Breadboard and lead resistance caused measurable supply losses. Adding another jumper improved one rail by roughly **0.05 V**; other checks found losses of approximately **0.08 V** in the positive path and **0.14 V** in the ground path. These observations prompted attention to wiring resistance and power distribution in the PCB.

With **0.15 A** flowing through a **10 Ω** resistor, dissipation is **I²R = 0.225 W** per resistor. This is uncomfortably close to a typical 0.25 W component's nominal rating, particularly inside a lamp. At the same per-branch current, **eight active LEDs would draw approximately 1.2 A** in total; that is a **projection, not a tested eight-LED measurement**. Power-supply capacity, voltage drop, resistor ratings, LED heat, and MOSFET thermal performance still require full-load verification.

## 4. KiCad development and revisions

### Three-output draft (November 15)

An editable, through-hole KiCad project was generated for the working three-LED circuit. It had an approximately **60 × 42 mm** two-layer board, an external USB-C breakout and SPDT switch, individually resistor-limited off-board LEDs, and the same MOSFET/RC topology. Native KiCad ERC and DRC had **not** been run in the generation environment.

### Seven-output generated revision (November 15)

At the user's request, the design was expanded to seven LED branches, retaining a separate resistor for each. The requested mechanical and routing requirements were:

- **Four 2.5 mm non-plated mounting holes**.
- **1.5 mm copper traces on all electrical paths**, including the gate circuit.
- Through-hole parts, with LED assemblies, USB-C breakout, and switch off-board.

The generated revision used an approximately **84 × 98 mm**, two-layer PCB and a **74 × 88 mm mounting-hole center pattern**. It specified 10 Ω, **2 W** LED resistors with 18 mm lead spacing. Internal script-based topology, track-width, and clearance checks were reported as passing; **native KiCad ERC/DRC and physical fit verification remained outstanding**. The size was potentially too large for the lamp.

### User-edited eight-output design reviewed November 18–19

The user subsequently presented a more compact KiCad design, identified as **`lamp01_100`**. The user confirmed that the move to **eight** LED outputs was deliberate, and that some could remain unused. The review described:

| Property | User's compact design |
|---|---|
| LED branches | **8**: D10–D17, R10–R17, J10–J17 |
| Resistor arrangement | A separate 10 Ω resistor for each branch |
| MOSFET and fade control | Single IRLZ44N with the existing analog RC approach |
| Board dimensions | Approximately **51.5 × 39 mm** |
| Routing | **Single copper layer**, with **1.0 mm traces** |
| Mounting | Four **3.2 mm** mounting holes |
| Wire-connection drill size | Approximately **0.7 mm** |
| LED-resistor footprint | Small vertical **DIN0207**, nominally 0.25 W |

The assistant's geometric/connectivity inspection **reported all existing routed pads connected**, no apparent cross-net copper shorts, and approximately **0.4 mm** minimum clearance in that check. This was **not** a native KiCad DRC pass or a fabrication sign-off.

The smaller layout was viewed favorably, but it differs from the **earlier requested** 1.5 mm traces and 2.5 mm mounting holes. Whether those original physical specifications still apply is an open design decision; the eight-LED count itself is **not** a problem.

## 5. Issues and changes discussed for the compact PCB

1. **LED resistor power and footprints — highest concern.** The current vertical DIN0207 footprints typically correspond to ~0.25 W resistors, while one 10 Ω resistor may dissipate about 0.225 W at the measured operating current. The discussion recommended moving to **at least 1 W-rated resistors** and footprint sizes appropriate to the actual parts. Verify resistor body dimensions, orientation, spacing, and cooling.
2. **Wire terminal drill diameter.** Approximately **0.7 mm** holes may be difficult for the intended **22 AWG silicone wire**. Suggested target: roughly **1.0–1.2 mm** drill holes, with suitably larger pads and space for soldering and strain relief. Confirm final wire preparation and copper-pad geometry.
3. **Original trace-width target.** Current traces are **1.0 mm**, rather than the requested **1.5 mm**. Decide whether to restore the original rule and reroute as necessary; evaluate board-size consequences.
4. **Original mounting-hole target.** Current holes are **3.2 mm**, rather than **2.5 mm**. Confirm intended fasteners, physical edge clearance, and whether 3.2 mm is now preferred.
5. **Power and heat at higher load.** Progressively test more populated branches, supply voltage at load, wire and board temperature, LED thermal mounting, resistor temperatures, and total current. The eight-output board does **not** require eight LEDs to be installed.
6. **Fabrication verification.** Run **KiCad ERC and DRC**, verify schematic-to-PCB consistency, confirm MOSFET pinout and footprints, inspect silk and edge/drill clearances, and review Gerbers and drill files before ordering.

## 6. KiCad editor guidance covered in this discussion

- **Crossing schematic wires:** Wires can cross without electrical connection if no junction dot is present. Ending one wire on another can intentionally create a junction; verify the dot and net connectivity.
- **Wire hop-overs:** The discussion identified this as a **KiCad 10** feature and gave **File → Schematic Setup → General → Formatting → Hop-over size**, selecting a visible size instead of `None`.
- **Editing custom symbols:** Open **Tools → Symbol Editor** from the Schematic Editor, choose the symbol from its custom library, make changes, and save the library. Then use **Tools → Update Symbols from Library** in the schematic to bring existing placed instances up to date.
- **Footprints are separate:** Use the PCB **Footprint Editor** to edit physical footprints; modifying a schematic symbol does not automatically alter a footprint.

## 7. Current state and next actions

**Current intent:** Keep the **single-MOSFET, SPDT ON–ON, 300 kΩ/10 µF** analog fade circuit. Continue with the user's compact **eight-output** KiCad design; populate or connect only the LED branches needed for the porcelain lamp.

**Established:** The three-LED breadboard version worked satisfactorily, and preliminary custom geometric checks of the uploaded compact PCB did not reveal obvious short circuits or disconnected routed pads.

**Not established:** Operation, thermal performance, or current at eight LEDs; exact physical suitability of the new resistor and wire footprints; native KiCad ERC/DRC cleanliness; or PCB fabrication readiness.

**Recommended immediate sequence:** Replace/verify resistor footprints and ratings; review wire terminal drills; decide whether the initial trace/mounting-hole dimensions still apply; run native KiCad schematic and board checks; inspect fabrication outputs; and bench-test incrementally from one LED upward.

## 8. To-do (as of November 19, 2026)

**Now**
- [ ] LED resistors: move to ≥1 W parts with matching footprints (each 10 Ω currently dissipates ~0.225 W).
- [ ] Wire pads J10–J17 (and probably J1): enlarge the 0.7 mm drills to ~1.0–1.2 mm for 22 AWG silicone wire.
- [ ] Re-breadboard and bench-test incrementally, from one LED upward (current, voltage at load, temperatures).
- [ ] Choose and source LEDs.

- [ ] Route the new USB-C jack J18 (GCT USB4085-GF-A, left edge) and its CC pull-downs R2/R3 (5.1 kΩ); tidy placement and silkscreen. Board widened 10 mm to the left; H1/H4 moved with the edge; board minimum clearance lowered to 0.15 mm for the jack's pins.

**Later**
- [ ] Review Gerbers and drill files before ordering.
- [x] Mouser check (Nov 19, via Mouser Search API). PR01 1 W, ±5 %, ~$0.17 each at qty 10, all in stock except as noted:
  - 10 Ω `PR01000101009JR500` (594-5073NW10R00J): **out of stock**, 20k due Nov 23. In-stock equivalent: `PR01000101009JA500` (594-PR01000101009JA5, ammo pack, same part).
  - 12 Ω `PR01000101209JR500` (594-5073NW12R00J) · 13 Ω `PR01000101309JR500` (594-5073NW13R00J) · 15 Ω `PR01000101509JR500` (594-5073NW15R00J) · 20 Ω `PR01000102009JR500` (594-5073NW20R00J)
  - 5.1 Ω `PR01000105108JR500` is available but would overload a 1 W part with these LEDs; don't use it.
  - Slim (0207) 1 W resistors: only Vishay PR01 found. 1 % version in stock only for 10 Ω (`PR01000101009FR500`, $0.31 at qty 10).
  - Through-hole, power-only USB-C jacks (in stock): GCT `USB4750-GF-C` (vertical, IP67, $1.61; GCT's spec title says through-hole), Kycon `KUSBV67X-TH-CS-6-BTR` (vertical, IP67, O-ring), TE `2495157-1` (6P waterproof "DIP", orientation unverified). No surface-mount parts. Needs 5.1 kΩ from each CC pin to GND.

**Done**
- [x] Traces are 1.5 mm (verified in `lamp01_100.kicad_pcb`).
- [x] Mounting holes: keep 3.2 mm (M3).
- [x] KiCad ERC, DRC and schematic parity: 0 violations (KiCad 10 `kicad-cli`, November 19).
- [x] Gitignore KiCad backup and unsaved-export files.

---

*This is a discussion and design-decision summary, not a substitute for a checked schematic, electrical testing, or a fabrication review. It intentionally excludes packaged project files, board images, and other artifacts.*
