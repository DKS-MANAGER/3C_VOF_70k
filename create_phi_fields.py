import os

template = """/*--------------------------------*- C++ -*----------------------------------*\\
| =========                 |                                                 |
| \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\\\    /   O peration     | Version:  2412                                  |
|   \\\\  /    A nd           | Website:  www.openfoam.com                      |
|    \\\\/     M anipulation  |                                                 |
\\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       surfaceScalarField;
    location    "0";
    object      PHINAME;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [0 3 -1 0 0 0 0];

internalField   uniform 0;

boundaryField
{
    inlet
    {
        type            calculated;
        value           uniform 0;
    }
    outlet
    {
        type            calculated;
        value           uniform 0;
    }
    bottom
    {
        type            calculated;
        value           uniform 0;
    }
    bridgeDeck
    {
        type            calculated;
        value           uniform 0;
    }
    atmosphere
    {
        type            calculated;
        value           uniform 0;
    }
    frontAndBack
    {
        type            empty;
    }
}

// ************************************************************************* //
"""

for field in ["phi.solid", "phi.water", "phi.gas"]:
    file_path = os.path.join("0_org", field)
    with open(file_path, "w") as f:
        f.write(template.replace("PHINAME", field))
print("Successfully generated initial surfaceScalarFields in 0_org!")
