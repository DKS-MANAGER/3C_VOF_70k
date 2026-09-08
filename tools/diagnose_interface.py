#!/usr/bin/env python3
import os
import numpy as np

# Analyze reconstruct time fields if present or sampleDict
times = [2, 10, 20]
for t in times:
    print(f"=== TIME {t} s ===")
    p_file = f"postProcessing/sampleDict/{t}/x_minus0p5_alpha.solid_epsilon.fluid_gamma_k.fluid_nut.fluid_p_rgh_U.fluid_U.solid.xy"
    if os.path.exists(p_file):
        d = np.loadtxt(p_file)
        y = d[:, 0]
        gamma = d[:, 3]
        ux = d[:, 7]
        idx_water = np.where(gamma >= 0.5)[0]
        if len(idx_water) > 0:
            y_bed = y[np.where(d[:, 1] >= 0.5)[0][-1]] if len(np.where(d[:, 1] >= 0.5)[0]) > 0 else 0.0
            y_surf = y[idx_water[-1]]
            h_water = y_surf - y_bed
            u_avg = np.mean(ux[idx_water])
            print(f"  Station x = -0.5m: Bed top y = {y_bed:.4f}m, Free surface y = {y_surf:.4f}m, Water depth = {h_water:.4f}m, U_avg = {u_avg:.4f}m/s")
        
    p_deck = f"postProcessing/sampleDict/{t}/x_0p0765_alpha.solid_epsilon.fluid_gamma_k.fluid_nut.fluid_p_rgh_U.fluid_U.solid.xy"
    if os.path.exists(p_deck):
        d = np.loadtxt(p_deck)
        y = d[:, 0]
        gamma = d[:, 3]
        ux = d[:, 7]
        idx_water = np.where(gamma >= 0.5)[0]
        if len(idx_water) > 0:
            y_surf = y[idx_water[-1]]
            u_avg = np.mean(ux[idx_water])
            print(f"  Station x = 0.0765m (Under deck): Free surface y = {y_surf:.4f}m, U_avg = {u_avg:.4f}m/s")
