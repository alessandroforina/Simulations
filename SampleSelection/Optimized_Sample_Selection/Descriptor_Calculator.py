#!/usr/bin/env python3

import ase.io
import chemiscope
import metatensor
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



#start = 0
#batch_size = 100


with open("feat.npy", "wb") as f:
        
    # Read the frames from the dataset

    frames = ase.io.read("dataset_silica_water_NNIP.xyz",
                index=":", format="extxyz")
        
        
    # Generate a SOAP power spectrum
    calculator = SoapPowerSpectrum(**hypers)
    rho2i = calculator.compute(frames)

    # Makes a dense block
    atom_soap = rho2i.keys_to_properties(["neighbor_1_type", "neighbor_2_type"])

    atom_soap_single_block = atom_soap.keys_to_samples(keys_to_move=["center_type"])

    # Sum over atomic centers to compute structure features
    struct_soap = metatensor.sum_over_samples(
        atom_soap_single_block, sample_names=["atom", "center_type"]
    )


    """print("atom feature descriptor shape:", atom_soap.block(0).values.shape)
    print(
        "atom feature descriptor (all in one block) shape:",
        atom_soap_single_block.block(0).values.shape,
    )
    print("structure feature descriptor shape:", struct_soap.block(0).values.shape)"""

    feat = struct_soap.block(0).values

    np.save(f,feat)
        
        #print(f"Batch {start//batch_size + 1}: processed {len(frames)} frame, "
            #f"saved in total {start + len(frames)} feature")


        #start += batch_size
print("It worked nicely!")
with open("log.txt", "a") as log:
    log.write("Work done! Check the feat.npy file for the features.\n")














