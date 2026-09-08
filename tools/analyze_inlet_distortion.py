#!/usr/bin/env python3
import os
import glob
import numpy as np
import matplotlib.pyplot as plt

os.makedirs('validation_20s/inlet_check', exist_ok=True)

times = [10, 20, 30]
sets = ['x_inlet_05cm', 'x_inlet_20cm', 'x_inlet_50cm', 'x_inlet_100cm']
labels = {'x_inlet_05cm': 'x = -1.45 m (5 cm from inlet)',
          'x_inlet_20cm': 'x = -1.30 m (20 cm from inlet)',
          'x_inlet_50cm': 'x = -1.00 m (50 cm from inlet)',
          'x_inlet_100cm': 'x = -0.50 m (100 cm from inlet)'}

def load_inlet_set(t, setName):
    pattern = f"postProcessing/sampleDict_inletCheck/{t}/{setName}_*.xy"
    files = sorted(glob.glob(pattern))
    if not files:
        raise FileNotFoundError(f"No file for {pattern}")
    d = np.loadtxt(files[0])
    return {
        'y': d[:, 0],
        'alpha_solid': d[:, 1],
        'gamma': d[:, 2],
        'p_rgh': d[:, 3],
        'Ux': d[:, 4],
        'Uy': d[:, 5],
        'Uz': d[:, 6]
    }

print("=====================================================================")
print("             INLET WATER-AIR INTERFACE DISTORTION CHECK              ")
print("=====================================================================")

report_lines = []
report_lines.append("# Inlet Water-Air Interface Distortion Analysis Report (t = 30 s)\n")
report_lines.append("## 1. Interface Smoothness & Spurious Velocity Assessment\n")

for t in times:
    print(f"\n--- TIME = {t} s ---")
    report_lines.append(f"\n### Time t = {t} s\n")
    for s in sets:
        try:
            d = load_inlet_set(t, s)
            y = d['y']
            gamma = d['gamma']
            Ux = d['Ux']
            Uy = d['Uy']
            
            # Interface region y in [0.08, 0.14] m
            idx_int = np.where((y >= 0.08) & (y <= 0.14))[0]
            
            # Interface location (gamma = 0.5)
            idx_50 = np.where(gamma >= 0.5)[0]
            y_int = y[idx_50[-1]] if len(idx_50) > 0 else 0.1107
            
            # Interface thickness delta_y (gamma 0.1 to 0.9)
            idx_10 = np.where(gamma >= 0.9)[0]
            idx_90 = np.where(gamma >= 0.1)[0]
            y_top_int = y[idx_10[-1]] if len(idx_10) > 0 else y_int
            y_bot_int = y[idx_90[0]] if len(idx_90) > 0 else y_int
            thick_mm = (y_top_int - y_bot_int) * 1000.0
            
            # Spurious vertical velocity inside interface
            max_Uy_int = np.max(np.abs(Uy[idx_int])) if len(idx_int) > 0 else 0.0
            max_dgamma = np.max(np.abs(np.diff(gamma))) if len(gamma) > 1 else 0.0
            
            status = "CLEAN & SMOOTH" if max_Uy_int < 0.05 and thick_mm < 15.0 else "DISTORTED"
            
            msg = f"{labels[s]}: Interface y = {y_int:.4f} m | Thickness = {thick_mm:.1f} mm | Max |Uy| spurious = {max_Uy_int:.4f} m/s | [{status}]"
            print(msg)
            report_lines.append(f"- **{labels[s]}**: Free surface $y = {y_int:.4f}\\text{{ m}}$, interface transition thickness = ${thick_mm:.1f}\\text{{ mm}}$, max $|U_y|$ spurious current = ${max_Uy_int:.4f}\\text{{ m/s}}$ -> **{status}**")
        except Exception as e:
            print(f"Error {s} t={t}: {e}")

# Plot gamma profiles near inlet at t = 30s
fig, ax = plt.subplots(figsize=(8, 6))
t_latest = 30
for s in sets:
    try:
        d = load_inlet_set(t_latest, s)
        ax.plot(d['gamma'], d['y'], label=labels[s], linewidth=2)
    except:
        pass
ax.axhline(0.1107, color='blue', linestyle='--', label='Initial Depth (y = 0.1107 m)')
ax.set_xlim(-0.05, 1.05)
ax.set_ylim(0.08, 0.15)
ax.set_xlabel('Water VOF Fraction gamma [-]')
ax.set_ylabel('Vertical Coordinate y [m]')
ax.set_title(f'Inlet Region Water-Air Interface Profile (t = {t_latest} s)')
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend()
plt.tight_layout()
plt.savefig('validation_20s/inlet_check/inlet_gamma_profiles_t30.png', dpi=300)
plt.close()

# Plot Ux profiles near inlet at t = 30s
fig, ax = plt.subplots(figsize=(8, 6))
for s in sets:
    try:
        d = load_inlet_set(t_latest, s)
        ax.plot(d['Ux'], d['y'], label=labels[s], linewidth=2)
    except:
        pass
ax.axvline(0.23, color='red', linestyle='--', label='Target Approach Ux = 0.23 m/s')
ax.axhline(0.1107, color='blue', linestyle=':', label='Free Surface (y = 0.1107 m)')
ax.set_ylim(-0.02, 0.25)
ax.set_xlabel('Horizontal Velocity Ux [m/s]')
ax.set_ylabel('Vertical Coordinate y [m]')
ax.set_title(f'Inlet Region Horizontal Velocity Profile (t = {t_latest} s)')
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend()
plt.tight_layout()
plt.savefig('validation_20s/inlet_check/inlet_Ux_profiles_t30.png', dpi=300)
plt.close()

# Plot Uy profiles near inlet at t = 30s
fig, ax = plt.subplots(figsize=(8, 6))
for s in sets:
    try:
        d = load_inlet_set(t_latest, s)
        ax.plot(d['Uy'], d['y'], label=labels[s], linewidth=2)
    except:
        pass
ax.axvline(0.0, color='black', linestyle='--', label='Zero Vertical Velocity')
ax.axhline(0.1107, color='blue', linestyle=':', label='Free Surface (y = 0.1107 m)')
ax.set_ylim(0.08, 0.15)
ax.set_xlabel('Vertical Velocity Uy [m/s]')
ax.set_ylabel('Vertical Coordinate y [m]')
ax.set_title(f'Inlet Region Spurious Vertical Velocity Uy (t = {t_latest} s)')
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend()
plt.tight_layout()
plt.savefig('validation_20s/inlet_check/inlet_Uy_spurious_t30.png', dpi=300)
plt.close()

with open('validation_20s/inlet_check/INLET_INTERFACE_REPORT.md', 'w') as f:
    f.write("\n".join(report_lines))

print("\nInlet interface distortion analysis complete. Report written to validation_20s/inlet_check/INLET_INTERFACE_REPORT.md")
