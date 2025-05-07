#!/usr/bin/env python3

from ase.io import read, write

def main():
    input_file = "dump_NPT.lammpstrj"
    output_file = "../restart_file_NPT_1.data"

    print(f"Reading last frame from {input_file}...")
    atoms = read(input_file, format="lammps-dump-text", index=-1)

    print(f"Writing restart file to {output_file}...")
    write(output_file, atoms, format="lammps-data", atom_style="atomic")

    print("✅ Done.")

if __name__ == "__main__":
    main()
