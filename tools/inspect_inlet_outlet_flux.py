#!/usr/bin/env python3
import os
import glob
import numpy as np

time_dirs = sorted([int(os.path.basename(p)) for p in glob.glob("postProcessing/sampleDict/*") if os.path.basename(p).isdigit()])
stations = ['-0.5', '0.0765', '0.4', '0.8']

for t in time_dirs:
    print(f"\n==================== TIME {t} s ====================")
    for st in stations:
        p_file = f"postProcessing/sampleDict/{t}/x_{st.replace('-','minus').replace('.','p')}_alpha.solid_epsilon.fluid_gamma_k.fluid_nut.fluid_p_rgh_U.fluid_U.solid.xy"
        if not os.path.exists(p_file):
            continue
        data = np.loadtxt(p_file)
        y = data[:, 0]
        asolid = data[:, 1]
        gamma = data[:, 3]
        prgh = data[:, 6]
        ux = data[:, 7]
        
        # Calculate water flux Q_water = int gamma * Ux dy
        dy = np.gradient(y)
        q_water = np.sum(gamma * ux * dy)
        q_air = np.sum((1.0 - gamma) * (1.0 - asolid) * ux * dy)
        
        # Water surface y (where gamma = 0.5)
        idx_surf = np.where(gamma >= 0.5)[0]
        y_surf = y[idx_surf[-1]] if len(idx_surf) > 0 else 0.1107
        
        # Bed top y (where asolid = 0.5)
        idx_bed = np.where(asolid >= 0.5)[0]
        y_bed = y[idx_bed[-1]] if len(idx_bed) > 0 else 0.0
        
        print(f"Station x = {st:>6}m | Q_water = {q_water:.5f} m²/s | Q_air = {q_air:.5f} m²/s | Bed y = {y_bed:+.4f}m | FreeSurf y = {y_surf:+.4f}m | max(p_rgh) = {np.max(prgh):.1f} Pa")
