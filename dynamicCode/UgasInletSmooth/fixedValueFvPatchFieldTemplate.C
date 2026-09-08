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
#line 31 "/mnt/f/DKS/DKS/Exp_3AC/3C_VOF_70k/0/U.gas/boundaryField/inlet"
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
// SHA1 = ffcd70c4b1a06f320a025549cc9d9a522d686a6d
//
// unique function name that can be checked if the correct library version
// has been loaded
extern "C" void UgasInletSmooth_ffcd70c4b1a06f320a025549cc9d9a522d686a6d(bool load)
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
    UgasInletSmoothFixedValueFvPatchVectorField
);

} // End namespace Foam


// * * * * * * * * * * * * * * * * Constructors  * * * * * * * * * * * * * * //

Foam::
UgasInletSmoothFixedValueFvPatchVectorField::
UgasInletSmoothFixedValueFvPatchVectorField
(
    const fvPatch& p,
    const DimensionedField<vector, volMesh>& iF
)
:
    parent_bctype(p, iF)
{
    if (false)
    {
        printMessage("Construct UgasInletSmooth : patch/DimensionedField");
    }
}


Foam::
UgasInletSmoothFixedValueFvPatchVectorField::
UgasInletSmoothFixedValueFvPatchVectorField
(
    const UgasInletSmoothFixedValueFvPatchVectorField& rhs,
    const fvPatch& p,
    const DimensionedField<vector, volMesh>& iF,
    const fvPatchFieldMapper& mapper
)
:
    parent_bctype(rhs, p, iF, mapper)
{
    if (false)
    {
        printMessage("Construct UgasInletSmooth : patch/DimensionedField/mapper");
    }
}


Foam::
UgasInletSmoothFixedValueFvPatchVectorField::
UgasInletSmoothFixedValueFvPatchVectorField
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
        printMessage("Construct UgasInletSmooth : patch/dictionary");
    }
}


Foam::
UgasInletSmoothFixedValueFvPatchVectorField::
UgasInletSmoothFixedValueFvPatchVectorField
(
    const UgasInletSmoothFixedValueFvPatchVectorField& rhs
)
:
    parent_bctype(rhs),
    dictionaryContent(rhs)
{
    if (false)
    {
        printMessage("Copy construct UgasInletSmooth");
    }
}


Foam::
UgasInletSmoothFixedValueFvPatchVectorField::
UgasInletSmoothFixedValueFvPatchVectorField
(
    const UgasInletSmoothFixedValueFvPatchVectorField& rhs,
    const DimensionedField<vector, volMesh>& iF
)
:
    parent_bctype(rhs, iF)
{
    if (false)
    {
        printMessage("Construct UgasInletSmooth : copy/DimensionedField");
    }
}


// * * * * * * * * * * * * * * * * Destructor  * * * * * * * * * * * * * * * //

Foam::
UgasInletSmoothFixedValueFvPatchVectorField::
~UgasInletSmoothFixedValueFvPatchVectorField()
{
    if (false)
    {
        printMessage("Destroy UgasInletSmooth");
    }
}


// * * * * * * * * * * * * * * * Member Functions  * * * * * * * * * * * * * //

void
Foam::
UgasInletSmoothFixedValueFvPatchVectorField::updateCoeffs()
{
    if (this->updated())
    {
        return;
    }

    if (false)
    {
        printMessage("updateCoeffs UgasInletSmooth");
    }

//{{{ begin code
    #line 49 "/mnt/f/DKS/DKS/Exp_3AC/3C_VOF_70k/0/U.gas/boundaryField/inlet"
const fvPatch& boundaryPatch = patch();
            const vectorField& Cf = boundaryPatch.Cf();
            vectorField& field = *this;

            const scalar ySurf = 0.1620;
            const scalar qWater = 0.0254667;
            const scalar Umax = (8.0 / 7.0) * (qWater / ySurf);
            const scalar Uair = 0.10;

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

