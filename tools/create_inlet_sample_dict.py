#!/usr/bin/env python3
import os
import glob
import numpy as np
import matplotlib.pyplot as plt

# Create sample dictionary for close-inlet sampling
sample_dict_content = """/*--------------------------------*- C++ -*----------------------------------*\\
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
    object      sampleDict;
}

type sets;
libs ("libsampling.so");

interpolationScheme cellPoint;
setFormat raw;

fields (gamma U.fluid p_rgh alpha.solid);

sets
(
    x_inlet_05cm
    {
        type        uniform;
        axis        y;
        start       (-1.45 -0.05 0.005);
        end         (-1.45  0.25 0.005);
        nPoints     600;
    }
    x_inlet_20cm
    {
        type        uniform;
        axis        y;
        start       (-1.30 -0.05 0.005);
        end         (-1.30  0.25 0.005);
        nPoints     600;
    }
    x_inlet_50cm
    {
        type        uniform;
        axis        y;
        start       (-1.00 -0.05 0.005);
        end         (-1.00  0.25 0.005);
        nPoints     600;
    }
    x_inlet_100cm
    {
        type        uniform;
        axis        y;
        start       (-0.50 -0.05 0.005);
        end         (-0.50  0.25 0.005);
        nPoints     600;
    }
);
"""

os.makedirs('system', exist_ok=True)
with open('system/sampleDict_inletCheck', 'w') as f:
    f.write(sample_dict_content)

print("Created system/sampleDict_inletCheck")
