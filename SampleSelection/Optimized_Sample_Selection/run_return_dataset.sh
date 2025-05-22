#!/bin/bash

#SBATCH --job-name=RD
#SBATCH --output=slurm.out
#SBATCH --partition=jobs
#SBATCH --nodes=1
#SBATCH --mem=0
#SBATCH --time=20:00:00  # try to set as low as possible
#SBATCH --get-user-env
#========================================

#conda activate /home/forina/miniforge3/envs/sampleselenv
./Return_Dataset.py
