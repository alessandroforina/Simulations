#!/usr/bin/env python3
import numpy as np
import glob
import os

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
