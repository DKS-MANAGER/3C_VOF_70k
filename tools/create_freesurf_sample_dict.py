#!/usr/bin/env python3
import os
import glob
import numpy as np
import matplotlib.pyplot as plt

# Create sample dictionary for longitudinal free surface profile (y vs x) along the whole flume
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
    object      sampleDict_freeSurface;
}

type sets;
libs ("libsampling.so");

interpolationScheme cellPoint;
setFormat raw;

fields (gamma alpha.solid);

sets
(
    free_surface_profile
    {
        type        uniform;
        axis        x;
        start       (-1.50  0.1107 0.005);
        end         ( 2.00  0.1107 0.005);
        nPoints     700;
    }
);
"""

os.makedirs('system', exist_ok=True)
with open('system/sampleDict_freeSurface', 'w') as f:
    f.write(sample_dict_content)

print("Created system/sampleDict_freeSurface")
