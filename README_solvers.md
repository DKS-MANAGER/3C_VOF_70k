# Solver Compatibility Guide: sedFoam vs. sedInterFoam
This guide explains how to compile, isolate, and run both **`sedFoam`** (two-phase) and **`sedInterFoam`** (three-phase) solvers on the same machine without library collisions.

---

## 1. The Collision Problem

Both solvers compile a core phase model library with the exact same name:

```
libtwoPhaseModel.so
```

By default, OpenFOAM's compilation environment (`Allwmake` or `wmake`) installs user-compiled libraries into the global user directory:

```
$WM_PROJECT_USER_DIR/platforms/linux64GccDPInt32Opt/lib   (FOAM_USER_LIBBIN)
```

### The Conflict:
Because `sedFoam` (2-phase) and `sedInterFoam` (3-phase VOF) have **different internal C++ structures** in `phaseModel.H` (sedFoam includes additional fields like `aE_`, `bE_`, `sF_`), if one solver is built globally, it overwrites `libtwoPhaseModel.so` for the other.

When the secondary solver runs, it loads the conflicting shared library with the wrong memory layout, causing **segmentation faults, uninitialized dimension sets, or floating-point exceptions** (`Different dimensions for '(a - b)'`).

---

## 2. The Solution: Isolated Prefix Builds

To keep both solvers operational on the same PC, `sedInterFoam` is built in an isolated directory using the module prefix mechanism.

### Step 1: Compiling sedInterFoam in Isolation
Execute the build script in `sedInterFoam` using a dedicated prefix folder:

```bash
source /usr/lib/openfoam/openfoam2412/etc/bashrc

# Sourcing waves2Foam paths is required for sedInterFoam linking
source /mnt/f/DKS/DKS/sedInterFoam/waves2Foam/bin/bashrc

cd /mnt/f/DKS/DKS/sedInterFoam
./Allwmake -prefix=$HOME/OpenFOAM/sedInterFoam-2412 -j > log.build 2>&1
```

This isolates the compilation:
* Binary location: `~/OpenFOAM/sedInterFoam-2412/bin/sedInterFoam`
* Libraries location: `~/OpenFOAM/sedInterFoam-2412/lib/libtwoPhaseModel.so`

---

## 3. Running the Solvers

Because OpenFOAM does not embed hardcoded library search paths (RPATH) in user binaries, you must set the environment variables correctly before executing each solver.

### 🌊 Running sedFoam (e.g. Exp_3AC cases)
`sedFoam_rbgh` links against the global user directory. Running it requires standard sourcing:

```bash
# 1. Source OpenFOAM 2412 environment
source /usr/lib/openfoam/openfoam2412/etc/bashrc

# 2. Run case (runs standard two-phase solver)
cd /mnt/f/DKS/DKS/Exp_3AC/3C
mpirun -np 8 sedFoam_rbgh -parallel > log.sedFoam 2>&1
```

---

### 🌊 Running sedInterFoam (e.g. Dam_break case)
To run the 3-phase solver, you **must prepend** its isolated library folder to `LD_LIBRARY_PATH` and the binary folder to `PATH`:

```bash
# 1. Source OpenFOAM 2412 environment
source /usr/lib/openfoam/openfoam2412/etc/bashrc

# 2. Inject isolated sedInterFoam paths
export FOAM_MODULE_LIBBIN=$HOME/OpenFOAM/sedInterFoam-2412/lib
export FOAM_MODULE_APPBIN=$HOME/OpenFOAM/sedInterFoam-2412/bin
export LD_LIBRARY_PATH=$FOAM_MODULE_LIBBIN:$LD_LIBRARY_PATH
export PATH=$FOAM_MODULE_APPBIN:$PATH

# 3. Sanity check: Ensure it resolves the correct path
ldd $(which sedInterFoam) | grep libtwoPhaseModel
# Must output: .../sedInterFoam-2412/lib/libtwoPhaseModel.so

# 4. Run parallel simulation
cd /mnt/f/DKS/DKS/Dam_break
mpirun -np 6 sedInterFoam -parallel > log.sedInterFoam 2>&1
```

---

## 4. Hard Rules (What NOT to Do)

1. **Do NOT run plain `./Allwmake` or `wmake` inside the `sedInterFoam` directory.** This will overwrite the shared `libtwoPhaseModel.so` inside your global user directory and break your standard `sedFoam` runs.
2. **Do NOT set the `sedInterFoam` variables globally inside your `~/.bashrc`.** Keep the environment exports local to the execution scripts or terminals to avoid cross-contamination.
3. **Do NOT forget the `LD_LIBRARY_PATH` redirection.** If you launch `sedInterFoam` without modifying the path, it will silently load `sedFoam`'s version of `libtwoPhaseModel.so` and crash immediately.
