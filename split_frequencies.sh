#!/bin/bash

# This script split all the normal modes information from a .log gaussian file into separated files
# Script made by Ely Miranda, PhD student at Physics Institute in Universidade de São Paulo
# Last update: 12/04/2024
# Any question or suggestion write me: ely.miranda@usp.br :)

# For running just type
# $./split_frequencies freq.log

if [ $# -eq 0 ]; then  # If no argument (input) is given, end the script.
    echo "No input provided"
    exit 1
fi

# Get the number of atoms from the .log file
NATOMS=$(grep -m1 "NAtoms=" $1 | awk '{print $2}')

# Calculate the number of normal modes
NNORMAL=$((3 * $NATOMS - 6))

# Obtain the main information for each mode
FREQ=($(grep "Frequencies --" "$1" | awk '{print $3, $4, $5}'))
RMASS=($(grep "Red. masses --" "$1" | awk '{print $4, $5, $6}'))
FORCE=($(grep "Frc consts  --" "$1" | awk '{print $4, $5, $6}'))
IR=($(grep "IR Inten    --" "$1" | awk '{print $4, $5, $6}'))

# Extracting normal coordinates
awk "/Atom  AN/{flag=1; next} flag && flag<=$NATOMS{print; flag++}" $1 | awk '{print $3, $4, $5, $6, $7, $8, $9, $10, $11}' > nc_tmp

# Convert the nc_tmp into sepatated files
# To check the mode number
NUMBER=0

# Obtain how many lines i will have to interact
NINT=$(($NNORMAL/3))
REST=$(($NNORMAL%3))
if [ $REST == 0 ]; then
    NINT=$(($NINT+1))
fi

# Loop for each NATOMS lines 
for ((lines = 0; lines < $NINT-1; lines++)); do

# Print lines 
    ILINE=$(($lines*$NATOMS+1))
    FLINE=$(($ILINE+$NATOMS-1))
 
    sed -n "${ILINE},${FLINE}p" nc_tmp > l_tmp

# Loop for each 3columns    
    for each in 0 1 2; do
        
        NUMBER=$(($NUMBER+1))
        
        columnx=$(($each*3+1))
        columny=$(($each*3+2))
        columnz=$(($each*3+3))

        awk -v x=$columnx -v y=$columny -v z=$columnz '{print $x, $y, $z}' l_tmp > nmode$NUMBER.log
        
    done

done

# Paste the atoms letter information
# Find the line containing "Distance matrix" and print the line number
LN=$(grep -n "Distance matrix" $1 | cut -d ':' -f1)

# Extract the atoms from lines below
ATOMS=$(sed -n "$(($LN+2)),$(($LN + $NATOMS +1))p" $1 | awk '{print $2}')

# Write the information about the normal mode
for ((i = 1; i < $NNORMAL+1; i++)); do
    PLACE=$i-1
    
    awk -v arr="${ATOMS[*]}" 'BEGIN {split(arr, a); i=1} {print a[i], $0; i++}' nmode$i.log > tmp && mv tmp nmode$i.log
    column -t nmode$i.log > tmp && mv tmp nmode$i.log

    echo "Frequencies: ${FREQ[$PLACE]} cm**-1
Red. masses: ${RMASS[$PLACE]} AMU
Frc constas: ${FORCE[$PLACE]} mDyne/A
IR Intenens: ${IR[$PLACE]} KM/Mole" | cat - nmode$i.log > tmp && mv tmp nmode$i.log 

done

# Remove tmp files
rm l_tmp nc_tmp