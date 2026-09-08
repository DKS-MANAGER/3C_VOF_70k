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
#line 31 "/mnt/f/DKS/DKS/Exp_3AC/3C_VOF_70k/0/gamma/boundaryField/inlet"
#include "fvCFD.H"
//}}} end codeInclude


// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

namespace Foam
{

// * * * * * * * * * * * * * * * Local Functions * * * * * * * * * * * * * * //

//{{{ begin localCode

//}}} end localCode


// * * * * * * * * * * * * * * * Global Functions  * * * * * * * * * * * * * //

// dynamicCode:
// SHA1 = 4c7566854b881c54756e8aca4b9b0d13ad83bd3c
//
// unique function name that can be checked if the correct library version
// has been loaded
extern "C" void gammaInletSmooth_4c7566854b881c54756e8aca4b9b0d13ad83bd3c(bool load)
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
    fvPatchScalarField,
    gammaInletSmoothFixedValueFvPatchScalarField
);

} // End namespace Foam


// * * * * * * * * * * * * * * * * Constructors  * * * * * * * * * * * * * * //

Foam::
gammaInletSmoothFixedValueFvPatchScalarField::
gammaInletSmoothFixedValueFvPatchScalarField
(
    const fvPatch& p,
    const DimensionedField<scalar, volMesh>& iF
)
:
    parent_bctype(p, iF)
{
    if (false)
    {
        printMessage("Construct gammaInletSmooth : patch/DimensionedField");
    }
}


Foam::
gammaInletSmoothFixedValueFvPatchScalarField::
gammaInletSmoothFixedValueFvPatchScalarField
(
    const gammaInletSmoothFixedValueFvPatchScalarField& rhs,
    const fvPatch& p,
    const DimensionedField<scalar, volMesh>& iF,
    const fvPatchFieldMapper& mapper
)
:
    parent_bctype(rhs, p, iF, mapper)
{
    if (false)
    {
        printMessage("Construct gammaInletSmooth : patch/DimensionedField/mapper");
    }
}


Foam::
gammaInletSmoothFixedValueFvPatchScalarField::
gammaInletSmoothFixedValueFvPatchScalarField
(
    const fvPatch& p,
    const DimensionedField<scalar, volMesh>& iF,
    const dictionary& dict
)
:
    parent_bctype(p, iF, dict)
{
    if (false)
    {
        printMessage("Construct gammaInletSmooth : patch/dictionary");
    }
}


Foam::
gammaInletSmoothFixedValueFvPatchScalarField::
gammaInletSmoothFixedValueFvPatchScalarField
(
    const gammaInletSmoothFixedValueFvPatchScalarField& rhs
)
:
    parent_bctype(rhs),
    dictionaryContent(rhs)
{
    if (false)
    {
        printMessage("Copy construct gammaInletSmooth");
    }
}


Foam::
gammaInletSmoothFixedValueFvPatchScalarField::
gammaInletSmoothFixedValueFvPatchScalarField
(
    const gammaInletSmoothFixedValueFvPatchScalarField& rhs,
    const DimensionedField<scalar, volMesh>& iF
)
:
    parent_bctype(rhs, iF)
{
    if (false)
    {
        printMessage("Construct gammaInletSmooth : copy/DimensionedField");
    }
}


// * * * * * * * * * * * * * * * * Destructor  * * * * * * * * * * * * * * * //

Foam::
gammaInletSmoothFixedValueFvPatchScalarField::
~gammaInletSmoothFixedValueFvPatchScalarField()
{
    if (false)
    {
        printMessage("Destroy gammaInletSmooth");
    }
}


// * * * * * * * * * * * * * * * Member Functions  * * * * * * * * * * * * * //

void
Foam::
gammaInletSmoothFixedValueFvPatchScalarField::updateCoeffs()
{
    if (this->updated())
    {
        return;
    }

    if (false)
    {
        printMessage("updateCoeffs gammaInletSmooth");
    }

//{{{ begin code
    #line 48 "/mnt/f/DKS/DKS/Exp_3AC/3C_VOF_70k/0/gamma/boundaryField/inlet"
// Smooth 3mm tanh transition centered at the equilibrium backwater height Y = 0.1620 m
            // Eliminates inlet step jump and water-air interface distortion at x = -1.5 m
            const fvPatch& boundaryPatch = patch();
            const vectorField& Cf = boundaryPatch.Cf();
            scalarField& field = *this;
            const scalar ySurf = 0.1620;

            forAll(Cf, faceI)
            {
                scalar yVal = Cf[faceI].y();
                if (yVal <= 0.0)
                {
                    field[faceI] = 1.0;
                }
                else
                {
                    field[faceI] = 0.5 * (1.0 - tanh((yVal - ySurf) / 0.003));
                }
            }
//}}} end code

    this->parent_bctype::updateCoeffs();
}


// ************************************************************************* //

