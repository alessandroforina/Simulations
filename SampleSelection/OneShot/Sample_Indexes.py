#!/usr/bin/env python3
import ase.io
import chemiscope
import metatensor
import numpy as np
from featomic import SoapPowerSpectrum
from matplotlib import pyplot as plt
import os
from sklearn.decomposition import PCA
from skmatter import feature_selection, sample_selection

# Setting Parameters
file_path = "feat.npy"
mode = "FPS"
n_structures = 50000

# Setting output files
output_log = f"Logs/log_{mode}_nstruct_{n_structures}.txt"
output_file = f"Selected/selected_structures_{mode}_nstruct_{n_structures}.txt"


# Check if the file exists
if os.path.exists(file_path):
    # Load the data
    feats = np.load(file_path)
else:
    ValueError(f"File {file_path} does not exist.")


# FPS structure selection
sample_fps = sample_selection.FPS(n_to_select=n_structures, initialize="random").fit(
    feats
)
struct_fps_idxs = sample_fps.selected_idx_
print("structures selected with FPS:\n", sample_fps.selected_idx_)

with open(output_log, "w") as f:
    f.write("The operations was succesfully completed!\n")

with open(output_file, "w") as f:
    for idx in sample_fps.selected_idx_:
        f.write(f"{idx}\n")
