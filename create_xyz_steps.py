#!/usr/bin/env python3

# This script creates geometries based of the normal mode for single point calculatio
# Script made by Ely Miranda, PhD student at Physics Institute in Universidade de São Paulo
# Last update: 22/04/2024
# Any question or suggestion write me: ely.miranda@usp.br :)

# To run this script use:
"""
./create_xyz_steps.py original_geometry.xyz frequency_normal_coordinates.log factor_to_multiply_coordinates number_steps

"""

import numpy as np
import sys
import os

def read_xyz(filename):
    """Reads atomic positions from an XYZ file."""
    with open(filename, 'r') as file:
        lines = file.readlines()[2:]  # Skip the first two lines
    positions = []
    for line in lines:
        atom_data = line.split()
        positions.append([float(atom_data[1]), float(atom_data[2]), float(atom_data[3])])
    return np.array(positions)

def read_displacement(filename):
    """Reads the displacement vector from a file."""
    with open(filename, 'r') as file:
        lines = file.readlines()[4:]  # Skip the first six lines
    displacement = []
    for line in lines:
        atom_data = line.split()
        displacement.append([float(atom_data[1]), float(atom_data[2]), float(atom_data[3])])
    return np.array(displacement)

def atoms_xyz(filename):
    """Reads atomic letter from an XYZ file."""
    with open(filename, 'r') as file:
        lines = file.readlines()[2:]  # Skip the first two lines
    atoms = []
    for line in lines:
        atom_data = line.split()
        atoms.append(atom_data[0])
    return(atoms)

def insert_array_into_file(file_path, array):
    # Read the content of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Insert the array elements into the appropriate positions after the second line
    for i, element in enumerate(array):
        lines[i+2] = str(element) + ' ' + lines[i+2]

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)

def write_xyz(filename, positions):
    """Writes atomic positions to an XYZ file."""
    with open(filename, 'w') as file:
        file.write(f'{len(positions)}\n')
        file.write('Updated Geometry\n')
        for atom in positions:
            file.write(f'{atom[0]:.6f} {atom[1]:.6f} {atom[2]:.6f}\n')  # Assuming carbon atoms for illustration

def create_directory(directory):
    """Creates a directory if it does not exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 create_xyz_steps.py original_geometry.xyz frequency_normal_coordinates.log factor_to_multiply_coordinates number_steps")
        sys.exit(1)

    geo_file = sys.argv[1]
    displacement_file = sys.argv[2]
    num_steps = int(sys.argv[4])
    factor = float(sys.argv[3])

    # Create the output directory if it does not exist
    create_directory('geom')

    # Read initial geometry and displacement vector
    initial_geometry = read_xyz(geo_file)
    displacement = read_displacement(displacement_file)
    displacement = np.array(displacement)
   
    # Get the new displacement
    factor_displacements = factor * displacement

    # Get the atoms from the original .xyz file
    atoms = atoms_xyz(geo_file)
    
    # Write original geometry
    output_filename = f"{'geom'}/step_0.xyz"
    write_xyz(output_filename, initial_geometry)
    insert_array_into_file(f"{'geom'}/step_0.xyz",atoms)
    
    # Create and write updated geometries for each step
    for i in range(1,num_steps+1):
        updated_geometry = initial_geometry + factor_displacements * i
        output_filename = f"{'geom'}/step_{i}.xyz"
        write_xyz(output_filename, updated_geometry)
        insert_array_into_file(f"{'geom'}/step_{i}.xyz",atoms)
        
        updated_geometry2 = initial_geometry - factor_displacements * i
        output_filename2 = f"{'geom'}/step_{-i}.xyz"
        write_xyz(output_filename2, updated_geometry2)
        insert_array_into_file(f"{'geom'}/step_{-i}.xyz",atoms)
