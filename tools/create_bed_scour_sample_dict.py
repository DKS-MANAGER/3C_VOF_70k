#!/usr/bin/env python3
import os
import glob
import numpy as np

# Create sampling dict for deep bed profiling (y from -0.10 to +0.05 m)
x_stations = np.linspace(-1.50, 1.50, 61)

sample_dict_bed = """/*--------------------------------*- C++ -*----------------------------------*\\
| =========                 |                                                 |
| \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\\\    /   O peration     | Version:  v2412                                 |
|   \\\\  /    A nd           | Project:  Bridge Deck Pressure-Flow Scour Study |
|    \\\\/     M anipulation  | Author:   Divyansh Kumar Singh (IIT Kanpur)     |
\\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    location    "system";
    object      sampleDict_bedScour;
}

type sets;
libs ("libsampling.so");

interpolationScheme cellPoint;
setFormat raw;

fields (alpha.solid);

sets
(
"""

for i, x_val in enumerate(x_stations):
    sample_dict_bed += f"""    line_x_{i:02d}
    {{
        type        uniform;
        axis        y;
        start       ({x_val:.4f} -0.100 0.005);
        end         ({x_val:.4f}  0.050 0.005);
        nPoints     300;
    }}
"""

sample_dict_bed += ");\n"

with open('system/sampleDict_bedScour', 'w') as f:
    f.write(sample_dict_bed)

print("Created system/sampleDict_bedScour for 61 vertical lines across domain.")
