#!/usr/bin/env python3

# This script gets the sp data from both neutral and anion single point calculation.
# Script made by Ely Miranda, PhD student at Physics Institute in Universidade de São Paulo
# Last update: 31/05/2024
# Any question or suggestion write me: ely.miranda@usp.br :)

# To run this script use:
# ./vibronic_excitation.py harmonic.log neutral.log anion.log (for harmonic)
# ./vibronic_excitation.py none neutral.log anion.log freq_neutro.log freq_anion.log (for anharmonic)
# ./vibronic_excitation.py harmonic.log neutral.log anion.log freq_neutro.log freq_anion.log (for both)

import re
import sys

def read_frequencies(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    neutral_frequencies = []
    anion_frequencies = []
    negative_frequencies = []

    for i in range(len(lines)):
        if "Neutral's" in lines[i] and "normal mode" in lines[i]:
            neutral_freq_line = lines[i + 3].strip()
            anion_freq_line = lines[i + 4].strip()

            neutral_freq_match = re.search(r'Neutral:\s+([\d.-]+)', neutral_freq_line)
            anion_freq_match = re.search(r'Anion:\s+([\d.-]+)', anion_freq_line)

            if neutral_freq_match and anion_freq_match:
                neutral_freq = float(neutral_freq_match.group(1))
                anion_freq = float(anion_freq_match.group(1))

                if neutral_freq < 0 or anion_freq < 0:
                    negative_frequencies.append((neutral_freq, anion_freq))
                    neutral_frequencies.append(None)
                    anion_frequencies.append(None)
                else:
                    neutral_frequencies.append(neutral_freq)
                    anion_frequencies.append(anion_freq)
            else:
                print(f"Error parsing frequencies at line {i}:")
                print(f"Neutral line: {neutral_freq_line}")
                print(f"Anion line: {anion_freq_line}")

    return neutral_frequencies, anion_frequencies, negative_frequencies

def harmonic_ener(freq, n, ref_energy=0):
    energy = ref_energy + freq * (n + 0.5)
    return energy

def read_scf_energy(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if "SCF Done:" in line:
            energy_match = re.search(r'SCF Done:\s+E\(\w+\)\s+=\s+([-0-9.]+)', line)
            if energy_match:
                return float(energy_match.group(1))
    raise ValueError(f"SCF energy not found in file: {file_path}")

def read_anharmonic_frequencies(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    frequencies = []
    constants = []

    for i in range(0, len(lines), 4):
        if i + 2 >= len(lines):
            break

        fundamental_line = lines[i + 1].strip()
        overtone_line = lines[i + 2].strip()
#        print(lines[i])
#        print(fundamental_line)
#        print(overtone_line)

        try:
            fundamental_freq = float(fundamental_line.split(":")[1].strip())
            overtone_freq = float(overtone_line.split(":")[1].strip())
#            print(lines[i])
#            print(fundamental_freq)
#            print(overtone_freq)
        except (IndexError, ValueError):
            print(f"Skipping malformed line at index {i}: {lines[i:i+3]}")
            frequencies.append(None)
            constants.append(None)
            continue

        if fundamental_freq < 0 or overtone_freq < 0:
            frequencies.append(None)
            constants.append(None)
        else:
            freq = 3 * fundamental_freq - overtone_freq
            x_e = (2 * fundamental_freq - overtone_freq) / (2 * freq)
#            print(freq)
#            print(x_e)
            frequencies.append(freq)
            constants.append(x_e)

    return frequencies, constants

def anharmonic_ener(freq, x_e, n, ref_energy=0):
    energy = ref_energy + freq * (n + 0.5) - x_e * freq * (n + 0.5)**2
    return energy

def vibronic_excitation_energy(neutral_frequencies, anion_frequencies, vertical_electron_energy):
    cm2meV = 0.123981
    excitation_energies = []
    for neutral_freq, anion_freq in zip(neutral_frequencies, anion_frequencies):
        if neutral_freq is None or anion_freq is None:
            excitation_energies.append(None)
            continue
        zpe_neutral = harmonic_ener(neutral_freq, 0)
        vibronic_energies = []
        for n in range(0, 11):
            excitation_energy = harmonic_ener(anion_freq, n) - zpe_neutral
            vibronic_energies.append(excitation_energy * cm2meV + vertical_electron_energy*1000)
        excitation_energies.append(vibronic_energies)
    return excitation_energies

def anharmonic_excitation_energy(neutral_frequencies, anion_frequencies, neutral_constants, anion_constants, vertical_electron_energy):
    cm2meV = 0.123981
    excitation_energies = []
    for neutral_freq, anion_freq, neutral_const, anion_const in zip(neutral_frequencies, anion_frequencies, neutral_constants, anion_constants):
        if neutral_freq is None or anion_freq is None or neutral_const is None or anion_const is None:
            excitation_energies.append(None)
            continue
        zpe_neutral = anharmonic_ener(neutral_freq, neutral_const, 0)
        vibronic_energies = []
        for n in range(0, 11):
            excitation_energy = anharmonic_ener(anion_freq, anion_const, n) - zpe_neutral
            vibronic_energies.append(excitation_energy * cm2meV + 1000*vertical_electron_energy)
        excitation_energies.append(vibronic_energies)
    return excitation_energies

def main(freq_file_path=None, neutral_log_file_path=None, anion_log_file_path=None, neutral_anharmonic_file=None, anion_anharmonic_file=None):
    if freq_file_path:
        neutral_frequencies, anion_frequencies, negative_frequencies = read_frequencies(freq_file_path)
    else:
        neutral_frequencies, anion_frequencies, negative_frequencies = ([], [], [])

    if neutral_log_file_path and anion_log_file_path:
        neutral_energy = read_scf_energy(neutral_log_file_path)
        anion_energy = read_scf_energy(anion_log_file_path)
        vertical_electron_energy = -(neutral_energy - anion_energy) * 27.2114  # Convert from atomic units to eV
        vertical_electron_energy_meV = vertical_electron_energy * 1000  # Convert from eV to meV

        print(f"Neutral single point energy: {neutral_energy:.8f} a.u.")
        print(f"Anion single point energy: {anion_energy:.8f} a.u.")
        print(f"Vertical electron energy difference: {vertical_electron_energy_meV:.2f} meV")
    else:
        vertical_electron_energy_meV = 0
        vertical_electron_energy = 0

    if negative_frequencies:
        print("Negative frequencies found in the following modes:")
        for nf, af in negative_frequencies:
            print(f"Neutral: {nf} cm^-1, Anion: {af} cm^-1")

    if freq_file_path:
        print("Harmonic analisys: \n")
        excitation_energies = vibronic_excitation_energy(neutral_frequencies, anion_frequencies, vertical_electron_energy)
        for mode, (neutral_freq, anion_freq, energies) in enumerate(zip(neutral_frequencies, anion_frequencies, excitation_energies), 1):
            if energies is None:
                print(f"Normal mode {mode} (Neutral: {neutral_freq} cm^-1, Anion: {anion_freq} cm^-1): Skipping due to negative frequency.")
            else:
                print(f"Normal mode {mode} (Neutral: {neutral_freq} cm^-1, Anion: {anion_freq} cm^-1):")
                print(f"  ZPE to ZPE: {energies[0]:.2f} meV")
                for n, energy in enumerate(energies[1:], 1):
                    print(f"  Excitation to level {n}: {energy:.2f} meV")
        print("\nEnd of harmonic analisys \n")

    if neutral_anharmonic_file and anion_anharmonic_file:
        print("Anhamornic analisys: \n")
        neutral_anharm_freqs, neutral_anharm_consts = read_anharmonic_frequencies(neutral_anharmonic_file)
        anion_anharm_freqs, anion_anharm_consts = read_anharmonic_frequencies(anion_anharmonic_file)
        anharmonic_energies = anharmonic_excitation_energy(neutral_anharm_freqs, anion_anharm_freqs, neutral_anharm_consts, anion_anharm_consts, vertical_electron_energy)
        for mode, (neutral_freq, neutral_xe, anion_freq, anion_xe, energies) in enumerate(zip(neutral_anharm_freqs,neutral_anharm_consts, anion_anharm_freqs, anion_anharm_consts,anharmonic_energies), 1):
            rmode = len(neutral_anharm_consts) - mode + 1
            if energies is None:
                print(f"Normal mode {rmode}: Skipping due to negative frequency.")
            else:
                print(f"Normal mode {rmode} (Neutral: {neutral_freq:.0f} cm^-1; x_e = {neutral_xe:.3f} and Anion: {anion_freq:.0f} cm^-1; x_e = {anion_xe:.3f})")
                print(f"  ZPE to ZPE: {energies[0]:.2f} meV")
                for n, energy in enumerate(energies[1:], 1):
                    print(f"  Excitation to level {n}: {energy:.2f} meV")
        print("\nEnd of anharmonic analisys")

if __name__ == "__main__":
    if len(sys.argv) not in [4, 6]:
        print("Usage: python3 vibronic_excitation.py frequencies.log neutral.log anion.log [neutral_anharmonic.log anion_anharmonic.log]")
        sys.exit(1)

    freq_file_path = sys.argv[1] if sys.argv[1] != 'none' else None
    neutral_log_file_path = sys.argv[2]
    anion_log_file_path = sys.argv[3]
    neutral_anharmonic_file = sys.argv[4] if len(sys.argv) == 6 else None
    anion_anharmonic_file = sys.argv[5] if len(sys.argv) == 6 else None
    main(freq_file_path, neutral_log_file_path, anion_log_file_path, neutral_anharmonic_file, anion_anharmonic_file)

