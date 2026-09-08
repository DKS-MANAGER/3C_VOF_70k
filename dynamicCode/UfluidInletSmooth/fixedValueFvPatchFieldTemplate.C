/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     |
    \\  /    A nd           | www.openfoam.com
     \\/     M anipulation  |
-------------------------------------------------------------------------------
    Copyright (C) 2019-2021 OpenCFD Ltd.
    Copyright (C) YEAR AUTHOR, AFFILIATION
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM.  If not, see <http://www.gnu.org/licenses/>.

\*---------------------------------------------------------------------------*/

#include "fixedValueFvPatchFieldTemplate.H"
#include "addToRunTimeSelectionTable.H"
#include "fvPatchFieldMapper.H"
#include "volFields.H"
#include "surfaceFields.H"
#include "unitConversion.H"
#include "PatchFunction1.H"

//{{{ begin codeInclude
#line 31 "/mnt/f/DKS/DKS/Exp_3AC/3C_VOF_70k/0/U.fluid/boundaryField/inlet"
#include "fvCFD.H"
            #include <cmath>
//}}} end codeInclude


// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

namespace Foam
{

// * * * * * * * * * * * * * * * Local Functions * * * * * * * * * * * * * * //

//{{{ begin localCode

//}}} end localCode


// * * * * * * * * * * * * * * * Global Functions  * * * * * * * * * * * * * //

// dynamicCode:
// SHA1 = a17575968bf7f66ed8f3f7c28bcb34edd7a291ed
//
// unique function name that can be checked if the correct library version
// has been loaded
extern "C" void UfluidInletSmooth_a17575968bf7f66ed8f3f7c28bcb34edd7a291ed(bool load)
{
    if (load)
    {
        // Code that can be explicitly executed after loading
    }
    else
    {
        // Code that can be explicitly executed before unloading
    }
}

// * * * * * * * * * * * * * * Static Data Members * * * * * * * * * * * * * //

makeRemovablePatchTypeField
(
    fvPatchVectorField,
    UfluidInletSmoothFixedValueFvPatchVectorField
);

} // End namespace Foam


// * * * * * * * * * * * * * * * * Constructors  * * * * * * * * * * * * * * //

Foam::
UfluidInletSmoothFixedValueFvPatchVectorField::
UfluidInletSmoothFixedValueFvPatchVectorField
(
    const fvPatch& p,
    const DimensionedField<vector, volMesh>& iF
)
:
    parent_bctype(p, iF)
{
    if (false)
    {
        printMessage("Construct UfluidInletSmooth : patch/DimensionedField");
    }
}


Foam::
UfluidInletSmoothFixedValueFvPatchVectorField::
UfluidInletSmoothFixedValueFvPatchVectorField
(
    const UfluidInletSmoothFixedValueFvPatchVectorField& rhs,
    const fvPatch& p,
    const DimensionedField<vector, volMesh>& iF,
    const fvPatchFieldMapper& mapper
)
:
    parent_bctype(rhs, p, iF, mapper)
{
    if (false)
    {
        printMessage("Construct UfluidInletSmooth : patch/DimensionedField/mapper");
    }
}


Foam::
UfluidInletSmoothFixedValueFvPatchVectorField::
UfluidInletSmoothFixedValueFvPatchVectorField
(
    const fvPatch& p,
    const DimensionedField<vector, volMesh>& iF,
    const dictionary& dict
)
:
    parent_bctype(p, iF, dict)
{
    if (false)
    {
        printMessage("Construct UfluidInletSmooth : patch/dictionary");
    }
}


Foam::
UfluidInletSmoothFixedValueFvPatchVectorField::
UfluidInletSmoothFixedValueFvPatchVectorField
(
    const UfluidInletSmoothFixedValueFvPatchVectorField& rhs
)
:
    parent_bctype(rhs),
    dictionaryContent(rhs)
{
    if (false)
    {
        printMessage("Copy construct UfluidInletSmooth");
    }
}


Foam::
UfluidInletSmoothFixedValueFvPatchVectorField::
UfluidInletSmoothFixedValueFvPatchVectorField
(
    const UfluidInletSmoothFixedValueFvPatchVectorField& rhs,
    const DimensionedField<vector, volMesh>& iF
)
:
    parent_bctype(rhs, iF)
{
    if (false)
    {
        printMessage("Construct UfluidInletSmooth : copy/DimensionedField");
    }
}


// * * * * * * * * * * * * * * * * Destructor  * * * * * * * * * * * * * * * //

Foam::
UfluidInletSmoothFixedValueFvPatchVectorField::
~UfluidInletSmoothFixedValueFvPatchVectorField()
{
    if (false)
    {
        printMessage("Destroy UfluidInletSmooth");
    }
}


// * * * * * * * * * * * * * * * Member Functions  * * * * * * * * * * * * * //

void
Foam::
UfluidInletSmoothFixedValueFvPatchVectorField::updateCoeffs()
{
    if (this->updated())
    {
        return;
    }

    if (false)
    {
        printMessage("updateCoeffs UfluidInletSmooth");
    }

//{{{ begin code
    #line 49 "/mnt/f/DKS/DKS/Exp_3AC/3C_VOF_70k/0/U.fluid/boundaryField/inlet"
// Smooth 1/7th power-law water inflow profile for Q = 7.64 L/s (q = 0.02547 m^2/s)
            // Matched to the backwater surface elevation Y = 0.1620 m
            const fvPatch& boundaryPatch = patch();
            const vectorField& Cf = boundaryPatch.Cf();
            vectorField& field = *this;

            const scalar ySurf = 0.1620;
            const scalar qWater = 0.0254667; // 7.64 L/s per W=0.30m
            const scalar Umax = (8.0 / 7.0) * (qWater / ySurf); // 0.1795 m/s
            const scalar Uair = 0.10; // Air co-flow velocity

            forAll(Cf, faceI)
            {
                scalar yVal = Cf[faceI].y();
                scalar gammaVal = 0.5 * (1.0 - tanh((yVal - ySurf) / 0.003));
                if (yVal <= 0.0)
                {
                    gammaVal = 1.0;
                }

                scalar uWater = 0.0;
                if (yVal <= 0.0)
                {
                    uWater = 0.0;
                }
                else if (yVal <= ySurf)
                {
                    uWater = Umax * std::pow(std::max(0.0, yVal / ySurf), 1.0 / 7.0);
                }
                else
                {
                    uWater = Umax;
                }

                scalar uX = gammaVal * uWater + (1.0 - gammaVal) * Uair;
                field[faceI] = vector(uX, 0.0, 0.0);
            }
//}}} end code

    this->parent_bctype::updateCoeffs();
}


// ************************************************************************* //

