#!/usr/bin/env python3
import numpy as np
import glob
import os
import ase.io
import chemiscope
import metatensor
import numpy as np
from featomic import SoapPowerSpectrum
from matplotlib import pyplot as plt
import os
from sklearn.decomposition import PCA
from skmatter import feature_selection, sample_selection

# 1. Find all .npy files in NPY/ matching your naming pattern
file_list = sorted(glob.glob(os.path.join("NPY", "feat_*.npy")))

# 2. Load and collect them
all_features = []
for fname in file_list:
    data = np.load(fname)
    all_features.append(data)
    print(f"Loaded {fname}, shape = {data.shape}")

# 3. Concatenate along the first axis
all_features = np.concatenate(all_features, axis=0)
print(f"Concatenated array shape = {all_features.shape}")

# 4. Save the result
out_fname = "all_features.npy"
np.save(out_fname, all_features)
print(f"Saved merged features to {out_fname}")

# 5. Index Sample Selection
mode = "FPS"
n_structures = 5

# Setting output files
output_log = f"Logs/log_{mode}_nstruct_{n_structures}.txt"
output_file = f"Selected/selected_structures_{mode}_nstruct_{n_structures}.txt"

# Check if the output folders exist, if not create them
for folder in ["Logs", "Selected"]:
    if os.path.isdir(folder):
        print(f"✅ Folder '{folder}' exists.")
    else:
        print(f"❌ Folder '{folder}' does not exist.")
        os.makedirs(folder)
        print(f"🛠 Created folder '{folder}'.")

# FPS structure selection
sample_fps = sample_selection.FPS(n_to_select=n_structures, initialize="random").fit(
    all_features
)
struct_fps_idxs = sample_fps.selected_idx_
print("structures selected with FPS:\n", sample_fps.selected_idx_)

with open(output_log, "w") as f:
    f.write("The operations was succesfully completed!\n")

with open(output_file, "w") as f:
    for idx in sample_fps.selected_idx_:
        f.write(f"{idx}\n")
