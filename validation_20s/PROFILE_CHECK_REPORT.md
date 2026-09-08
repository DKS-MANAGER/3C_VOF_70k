# Profile Check & High-Accuracy Validation Report (t = 30 s)

## 1. Executive Summary & Verdict
A high-accuracy 30-second validation simulation was executed for `3C_VOF_70k` on 8 parallel cores using OpenFOAM v2412 following the inlet mass boundary condition repair.

### **FINAL VERDICT: PROCEED TO 1800 s PRODUCTION RUN**
- **Status**: **PASSED (ALL 14 ACCEPTANCE CRITERIA MET)**
- **Simulation Time Reached**: 30.0 seconds cleanly without FPE, crashes, or artificial velocity jet anomalies
- **High Accuracy Execution**: 2nd-order TVD convection (`Gauss limitedLinear 1`), MULES sub-cycling (`nAlphaSubCycles 2`), PISO `nCorrectors 3`

---

## 2. Acceptance Criteria Pass/Fail Results Table

| ID | Parameter / Category | Target Criterion | Measured Result | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **S1** | Sand: Packed Bed Concentration | 0.55 <= alpha_solid <= 0.64 in bed, global <= 0.64 | Bed range: [0.6015, 0.6395], Min: 0.000000 | **PASS** |
| **S2** | Sand: Upstream Bed Level Stability | Bed top y = 0.000 +- 0.010 m at x = -0.5 m | Measured bed top y = -0.0081 m | **PASS** |
| **S3** | Sand: Suspended Load & Air Contamination | alpha_solid < 1e-3 above y=0.01m, < 1e-6 in air | Max water susp: 4.67e-26, Max air: 6.39e-128 | **PASS** |
| **S4** | Sand: Sediment Phase Velocity Us | |Us| < 0.05 m/s inside packed bed (y < -0.02m) | Max packed bed |Us| = 0.00000 m/s | **PASS** |
| **W1** | Water: VOF Boundedness | -1e-6 <= gamma <= 1 + 1e-6 globally | Global gamma range: [0.0000000, 1.0000000] | **PASS** |
| **W2** | Water: Phase Separation | gamma >= 0.99 in water column, <= 0.05 in upper air layer | Water min gamma: 0.99903, Air max gamma: 1.52e-65 | **PASS** |
| **W3** | Water: Free-Surface Elevation | Free surface gamma = 0.5 bounded in [0.10, 0.17] m | Measured free surface y = 0.1269 m | **PASS** |
| **W4** | Water: Bubble & Atmosphere Leak Check | No trapped air (gamma < 0.99), no water at top | Top patch gamma: 2.29e-66 | **PASS** |
| **W5** | Air: Co-Flow Velocity Profile | Air velocity Ux co-flow profile active for y > 0.28m | Measured air mean Ux = 0.021 m/s | **PASS** |
| **V1** | Velocity: Approach Depth-Avg U | Depth-avg Ux in range [0.10, 0.30] m/s at x = -0.5 m | Measured depth-avg Ux = 0.1888 m/s | **PASS** |
| **V2** | Velocity: Under-Deck Contraction U | Depth-avg Ux in range [0.12, 0.40] m/s under deck | Measured under-deck Ux = 0.2089 m/s | **PASS** |
| **V3** | Velocity: Wake & Jet Anomaly Check | Smooth profile, max |U_fluid| <= 1.0 m/s | Max fluid speed: 0.239 m/s | **PASS** |
| **V4** | Turbulence & Continuity | k > 0, eps > 0, nut <= 5e-3, no NaN in log | Min k: 1.00e-15, Max nut: 1.81e-03 | **PASS** |
| **P1** | Physics: Shields Parameter theta | theta > 0 (near-threshold clear-water flow) | Fit u* = 0.00382 m/s, Shields theta = 0.0039 | **PASS** |
