#!/usr/bin/env python3
import os
import glob
import numpy as np
import matplotlib.pyplot as plt

os.makedirs('validation_20s/inlet_check', exist_ok=True)

times = [10, 20, 30]
n_y = 60
y_levels = np.linspace(-0.02, 0.24, n_y)

def process_2d_time(t):
    # Load all 60 line files for time t
    x_uniform = np.linspace(-1.50, 2.00, 350)
    gamma_grid = []
    ux_grid = []
    uy_grid = []
    
    for i, y_val in enumerate(y_levels):
        pattern = f"postProcessing/sampleDict_2DGrid/{t}/line_y_{i:02d}_*.xy"
        files = sorted(glob.glob(pattern))
        if not files:
            print(f"Missing file for time {t}, line {i}")
            return None
        d = np.loadtxt(files[0])
        x_line = d[:, 0]
        gamma_line = d[:, 2] # gamma is column 2
        ux_line = d[:, 3]    # Ux is column 3
        uy_line = d[:, 4]    # Uy is column 4
        
        # Interpolate onto x_uniform
        g_interp = np.interp(x_uniform, x_line, gamma_line)
        ux_interp = np.interp(x_uniform, x_line, ux_line)
        uy_interp = np.interp(x_uniform, x_line, uy_line)
        
        gamma_grid.append(g_interp)
        ux_grid.append(ux_interp)
        uy_grid.append(uy_interp)
        
    Gamma = np.array(gamma_grid) # shape (60, 350)
    Ux = np.array(ux_grid)
    Uy = np.array(uy_grid)
    X, Y = np.meshgrid(x_uniform, y_levels)
    x_coords = x_uniform
    
    # Track free surface y_surf(x) where Gamma = 0.5 for y >= 0.02 m
    y_surf = []
    idx_above_bed = np.where(y_levels >= 0.02)[0]
    for col in range(len(x_coords)):
        g_col = Gamma[idx_above_bed, col]
        y_col = y_levels[idx_above_bed]
        idx = np.where(g_col >= 0.5)[0]
        if len(idx) > 0 and idx[-1] < len(y_col) - 1:
            i1 = idx[-1]
            i2 = i1 + 1
            g1, g2 = g_col[i1], g_col[i2]
            y1, y2 = y_col[i1], y_col[i2]
            if abs(g2 - g1) > 1e-5:
                y_s = y1 + (0.5 - g1) * (y2 - y1) / (g2 - g1)
            else:
                y_s = y1
        else:
            y_s = 0.1107
        y_surf.append(y_s)
        
    return X, Y, Gamma, Ux, Uy, x_coords, np.array(y_surf)

fig, ax = plt.subplots(figsize=(12, 5))

for t in times:
    res = process_2d_time(t)
    if res is not None:
        X, Y, Gamma, Ux, Uy, x_coords, y_surf = res
        ax.plot(x_coords, y_surf, label=f'Water Surface t = {t} s', linewidth=2)

# Draw bridge deck rectangle
ax.axvspan(0.0, 0.153, ymin=(0.0770 - (-0.02))/0.26, ymax=(0.1470 - (-0.02))/0.26, color='gray', alpha=0.5, label='Bridge Deck (y: 0.077 to 0.147 m)')
ax.axhline(0.1107, color='blue', linestyle='--', label='Initial Depth (y = 0.1107 m)')
ax.axhline(0.0, color='brown', linestyle='-', label='Initial Sediment Bed (y = 0.0 m)')

ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-0.02, 0.22)
ax.set_xlabel('Longitudinal Distance x [m]')
ax.set_ylabel('Vertical Elevation y [m]')
ax.set_title('Longitudinal Water Surface Elevation & Backwater Curve Profile')
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='upper right')
plt.tight_layout()
plt.savefig('validation_20s/inlet_check/longitudinal_water_surface_profile.png', dpi=300)
plt.close()

print("Longitudinal water surface profile saved to validation_20s/inlet_check/longitudinal_water_surface_profile.png")
