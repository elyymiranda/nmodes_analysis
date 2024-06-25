# This script plots a normal mode PES cut based of the normal mode for single point calculation data.
# Script made by Ely Miranda, PhD student at Physics Institute in Universidade de São Paulo
# Last update: 18/04/2024
# Any question or suggestion write me: ely.miranda@usp.br :)

# To run this script use:
"""
python3 plotnm.py data.log
"""

import matplotlib.pyplot as plt
import numpy as np
import sys
import os

# Function to obtain the data from the data file and separate them
def read_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = []
    for line in lines[1:]:
        parts = line.split()
        step = float(parts[0])
        energy1 = float(parts[1])
        energy2 = float(parts[2])
        energy3 = float(parts[3]) 
        data.append([step, energy1, energy2, energy3])

    return np.array(data)

# Function to create the values for harmonic vibrational levels
def harmonic_ener(freq, n, ref_energy):
    # Transform cm**-1 to Hz 
    cm2hz = 29979245800

    # Plank constant value h
    h = 4.1356692E-15	

    # Harmonic energy for level n relative to the reference energy
    energy = ref_energy + freq * h * cm2hz * (n + 0.5)
    return energy 

# Fuction to find the minium n value for vibrational diference between anion and neutral
def dif_value(freq_neutral, freq_anion, gap, n, m):

    energy=-harmonic_ener(freq_neutral,n,0)+harmonic_ener(freq_anion,m,gap)

    return energy

# Function to find the minimum energy from data
def min_energy(data):

    # Extract the energy values from the data
    energy1_values = data[:, 1]
    energy2_values = data[:, 2]

    # Find the minimum energy for neutral and anion
    min_energy_neutral = min(energy1_values)
    min_energy_anion = min(energy2_values)

    return min_energy_neutral, min_energy_anion

# Function to plot the required data with the required title
def plot_data(data, title, freq_neutral, freq_anion):

    # Find the minimum energy for neutral and anion
    min_energy_neutral = min_energy(data)[0]
    min_energy_anion = min_energy(data)[1]

    # Plot the neutral and anion energies
    plt.plot(data[:, 0], data[:, 1], color='blue', marker='o', linestyle='-', label='S$_0$')
    plt.plot(data[:, 0], data[:, 2], color='red', marker='o', linestyle='-', label='$\pi_1^*$')
    plt.plot(data[:, 0], data[:, 3], color='orange', marker='o', linestyle='-', label='$\sigma_{CBr}^*$')

    # Plot harmonic vibrational levels for neutral relative to its minimum energy
    for n in range(0, 10):
        energy_neutral = harmonic_ener(freq_neutral, n, min_energy_neutral)
        plt.axhline(y=energy_neutral, color='blue', linestyle='--')

    # Plot harmonic vibrational levels for anion relative to its minimum energy
    for n in range(0, 10):
        energy_anion = harmonic_ener(freq_anion, n, min_energy_anion)
        plt.axhline(y=energy_anion, color='red', linestyle='--')

    plt.xlabel('Step')
    plt.ylabel('Energy')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

# Main function to call all other functions and input required for plotting
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Current number of aruments is", len(sys.argv), "Usage: python3 plotnm.py data.log freq_neutral freq_anion")
        sys.exit(1)

    file_path = sys.argv[1]
    freq_neutral = float(sys.argv[2])
    freq_anion = float(sys.argv[3])
    data = read_data(file_path)
    title = os.path.splitext(os.path.basename(file_path))[0]

    for n in range(0,10):
        print("Energy diference between m = 0 and n =",n,"is",int(dif_value(freq_neutral, freq_anion, min_energy(data)[1], min_energy(data)[0], n)*1000), "meV")
#        print("Energy for n =", n,"is",int(harmonic_ener(freq_anion,n,min_energy(data)[1])*1000),"meV")
    plot_data(data, title, freq_neutral, freq_anion)

