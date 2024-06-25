#!/bin/bash

# This script gets the sp data from both neutral and anion single point calculation.
# Script made by Ely Miranda, PhD student at Physics Institute in Universidade de São Paulo
# Last update: 31/05/2024
# Any question or suggestion write me: ely.miranda@usp.br :)

# To run this script use:
# ./join_data comp_table path/to/log/neutral path/to/log/anion 

# Get the number os lines of comp_table to obtain total normal modes number
NMODES=$(wc -l $1 | awk '{print $1}')

# For each line in the comp_table, obtain the single point energy for each mode
# LOG file for analisys and debbug
LOG=join_data.log

# Keep on track on the line number or the nmodes number
MNUMBER=0

# Print information in LOG file
echo "Starting the analisys for modes comparison
" > $LOG

# For each line in comp_table
while IFS=':' read -r line_number _; do
	
	# Update number value
	MNUMBER=$((MNUMBER+1))

	# Obtain the normal mode for neutro
	MODENEUTRO=$(echo $line_number | awk '{print $1}')
	
	# Obtain the respective normal mode (in respect to neutro) for anion
	MODEANION=$(echo $line_number |  awk '{print $2}')

	# Obtain frequencies 
	NFREQ=$(awk '/Frequencies/ {print $2}' $2/nmode$MODENEUTRO.log)
	AFREQ=$(awk '/Frequencies/ {print $2}' $3/nmode$MODEANION.log)

	# Obtain IR intensity
	NIR=$(awk '/IR Intenens/ {print $3}' $2/nmode$MODENEUTRO.log)
	AIR=$(awk '/IR Intenens/ {print $3}' $3/nmode$MODEANION.log)
	
	# Print information in the log file
	echo "                              Done $MNUMBER of $NMODES 
    ---------------------------------------------------------------------------
	Normal mode correspondence from table
	Neutral's $MODENEUTRO normal mode <-> Anion's $MODEANION normal mode
	
	Frequencies (cm**-1)
	Neutral: $NFREQ
	Anion: $AFREQ

	IR intensities (KM/Mole)
	Neutral: $NIR
	Anion: $AIR    	
	" >> $LOG

    echo "    ---------------------------------------------------------------------------
	" >> $LOG

done < $1
