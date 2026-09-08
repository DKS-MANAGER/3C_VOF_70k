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
#line 63 "/mnt/f/DKS/DKS/Exp_3AC/3C_VOF_70k/0/omega.fluid/boundaryField/inlet"
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
// SHA1 = 7e092f2edabe5ffb1e93bd371710e4c061722311
//
// unique function name that can be checked if the correct library version
// has been loaded
extern "C" void inlet_omega_01a_7e092f2edabe5ffb1e93bd371710e4c061722311(bool load)
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
    inlet_omega_01aFixedValueFvPatchScalarField
);

} // End namespace Foam


// * * * * * * * * * * * * * * * * Constructors  * * * * * * * * * * * * * * //

Foam::
inlet_omega_01aFixedValueFvPatchScalarField::
inlet_omega_01aFixedValueFvPatchScalarField
(
    const fvPatch& p,
    const DimensionedField<scalar, volMesh>& iF
)
:
    parent_bctype(p, iF)
{
    if (false)
    {
        printMessage("Construct inlet_omega_01a : patch/DimensionedField");
    }
}


Foam::
inlet_omega_01aFixedValueFvPatchScalarField::
inlet_omega_01aFixedValueFvPatchScalarField
(
    const inlet_omega_01aFixedValueFvPatchScalarField& rhs,
    const fvPatch& p,
    const DimensionedField<scalar, volMesh>& iF,
    const fvPatchFieldMapper& mapper
)
:
    parent_bctype(rhs, p, iF, mapper)
{
    if (false)
    {
        printMessage("Construct inlet_omega_01a : patch/DimensionedField/mapper");
    }
}


Foam::
inlet_omega_01aFixedValueFvPatchScalarField::
inlet_omega_01aFixedValueFvPatchScalarField
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
        printMessage("Construct inlet_omega_01a : patch/dictionary");
    }
}


Foam::
inlet_omega_01aFixedValueFvPatchScalarField::
inlet_omega_01aFixedValueFvPatchScalarField
(
    const inlet_omega_01aFixedValueFvPatchScalarField& rhs
)
:
    parent_bctype(rhs),
    dictionaryContent(rhs)
{
    if (false)
    {
        printMessage("Copy construct inlet_omega_01a");
    }
}


Foam::
inlet_omega_01aFixedValueFvPatchScalarField::
inlet_omega_01aFixedValueFvPatchScalarField
(
    const inlet_omega_01aFixedValueFvPatchScalarField& rhs,
    const DimensionedField<scalar, volMesh>& iF
)
:
    parent_bctype(rhs, iF)
{
    if (false)
    {
        printMessage("Construct inlet_omega_01a : copy/DimensionedField");
    }
}


// * * * * * * * * * * * * * * * * Destructor  * * * * * * * * * * * * * * * //

Foam::
inlet_omega_01aFixedValueFvPatchScalarField::
~inlet_omega_01aFixedValueFvPatchScalarField()
{
    if (false)
    {
        printMessage("Destroy inlet_omega_01a");
    }
}


// * * * * * * * * * * * * * * * Member Functions  * * * * * * * * * * * * * //

void
Foam::
inlet_omega_01aFixedValueFvPatchScalarField::updateCoeffs()
{
    if (this->updated())
    {
        return;
    }

    if (false)
    {
        printMessage("updateCoeffs inlet_omega_01a");
    }

//{{{ begin code
    #line 77 "/mnt/f/DKS/DKS/Exp_3AC/3C_VOF_70k/0/omega.fluid/boundaryField/inlet"
const fvPatch& boundaryPatch = patch();
            const vectorField& Cf = boundaryPatch.Cf();
            scalarField& field = *this;
            forAll(Cf, faceI)
            {
                if (Cf[faceI].y() >= 0.0)
                {
                    field[faceI] = 3.06;
                }
                else
                {
                    field[faceI] = 300.0;
                }
            }
//}}} end code

    this->parent_bctype::updateCoeffs();
}


// ************************************************************************* //

