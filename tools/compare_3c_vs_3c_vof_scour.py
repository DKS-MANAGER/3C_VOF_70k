#!/usr/bin/env python3
import os
import glob
import numpy as np
import matplotlib.pyplot as plt

os.makedirs('validation_20s/scour_analysis', exist_ok=True)

times_3c_vof = [10, 20, 30]
times_3c = [20, 40, 60, 80, 100, 200, 300, 500]
x_stations = np.linspace(-1.50, 1.50, 61)

# Theoretical Equilibrium Scour Depth Calculation for Experiment 03(c):
# Y = 0.1107 m
# Hb = 0.0770 m -> Hb / Y = 0.700
# U_ia = 0.23 m/s
# Vc = 0.2738 m/s -> U_ia / Vc = 0.840
# Fr = 0.221

Y = 0.1107
Hb = 0.0770
U_ia = 0.23
Vc = 0.2738

# 1. Trump (1980) empirical equilibrium scour formula for pressure flow:
# ds_eq / Y = 0.4453 * (U_ia / Vc)^0.7045 * (Hb / Y)^0.2217
ds_eq_trump = Y * 0.4453 * ((U_ia / Vc)**0.7045) * ((Hb / Y)**0.2217)

# 2. Umbrell et al. (1998) pressure-flow scour formula:
# Ys = 0.58 * (U_ia / Vc)^2.2 * (Hb / (Y - Ys))^0.4 * Y -> implicit
# Solving Ys:
ds_eq_umbrell = 0.0473 # 47.3 mm

print("=====================================================================")
print("          THEORETICAL & SIMULATED SCOUR RATE COMPARISON              ")
print("=====================================================================")
print(f"Theoretical Equilibrium Scour Depth (Trump 1980):    {ds_eq_trump*1000:.1f} mm")
print(f"Theoretical Equilibrium Scour Depth (Umbrell 1998):  {ds_eq_umbrell*1000:.1f} mm")
print("---------------------------------------------------------------------")

scour_3c_vof = {}
for t in times_3c_vof:
    ds_max = 0.0
    x_max = 0.0
    for i, x_val in enumerate(x_stations):
        files = sorted(glob.glob(f"postProcessing/sampleDict_bedScour/{t}/line_x_{i:02d}_*.xy"))
        if not files: continue
        d = np.loadtxt(files[0])
        idx = np.where(d[:, 1] >= 0.30)[0] # alpha_solid >= 0.30 for 3C_VOF
        if len(idx) > 0:
            y_bed = d[:, 0][idx[-1]]
            if y_bed < 0.0 and -y_bed > ds_max and x_val > -1.4:
                ds_max = -y_bed
                x_max = x_val
    scour_3c_vof[t] = (ds_max, x_max)
    print(f"3C_VOF_70k (3-Phase) t = {t:3d} s: ds = {ds_max*1000:5.1f} mm at x = {x_max:+6.3f} m")

print("---------------------------------------------------------------------")
scour_3c = {}
for t in times_3c:
    ds_max = 0.0
    x_max = 0.0
    for i, x_val in enumerate(x_stations):
        files = sorted(glob.glob(f"../3C/postProcessing/sampleDict_bedScour_3c/{t}/line_x_{i:02d}_*.xy"))
        if not files: continue
        d = np.loadtxt(files[0])
        idx = np.where(d[:, 1] <= 0.50)[0] # alpha.b <= 0.50 in 3C (alpha.b is water fraction, so bed is alpha.b ~ 0.40)
        if len(idx) > 0:
            y_bed = d[:, 0][idx[-1]]
            if y_bed < 0.0 and -y_bed > ds_max and x_val > -1.4:
                ds_max = -y_bed
                x_max = x_val
    scour_3c[t] = (ds_max, x_max)
    print(f"3C (2-Phase Reference) t = {t:3d} s: ds = {ds_max*1000:5.1f} mm at x = {x_max:+6.3f} m")

print("=====================================================================")

# Plot Scour Depth Evolution vs Time
fig, ax = plt.subplots(figsize=(9, 6))

t_vof = list(scour_3c_vof.keys())
ds_vof = [scour_3c_vof[t][0]*1000 for t in t_vof]

t_ref = list(scour_3c.keys())
ds_ref = [scour_3c[t][0]*1000 for t in t_ref]

ax.plot(t_vof, ds_vof, 'ro-', linewidth=2.5, markersize=8, label='3C_VOF_70k (3-Phase Air-Water-Sediment)')
ax.plot(t_ref, ds_ref, 'bs--', linewidth=2.0, markersize=7, label='3C (2-Phase Reference Case)')

ax.axhline(ds_eq_trump*1000, color='darkgreen', linestyle=':', linewidth=2, label=f'Trump (1980) Equilibrium ({ds_eq_trump*1000:.1f} mm)')
ax.axhline(ds_eq_umbrell*1000, color='purple', linestyle='-.', linewidth=2, label=f'Umbrell (1998) Equilibrium ({ds_eq_umbrell*1000:.1f} mm)')

ax.set_xlabel('Simulation Time t [s]', fontsize=12)
ax.set_ylabel('Maximum Scour Depth ds [mm]', fontsize=12)
ax.set_title('Scour Depth Evolution: 3C_VOF_70k vs 2-Phase Reference 3C vs Theory', fontsize=13, fontweight='bold')
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(fontsize=11, loc='lower right')
plt.tight_layout()
plt.savefig('validation_20s/scour_analysis/scour_depth_temporal_evolution.png', dpi=300)
plt.close()

print("Saved temporal scour evolution plot to validation_20s/scour_analysis/scour_depth_temporal_evolution.png")
