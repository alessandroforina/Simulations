#!/usr/bin/env python3
import ase
from ase import Atoms
from ase.io import read, write
import os
import re
from tqdm import tqdm
from typing import List, Union

def load_indices(path:str) -> List[int]:
    """
    Load indices from a file.
    
    Args:
        path (str): Path to the file containing indices.
        
    Returns:
        List[int]: List of indices.
    """
    if not isinstance(path, str):
        raise TypeError("Expected path to be a str, got {type(path).__name__!r}")
    
    indices: List[int] = []
    with open(path, 'r') as f:
        for line_number, line in enumerate(f, start =1):
            s = line.strip()
            if not s:
                continue
            try:
                index = int(s)
            except ValueError:
                raise ValueError(f"Line {line_number!r} in {path!r} is not a valid integer: {s!r}")
            else:
                indices.append(index)
    return indices

def read_configurations(path_of_configurations_file: str, indices: List[int]) -> List[Atoms]:
    """
    Read configurations from a file.
    
    Args:
        path (str): Path to the file containing configurations.
        indices (List[int]): List of indices to read.
        
    Returns:
        List[Atoms]: List of ASE Atoms objects.
    """

    # Checks that all the arguments are of the correct type and valid for the purpose
    # if not isinstance(path_of_configurations_file, str):
    #     raise TypeError(f"Expected path to be a str, got {type(path).__name__!r}")
    
    # if not all(isinstance(i,int) for i in indices):
    #     raise TypeError(f"Expected indices to be a list of int, got {type(indices).__name__!r}")
    
    # if not os.path.exists(path_of_configurations_file):
    #     raise FileNotFoundError(f"File {path_of_configurations_file!r} does not exist.")
    
    # if not os.path.isfile(path_of_configurations_file):
    #     raise IsADirectoryError(f"{path_of_configurations_file!r} is a directory, not a file.")
    
        
    # 1) Read all structures in one go (loads everything into memory)
    all_structures: List[Atoms] = read(
        path_of_configurations_file,
        index=":",           # ":" means “all frames”
        #format="extxyz"      # or whatever format your file is
    )

    # 2) Pick out just the ones you asked for
    #    This is now just a quick list-lookup, zero file I/O
    selected = []
    for i in tqdm(indices, desc="Selecting frames", unit="frame"):
        selected.append(all_structures[i])

    return selected




if __name__ == "__main__":
    # Define the paths to the index and configuration files
    path_of_index_file = "/home/forina/Documents/MIT/MIT_Dataset/PCA/selected_structures_FPS_nstruct_7000.txt"
    path_of_configurations_file = "/home/forina/Documents/MIT/MIT_Dataset/PCA/dataset_silica_water_NNIP.xyz"
    path_of_output_file = "Selected_Configurations/dataset_silica_water_NNIP_selected_structures.xyz"
    
    if not os.path.exists("Selected_Configurations"):
        os.makedirs("Selected_Configurations")
        print("Directory 'Selected_Configurations' created.")

    # Load the indices from the file
    indices = load_indices(path_of_index_file)
    print(f"Loaded {len(indices)} indices from {path_of_index_file!r}.")
    
    
    # Read the configurations from the file
    configurations = read_configurations(path_of_configurations_file, indices)
    print(f"Read {len(configurations)} configurations from {path_of_configurations_file!r}.")
    
    # Write the configurations to the output file
    # open once for writing all frames
    write(path_of_output_file, configurations, format="extxyz")    

