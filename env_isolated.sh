#!/bin/bash
# =====================================================================
#  sedInterFoam (ISOLATED build) environment loader
#
#  Loads PATH + LD_LIBRARY_PATH so that 'sedInterFoam' resolves to the
#  module-prefixed build in ~/OpenFOAM/sedInterFoam-2412 and links its
#  OWN renamed library (libtwoPhaseModelInter.so) -- NOT sedFoam's
#  libtwoPhaseModel.so. This prevents the ABI clash that used to occur
#  when both solvers shared FOAM_USER_LIBBIN.
#
#  Usage (after sourcing OpenFOAM env):
#      source /mnt/f/DKS/DKS/sedInterFoam/env_isolated.sh
#      which sedInterFoam        # -> ~/OpenFOAM/sedInterFoam-2412/bin/sedInterFoam
#      ldd $(which sedInterFoam) | grep libtwoPhaseModel   # -> .../libtwoPhaseModelInter.so
#      mpirun -np 8 sedInterFoam -parallel > log.sedInterFoam 2>&1
# =====================================================================
export FOAM_MODULE_PREFIX="$HOME/OpenFOAM/sedInterFoam-2412"
export FOAM_MODULE_APPBIN="$FOAM_MODULE_PREFIX/bin"
export FOAM_MODULE_LIBBIN="$FOAM_MODULE_PREFIX/lib"
export LD_LIBRARY_PATH="$FOAM_MODULE_LIBBIN:$LD_LIBRARY_PATH"
export PATH="$FOAM_MODULE_APPBIN:$PATH"
echo "sedInterFoam -> $FOAM_MODULE_APPBIN/sedInterFoam"
echo "  (isolated libs in $FOAM_MODULE_LIBBIN ; libtwoPhaseModelInter.so)"
