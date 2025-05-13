#!/usr/bin/env python3

import ase.io
import chemiscope
import metatensor
from metatensor import Labels
import numpy as np
import os
from featomic import SoapPowerSpectrum
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from skmatter import feature_selection, sample_selection

# Define the list of hyper parameters

hypers = {
    "cutoff": {"radius": 6.0, "smoothing": {"type": "ShiftedCosine", "width": 0.5}},
    "density": {
        "type": "Gaussian",
        "width": 0.3,
        "scaling": {"type": "Willatt2018", "exponent": 4, "rate": 1, "scale": 3.5},
    },
    "basis": {
        "type": "TensorProduct",
        "max_angular": 6,
        "radial": {"type": "Gto", "max_radial": 7},
    },
}

global_atom_types = [1, 8, 11, 14]



start = 0
batch_size = 100
batch_idx = 1
all_features = []



while True:
    
    # Read the frames from the dataset

    frames = ase.io.read("dataset_silica_water_NNIP.xyz",
                        index=slice(start, start + batch_size),
                        format="extxyz")
    if not frames:   # esci se la lista è vuota
        break
    
    
    # Generate a SOAP power spectrum
    calculator = SoapPowerSpectrum(**hypers)
    rho2i = calculator.compute(frames)

    # Makes a dense block
    atom_soap = rho2i.keys_to_properties(
        Labels(
            ["neighbor_1_type", "neighbor_2_type"],
            np.array(
                [
                    [i, j]
                    for i in global_atom_types 
                    for j in global_atom_types
                ]
            )
        )
    )

    atom_soap_single_block = atom_soap.keys_to_samples(keys_to_move=["center_type"])

    # Sum over atomic centers to compute structure features
    struct_soap = metatensor.sum_over_samples(
        atom_soap_single_block, sample_names=["atom", "center_type"]
    )

    # Save the features in a numpy array
    feat = struct_soap.block(0).values

    filename=f"NPY/feat_{batch_idx:03d}.npy"
    np.save(filename, feat)

     # Updating the progress  
    print(f"Batch {start//batch_size + 1}: processed {len(frames)} frame, "
        f"saved in total {start + len(frames)} feature")


    start += batch_size
    batch_idx += 1
# Concatenate all features into a single numpy array
all_features = np.concatenate(all_features, axis=0)
# Save the features to a file
np.save("feat_3.npy", all_features)

print("Work done! Check the feat.npy file for the features.")















