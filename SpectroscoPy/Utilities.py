# SpectroscoPy/Utilities.py


# ---------
# Docstring
# ---------

""" Utility functions and constants. """


# -------
# Imports
# -------

import numpy as np;

from SpectroscoPy import Constants;


# -------------
# Unit Handling
# -------------

def GetFrequencyUnitLabel(frequencyUnits):
    """ Get a label for units frequencyUnits to be used in plots and output files. """

    # If frequencyUnits is one of the units supported by ConvertFrequencyUnits(), FrequencyUnitLabels will have a label for it.

    key = frequencyUnits.lower();

    if key in Constants.FrequencyUnitLabels:
        return Constants.FrequencyUnitLabels[key];
    else:
        return frequencyUnits;

def ConvertFrequencyUnits(frequencies, unitsFrom, unitsTo):
    """
    Convert frequencies in unitsFrom to unitsTo.
    Supported values of unitsFrom/unitsTo are: 'thz', 'inv_cm', 'mev' and 'um'.
    """

    unitsFrom, unitsTo = unitsFrom.lower(), unitsTo.lower();

    # No point in doing any work if we don't have to...

    if unitsFrom == unitsTo:
        return frequencies;

    # First convert frequencies to THz...

    if unitsFrom != 'thz':
        if unitsFrom == 'inv_cm':
            frequencies = [frequency / Constants.THzToInvCm for frequency in frequencies];
        elif unitsFrom == 'mev':
            frequencies = [frequency / Constants.THzToMeV for frequency in frequencies];
        elif unitsFrom == 'um':
            frequencies = [1.0 / (frequency * Constants.THzToInvUm) for frequency in frequencies];
        else:
            raise Exception("Error: Unsupported units '{0}'.".format(unitsFrom));

    # ... and now convert to the desired unit.

    if unitsTo != 'thz':
        if unitsTo == 'inv_cm':
            frequencies = [frequency * Constants.THzToInvCm for frequency in frequencies];
        elif unitsTo == 'mev':
            frequencies = [frequency * Constants.THzToMeV for frequency in frequencies];
        elif unitsTo == 'um':
            frequencies = [1.0 / (frequency * Constants.THzToInvUm) for frequency in frequencies];
        else:
            raise Exception("Error: Unsupported units '{0}'.".format(unitsTo));

    return frequencies;

# ----------------------
# Peak-Table Preparation
# ----------------------

def GroupForPeakTable(frequencies, intensities, irRepData, linewidths = None):
    """
    Average mode frequencies, intensities and linewidths (if supplied) into groups defined by the (symbol, band_indices) tuples in irRepData.
    Returns a tuple of (new_frequencies, new_intensities, irrep_symbols, new_linewidths) lists, each with the same length as irRepData.
    """

    numModes = len(frequencies);

    if len(intensities) != numModes:
        raise Exception("Error: The lengths of frequencies and intensities are inconsistent.");

    if linewidths is not None and len(linewidths) != numModes:
        raise Exception("Error: If supplied, linewidths must have the same number of elements as frequencies and intensities.");

    # Check band indices.

    includedIndices = set();

    for _, bandIndices in irRepData:
        for index in bandIndices:
            if index in includedIndices:
                raise Exception("Error: Band index {0} assigned to multiple ir. rep. groups.".format(index));

            if index < 1 or index > numModes:
                raise Exception("Error: Band index {0} is out of bounds for # modes = {1}.".format(index, numModes));

            includedIndices.add(index);

    if len(includedIndices) != len(frequencies):
        raise Exception("Error: The number of bands references in the ir. rep. groups is more than # modes = {0}.".format(numModes));

    frequenciesNew, intensitiesNew = [], [];
    linewidthsNew = [] if linewidths != None else None;

    for _, bandIndices in irRepData:
        if len(bandIndices) == 1:
            index = bandIndices[0] - 1;

            frequenciesNew.append(frequencies[index]);
            intensitiesNew.append(intensities[index]);

            if linewidths != None:
                linewidthsNew.append(linewidths[index]);

        else:
            # Average the frequencies.

            frequenciesNew.append(
                np.average([frequencies[index - 1] for index in bandIndices])
                );

            # Sum the intensities.

            intensitiesNew.append(
                np.sum([intensities[index - 1] for index in bandIndices])
                );

            if linewidths != None:
                # Average the linewidths.

                linewidthsNew.append(
                    np.average([linewidths[index - 1] for index in bandIndices])
                    );

    return (frequenciesNew, intensitiesNew, [symbol for symbol, _ in irRepData], linewidthsNew);


# ---------------
# Helper Routines
# ---------------

def CartesianToFractionalCoordinates(positions, latticeVectors):
    """
    Convert positions from cartesian to fractional coordinates.

    Arguments:
        positions -- a list of N three-component vectors in Cartesian coordinates.
        latticeVectors -- must be convertible to a 3x3 NumPy matrix.
    """

    dim1, dim2 = np.shape(latticeVectors);

    if dim1 != 3 or dim2 != 3:
        raise Exception("Error: latticeVectors must be a 3x3 matrix.");

    # The transformation matrix from cartesian to fractional coordinates is the inverse of a matrix built from the lattice vectors.

    transformationMatrix = np.linalg.inv(latticeVectors);

    # If the positions are not three-component vectors, np.dot() raises a readable error message.

    return [
        np.dot(position, transformationMatrix)
            for position in positions
        ];

def FractionalToCartesianCoordinates(positions, latticeVectors):
    """
    Convert positions from fractional to cartesian coordinates.

    Arguments:
        positions -- a list of N three-component vectors in Cartesian coordinates.
        latticeVectors -- must be convertible to a 3x3 NumPy matrix.
    """

    dim1, dim2 = np.shape(latticeVectors);

    if dim1 != 3 or dim2 != 3:
        raise Exception("Error: latticeVectors must be a 3x3 matrix.");

    v1, v2, v3 = latticeVectors[0], latticeVectors[1], latticeVectors[2];

    return [
        np.multiply(f1, v1) + np.multiply(f2, v2) + np.multiply(f3, v3)
            for f1, f2, f3 in positions
        ];

def EigenvectorsToEigendisplacements(eigenvectors, atomicMasses):
    """
    Return the eigenvectors after division of each component by sqrt(mass).

    Arguments:
        eigenvectors -- eigenvectors as 3N x N three-component vectors.
        atomicMasses -- set of N atomic masses.
    """

    numModes, numAtoms, eigDim3 = len(eigenvectors), len(eigenvectors[0]), len(eigenvectors[0][0]);

    if numModes != 3 * numAtoms or eigDim3 != 3:
        raise Exception("Error: eigenvectors should be a 3N x N x 3 matrix.");

    massesDim1 = len(atomicMasses);

    if massesDim1 != numAtoms:
        raise Exception("Error: The number of supplied atomic masses is inconsistent with the number of displacements in the eigenvectors.");

    sqrtMasses = np.sqrt(atomicMasses);

    eigendisplacements = np.zeros(
        (numModes, numAtoms, 3), dtype = np.float64
        );

    for i in range(0, numModes):
        # This should avoid requiring external code to supply eigenvectors as NumPy arrays.

        eigenvector = eigenvectors[i];

        for j in range(0, numAtoms):
            eigendisplacements[i, j, :] = np.divide(eigenvector[j], sqrtMasses[j]);

    return eigendisplacements;
