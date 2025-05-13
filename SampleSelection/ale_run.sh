#!/bin/bash

#SBATCH --job-name=Soap_features
#SBATCH --output=slurm_FT.out
#SBATCH --partition=fat
#SBATCH --nodes=1
#SBATCH --mem=0
#SBATCH --time=10:00:00  # try to set as low as possible
#========================================

conda activate sampleselenv
./PCA.py
