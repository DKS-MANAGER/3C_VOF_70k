#!/usr/bin/env python3
import os
import glob
import numpy as np

sample_dict = """/*--------------------------------*- C++ -*----------------------------------*\\
FoamFile { version 2.0; format ascii; class dictionary; location "system"; object sampleDictHorizontal; }
type sets;
libs ("libsampling.so");
writeControl timeStep;
writeInterval 1;
interpolationScheme cell;
setFormat raw;
sets
(
    line_y0p1107
    {
        type lineUniform;
        axis x;
        start (-1.5 0.1107 0.005);
        end   (0.0  0.1107 0.005);
        nPoints 100;
    }
    line_y0p14
    {
        type lineUniform;
        axis x;
        start (-1.5 0.1400 0.005);
        end   (0.0  0.1400 0.005);
        nPoints 100;
    }
);
fields (gamma);
"""

with open('system/sampleDictHorizontal', 'w') as f:
    f.write(sample_dict)
