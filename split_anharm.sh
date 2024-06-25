#!/bin/bash

# This script gets the information data from anharmonic frequency calculation.
# Script made by Ely Miranda, PhD student at Physics Institute in Universidade de São Paulo
# Last update: 04/06/2024
# Any question or suggestion write me: ely.miranda@usp.br :)

# To run this script use:
# ./split_anharm freq.log 

# Check if file name is provided
if [ $# -eq 0 ]; then
    echo "No arguments supplied. Please provide the log file name."
    exit 1
fi

# File name
file=$1

# Flags to check sections
in_section=false
in_fundamental_bands=false
in_overtones=false

# Temporary arrays to store energies
declare -a modes
declare -a fundamental_energies
declare -a overtone_energies

# Read file line by line
while IFS= read -r line; do
    # Check if we are in the "Vibrational Energies at Anharmonic Level" section
    if [[ $line == *"Vibrational Energies at Anharmonic Level"* ]]; then
        in_section=true
    fi

    # Check if we are in the "Fundamental Bands" section
    if $in_section && [[ $line == *"Fundamental Bands"* ]]; then
        in_fundamental_bands=true
        in_overtones=false
        continue
    fi

    # Check if we are in the "Overtones" section
    if $in_section && [[ $line == *"Overtones"* ]]; then
        in_fundamental_bands=false
        in_overtones=true
        continue
    fi

    # Stop processing if we reach the "Combination Bands" section
    if [[ $line == *"Combination Bands"* ]]; then
        break
    fi
    
    # If we are in the "Fundamental Bands" section, extract energies
    if $in_fundamental_bands && [[ $line =~ [0-9]+\([0-9]+\) ]]; then
        mode=$(echo $line | sed 's/^H//g' | sed 's/^L//g' | awk '{print $1}' | sed 's/...$//')
        energy=$(echo $line | sed 's/^H//g' | sed 's/^L//g' | awk '{print $4}')
#        echo $line | sed 's/^H//g' | sed 's/^L//g' | awk '{print $4}'
	modes+=("$mode")
        fundamental_energies+=("$mode $energy")
    fi

    # If we are in the "Overtones" section, extract energies
    if $in_overtones && [[ $line =~ [0-9]+\([0-9]+\) ]]; then
        mode=$(echo $line | sed 's/^H//g' | sed 's/^L//g' | awk '{print $1}' | sed 's/...$//')
        energy=$(echo $line | sed 's/^H//g' | sed 's/^L//g' | awk '{print $3}')
#	echo $line | sed 's/^H//g' | sed 's/^L//g' | awk '{print $2}'
#	modes+=("$mode")
        overtone_energies+=("$mode $energy")
    fi
done < "$file"

# Remove duplicates and sort modes
#modes=($(printf "%s\n" "${modes[@]}" | sort -u))

# Print the organized output
for mode in "${modes[@]}"; do
    fundamental_band=-1
    overtone_band=-1
    for entry in "${fundamental_energies[@]}"; do
        if [[ $entry == $mode* ]]; then
            fundamental_band=$(echo $entry | awk '{print $2}')
            break
        fi
    done
    for entry in "${overtone_energies[@]}"; do
        if [[ $entry == $mode* ]]; then
            overtone_band=$(echo $entry | awk '{print $2}')
            break
        fi
    done
    echo "Mode $((${#modes[@]}-mode+1)) 
Fundamental band: $fundamental_band 
First Overtone: $overtone_band
    "
done

