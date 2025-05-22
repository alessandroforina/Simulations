#!/bin/bash

#SBATCH --job-name=Soap_features
#SBATCH --output=slurm_FT.out
#SBATCH --partition=jobs
#SBATCH --nodes=1
#SBATCH --mem=0
#SBATCH --time=20:00:00  # try to set as low as possible
#SBATCH --get-user-env
#========================================

#conda activate /home/forina/miniforge3/envs/sampleselenv
./Sample_Indexes.py
