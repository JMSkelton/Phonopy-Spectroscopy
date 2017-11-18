# Phonopy-Spectroscopy

Phonopy-Spectroscopy is a project to add the capability to simulate vibrational spectra to the Phonopy code.[[1](#Ref1)]

The software package consists of a Python module, `SpectroscoPy`, along with a set of command-line scripts for working with output from Phonopy and VASP.


## Features

* Calculate infrared (IR) intensities from Phonopy or VASP calculations.

* Prepare peak tables including assigning modes to irreducible representations (Phonopy interface).

* Output customisable simulated spectra with support for multiple unit systems and simulated instrumental broadening.

* Include first-principles mode linewidths from Phono3py[[2](#Ref2)] calculations (Phonopy interface).

* A workflow for simulating Raman spectra within the far from resonance approximation is planned for the near future.


## Installation

The code depends on the `NumPy` package,[[3](#Ref3)] and the Phonopy interface requires the `Phonopy` Python library.[[1](#Ref1)]
Please see the documentation of these codes for instructions on how to install them on your system.

After cloning or downloading and unpacking the repository, add it to your `PYTHONPATH` so that the command-line scripts can locate `SpectroscoPy`, e.g.:

`export PYTHONPATH=${PYTHONPATH}:/Volumes/Data/Repositories/Phonopy-Spectroscopy`

The command-line scripts are in the [Scripts](./Scripts) directory.
For convenience, you may wish to add this folder to your `PATH` variable, e.g.:

`export PATH=${PATH}:/Volumes/Data/Repositories/Phonopy-Spectroscopy/Scripts`

For a description of the command-line arguments the scripts accept, call them with the `-h` option, e.g.:

`phonopy-ir -h`


## Examples

1. [Benzene derivatives](./Examples/Benzene-Derivatives): Simulated IR spectra of isolated molecules using the Phonopy interface, compared to reference gas-phase spectra from the NIST database


## References

1. <a name="Ref1"></a>[https://atztogo.github.io/phonopy/](https://atztogo.github.io/phonopy/)
2. <a name="Ref2"></a>[https://atztogo.github.io/phono3py/](https://atztogo.github.io/phono3py/)
3. <a name="Ref3"></a>[http://www.numpy.org/](http://www.numpy.org/)
