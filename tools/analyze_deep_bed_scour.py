#!/usr/bin/env python3
import os
import glob
import numpy as np

times = [10, 20, 30]
x_stations = np.linspace(-1.50, 1.50, 61)

print("=====================================================================")
print("           3C_VOF_70k EXPLICIT BED SCOUR DEPTH ANALYSIS              ")
print("=====================================================================")

for t in times:
    scour_max = 0.0
    x_max = 0.0
    y_max = 0.0
    
    print(f"\n--- TIME = {t} s ---")
    for i, x_val in enumerate(x_stations):
        pattern = f"postProcessing/sampleDict_bedScour/{t}/line_x_{i:02d}_*.xy"
        files = sorted(glob.glob(pattern))
        if not files: continue
        d = np.loadtxt(files[0])
        y = d[:, 0]
        alpha_solid = d[:, 1]
        
        idx_bed = np.where(alpha_solid >= 0.50)[0]
        if len(idx_bed) > 0:
            y_bed = y[idx_bed[-1]]
            if y_bed < 0.0:
                ds = -y_bed
                if ds > scour_max:
                    scour_max = ds
                    x_max = x_val
                    y_max = y_bed
                if abs(x_val - 0.0765) < 0.03 or abs(x_val - 0.20) < 0.03 or abs(x_val + 0.5) < 0.03:
                    print(f"Station x = {x_val:+6.3f} m: Bed top y = {y_bed:+6.4f} m | Scour depth ds = {ds*1000:5.1f} mm")
                    
    print(f"** ABSOLUTE MAX SCOUR (t = {t} s): ds = {scour_max*1000:.1f} mm at x = {x_max:+6.3f} m (y = {y_max:+6.4f} m) **")
