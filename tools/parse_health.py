#!/usr/bin/env python3
import sys
import re
import csv

def parse_log(log_path):
    time_re = re.compile(r"^Time = ([0-9\.eE\+\-]+)")
    deltaT_re = re.compile(r"deltaT = ([0-9\.eE\+\-]+)")
    co_re = re.compile(r"Courant Number mean: ([0-9\.eE\+\-]+) max: ([0-9\.eE\+\-]+)")
    urco_re = re.compile(r"Max Ur Courant Number = ([0-9\.eE\+\-]+)")
    alphas_re = re.compile(r"Min\(alphas\) = ([0-9\.eE\+\-]+)\s+Max\(alphas\) = ([0-9\.eE\+\-]+)")
    gamma_re = re.compile(r"Min\(alpha\.water\) = ([0-9\.eE\+\-]+)\s+Max\(alpha\.water\) = ([0-9\.eE\+\-]+)")
    pff_re = re.compile(r"Contact pressure\s+pff:\s*Min =([0-9\.eE\+\-]+),\s*Max =([0-9\.eE\+\-]+)")
    ps_re = re.compile(r"Shear ind\. press\.\s+ps:\s*Min =([0-9\.eE\+\-]+),\s*Max =([0-9\.eE\+\-]+)")
    uf_re = re.compile(r"min\(Uf\) = \(([0-9\.eE\+\-]+)\s+([0-9\.eE\+\-]+)\s+([0-9\.eE\+\-]+)\)\s*max\(Uf\) = \(([0-9\.eE\+\-]+)\s+([0-9\.eE\+\-]+)\s+([0-9\.eE\+\-]+)\)")
    us_re = re.compile(r"min\(Us\) = \(([0-9\.eE\+\-]+)\s+([0-9\.eE\+\-]+)\s+([0-9\.eE\+\-]+)\)\s*max\(Us\) = \(([0-9\.eE\+\-]+)\s+([0-9\.eE\+\-]+)\s+([0-9\.eE\+\-]+)\)")
    cont_re = re.compile(r"time step continuity errors : .* cumulative = ([0-9\.eE\+\-]+)")

    records = []
    curr = {}

    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            tm = time_re.search(line)
            if tm:
                if curr and 't' in curr:
                    records.append(curr)
                curr = {'t': float(tm.group(1))}
                continue

            dt_m = deltaT_re.search(line)
            if dt_m:
                curr['deltaT'] = float(dt_m.group(1))

            co_m = co_re.search(line)
            if co_m:
                curr['Co_mean'] = float(co_m.group(1))
                curr['Co_max'] = float(co_m.group(2))

            ur_m = urco_re.search(line)
            if ur_m:
                curr['UrCo'] = float(ur_m.group(1))

            as_m = alphas_re.search(line)
            if as_m:
                curr['alphaS_min'] = float(as_m.group(1))
                curr['alphaS_max'] = float(as_m.group(2))

            g_m = gamma_re.search(line)
            if g_m:
                curr['gamma_min'] = float(g_m.group(1))
                curr['gamma_max'] = float(g_m.group(2))

            pff_m = pff_re.search(line)
            if pff_m:
                curr['pff_max'] = float(pff_m.group(2))

            ps_m = ps_re.search(line)
            if ps_m:
                curr['ps_max'] = float(ps_m.group(2))

            uf_m = uf_re.search(line)
            if uf_m:
                curr['Uf_min_x'] = float(uf_m.group(1))
                curr['Uf_min_y'] = float(uf_m.group(2))
                curr['Uf_max_x'] = float(uf_m.group(4))
                curr['Uf_max_y'] = float(uf_m.group(5))

            us_m = us_re.search(line)
            if us_m:
                min_x, min_y, min_z = float(us_m.group(1)), float(us_m.group(2)), float(us_m.group(3))
                max_x, max_y, max_z = float(us_m.group(4)), float(us_m.group(5)), float(us_m.group(6))
                curr['Us_max_mag'] = max((min_x**2 + min_y**2 + min_z**2)**0.5, (max_x**2 + max_y**2 + max_z**2)**0.5)

            c_m = cont_re.search(line)
            if c_m:
                curr['cont_cum'] = float(c_m.group(1))

    if curr and 't' in curr:
        records.append(curr)

    return records

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: parse_health.py <log.sedInterFoam>")
        sys.exit(1)

    log_file = sys.argv[1]
    recs = parse_log(log_file)
    fields = ['t', 'deltaT', 'Co_mean', 'Co_max', 'UrCo', 'alphaS_min', 'alphaS_max',
              'gamma_min', 'gamma_max', 'pff_max', 'ps_max', 'Uf_min_x', 'Uf_max_x',
              'Uf_min_y', 'Uf_max_y', 'Us_max_mag', 'cont_cum']

    writer = csv.DictWriter(sys.stdout, fieldnames=fields)
    writer.writeheader()
    for r in recs:
        row = {f: r.get(f, '') for f in fields}
        writer.writerow(row)
