#!/usr/bin/env python3
import os
import glob
import numpy as np
import matplotlib.pyplot as plt

os.makedirs('validation_20s/inlet_check', exist_ok=True)

# Generate a 2D sampling dict (grid of lines along x at different y levels)
n_y = 60
y_levels = np.linspace(-0.02, 0.24, n_y)

sample_dict_2d = """/*--------------------------------*- C++ -*----------------------------------*\\
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
    object      sampleDict_2DGrid;
}

type sets;
libs ("libsampling.so");

interpolationScheme cellPoint;
setFormat raw;

fields (gamma U.fluid alpha.solid);

sets
(
"""

for i, y_val in enumerate(y_levels):
    sample_dict_2d += f"""    line_y_{i:02d}
    {{
        type        uniform;
        axis        x;
        start       (-1.50 {y_val:.4f} 0.005);
        end         ( 2.00 {y_val:.4f} 0.005);
        nPoints     350;
    }}
"""

sample_dict_2d += ");\n"

with open('system/sampleDict_2DGrid', 'w') as f:
    f.write(sample_dict_2d)

print("Created system/sampleDict_2DGrid with 60 horizontal lines across domain.")
