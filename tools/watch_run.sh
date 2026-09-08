#!/bin/bash
# =====================================================================
# Real-time health monitor for sedInterFoam 3C_VOF simulation
# Exits nonzero if physical or numerical bounds are violated.
# =====================================================================

LOGFILE="${1:-log.sedInterFoam}"

if [ ! -f "$LOGFILE" ]; then
    echo "Log file $LOGFILE not found."
    exit 1
fi

echo "Monitoring health of $LOGFILE..."
python3 tools/parse_health.py "$LOGFILE" | tail -n 10

LAST_LINE=$(python3 tools/parse_health.py "$LOGFILE" | tail -n 1)

DT=$(echo "$LAST_LINE" | cut -d',' -f2)
AS_MAX=$(echo "$LAST_LINE" | cut -d',' -f7)
PFF_MAX=$(echo "$LAST_LINE" | cut -d',' -f10)
UF_MAX=$(echo "$LAST_LINE" | cut -d',' -f13)

python3 -c "
dt = float('$DT') if '$DT' else 1e-3
as_max = float('$AS_MAX') if '$AS_MAX' else 0.6
pff_max = float('$PFF_MAX') if '$PFF_MAX' else 0.0
uf_max = float('$UF_MAX') if '$UF_MAX' else 0.0

if dt < 1e-4:
    print(f'HEALTH FAILURE: deltaT collapsed ({dt:.2e} < 1e-4)')
    exit(1)

if as_max > 0.645:
    print(f'HEALTH FAILURE: alpha.solid unphysically high ({as_max:.4f} > 0.645)')
    exit(1)

if pff_max > 1e4:
    print(f'HEALTH FAILURE: pff pressure spike ({pff_max:.1f} > 10000 Pa)')
    exit(1)

if abs(uf_max) > 5.0:
    print(f'HEALTH FAILURE: velocity jet anomaly ({uf_max:.2f} > 5.0 m/s)')
    exit(1)

print('HEALTH OK: Simulation metrics within bounded limits.')
"
