# 3C_VOF_70k: Experiment-03(c) Three-Phase VOF Simulation Case

## Status & Performance Summary
* **Status**: **STABLE & VALIDATED** (All global acceptance gates passed)
* **Sustained Throughput**: **63.2 sim-s per wall-clock hour** (Measured over 300+ s window on 8 parallel cores)
* **Mesh Resolution**: **51,550 cells** (Exact 5-layer 25-block geometry matching 2-phase twin `3C` spatial resolution)
* **Solver**: Isolated `sedInterFoam` (v2412, loading `$HOME/OpenFOAM/sedInterFoam-2412/lib/libtwoPhaseModelInter.so`)

---

## Case Overview
* **Target Experiment**: Experiment-03(c) ($H_b/Y = 0.70$)
* **Opening Ratio ($H_b/Y$)**: **0.70** (Milder vertical contraction; max scour occurs downstream of deck)
* **Bed Thickness**: $0.120\text{ m}$ ($y \in [-0.12, 0.0]\text{ m}$)
* **Water Depth**: $Y = 0.1107\text{ m}$ ($y \in [0.0, 0.1107]\text{ m}$)
* **Bridge Deck Soffit ($H_b$)**: $0.0770\text{ m}$ ($y \in [0.0, 0.0770]\text{ m}$)
* **Bridge Deck Top Level**: $0.2000\text{ m}$ ($y \in [0.0770, 0.2000]\text{ m}$)
* **Air Region Above Deck**: $y \in [0.2000, 0.3107]\text{ m}$ (Includes continuous air mesh block above deck)
* **Bridge Deck Dimensions**: Length $L = 0.153\text{ m}$ ($x \in [0.0, 0.153]\text{ m}$)

---

## Computational Domain & Layer Schematic

```text
========================================================================================================================
                                     3C_VOF DOMAIN & LAYER SCHEMATIC LAYOUT
========================================================================================================================

   y (m)
  0.3107 +----------------------+----------------------+----------------------+----------------------+----------------------+  <-- Top Atmosphere
         |      BLOCK 20        |      BLOCK 21        |      BLOCK 22        |      BLOCK 23        |      BLOCK 24        |      (Patch)
         |     AIR REGION       |     AIR REGION       |  AIR MESH ABOVE DECK |     AIR REGION       |     AIR REGION       |
         |   (gamma = 0.0)      |   (gamma = 0.0)      |   (gamma = 0.0)      |   (gamma = 0.0)      |   (gamma = 0.0)      |
  0.2000 +----------------------+----------------------+----------------------+----------------------+----------------------+  <-- Deck Top Level
         |      BLOCK 16        |      BLOCK 17        |  SOLID BRIDGE DECK   |      BLOCK 18        |      BLOCK 19        |
         |     AIR REGION       |     AIR REGION       |   (OMITTED BLOCK)    |     AIR REGION       |     AIR REGION       |
         |   (gamma = 0.0)      |   (gamma = 0.0)      |                      |   (gamma = 0.0)      |   (gamma = 0.0)      |
 0.07700 +----------------------+----------------------+----------------------+----------------------+----------------------+  <-- Deck Soffit (Hb)
         |      BLOCK 11        |      BLOCK 12        |      BLOCK 13        |      BLOCK 14        |      BLOCK 15        |
         |    WATER COLUMN      |    WATER COLUMN      |  PRESSURE FLOW ZONE  |    WATER COLUMN      |    WATER COLUMN      |
         |   (gamma = 1.0)      |   (gamma = 1.0)      |   (gamma = 1.0)      |   (gamma = 1.0)      |   (gamma = 1.0)      |
  0.0000 +~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~+~~~~~~~~~~~~~~~~~~~~~~+  <-- Initial Bed Level
         |      BLOCK 6         |      BLOCK 7         |      BLOCK 8         |      BLOCK 9         |      BLOCK 10        |
         |  UPPER SAND BED      |  UPPER SAND BED      |  UPPER SAND BED      |  UPPER SAND BED      |  UPPER SAND BED      |
 -0.0400 + - - - - - - - - - - -+- - - - - - - - - - - +- - - - - - - - - - - +- - - - - - - - - - - +- - - - - - - - - - - +  <-- Mid Bed Level
         |      BLOCK 1         |      BLOCK 2         |      BLOCK 3         |      BLOCK 4         |      BLOCK 5         |
         |  DEEP SAND BED       |  DEEP SAND BED       |  DEEP SAND BED       |  DEEP SAND BED       |  DEEP SAND BED       |
 -0.1200 +----------------------+----------------------+----------------------+----------------------+----------------------+  <-- Bottom Rigid Wall
       x:     -1.5 m                 -0.5 m                  0.0 m      0.153 m                 0.8 m                  2.0 m
           (Inlet Patch)          (Approach)             (Deck LE)   (Deck TE)                (Wake)             (Outlet Patch)
========================================================================================================================
```

---

## Validation Artifacts
- Full quantitative report: [VALIDATION_REPORT.md](validation/VALIDATION_REPORT.md)
- Velocity Profile Comparison vs 2-phase twin: [ux_profiles.png](validation/ux_profiles.png)
- Phase Fraction Profiles ($\alpha_s$, $\gamma$, $1-\gamma$): [phase_profiles.png](validation/phase_profiles.png)

---

## Workflow Commands
```bash
# 1. Source environment
source /usr/lib/openfoam/openfoam2412/etc/bashrc
source ./env_isolated.sh

# 2. Clean and run simulation (8 cores)
./Allclean
./Allrun

# 3. Monitor health metrics
./tools/watch_run.sh log.sedInterFoam
```
