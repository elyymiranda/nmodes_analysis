#!/bin/bash

# This script gets the sp data from both neutral and anion single point calculation and create a table with all required information.
# Script made by Ely Miranda, PhD student at Physics Institute in Universidade de São Paulo
# Last update: 22/04/2024
# Any question or suggestion write me: ely.miranda@usp.br :)

# To run this script use:
# ./join_data comp_table parameter.log STEP=step path/to/log/neutral path/to/log/anion 

# Get the number os lines of comp_table to obtain total normal modes number
NMODES=$(wc -l $1 | awk '{print $1}')

# For each line in the comp_table, obtain the single point energy for each mode
# Obtain the parameter energy from parameter.log
EPAR=$(grep "SCF Done:" $2 | awk '{print $5}')

# Hartree2eV
hf2ev=27.2114

# Step in normal coordinates
STEP=$3

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
	NFREQ=$(awk '/Frequencies/ {print $2}' $4/nmode$MODENEUTRO/nmode$MODENEUTRO.log)
	AFREQ=$(awk '/Frequencies/ {print $2}' $5/nmode$MODEANION/nmode$MODEANION.log)

	# Obtain IR intensity
	NIR=$(awk '/IR Intenens/ {print $3}' $4/nmode$MODENEUTRO/nmode$MODENEUTRO.log)
	AIR=$(awk '/IR Intenens/ {print $3}' $5/nmode$MODEANION/nmode$MODEANION.log)
	
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


	# Print columns name
	printf "%-15s %-15s %-15s %-15s\n" "Step" "Neutral" "Anion0" "Anion1" > nmode$MNUMBER.dat

	for each in $(ls -1 $4/nmode$MODENEUTRO/*.log | sort -n -t _ -k 2 | xargs -n 1 basename); do

		# Find and scale the neutral energy
		ENEUTRAL=$(grep "SCF Done:" $4/nmode$MODENEUTRO/$each | awk '{print $5}')
		FENEUTRAL=$(awk -v s1=$EPAR -v s2=$ENEUTRAL -v s3=$hf2ev 'BEGIN { printf "%.3f\n", (- s1 + s2) * s3}')
	
		# Find and scale the anion energy
		EANION=$(grep "SCF Done:" $5/nmode$MODEANION/$each | awk '{print $5}')
		FEANION=$(awk -v s1=$EPAR -v s2=$EANION -v s3=$hf2ev 'BEGIN { printf "%.3f\n", (- s1 + s2) * s3}')

		# Find and scale the first anion excited state
		EXANION=$(grep "Total Energy, E(TD-HF/TD-DFT) =" $5/nmode$MODEANION/$each | awk '{print $5}')
		FEXANION=$(awk -v s1=$EPAR -v s2=$EXANION -v s3=$hf2ev 'BEGIN { printf "%.3f\n", (- s1 + s2) * s3}')

		# Calculate the factor step
		NUMBER=$(echo $each | sed 's/^step_\(-*[0-9]*\)\.log$/\1/')
		FACTOR=$(awk -v s1=$STEP -v s2=$NUMBER 'BEGIN { printf "%.2f\n", s1 * s2}')

		# Check if ENERGY is less than 1000
    	if (( $(echo "$FENEUTRAL > 1000" | bc -l) )) || (( $(echo "$FEANION > 1000" | bc -l) )); then
        	echo "	Some calculation in $FACTOR step does not converged. Check gaussian .log neutral and anion files" >>  $LOG
        	
		else
			# Print the result in a table
			printf "%-15s %-15s %-15s %-15s\n" "$FACTOR" "$FENEUTRAL" "$FEANION" "$FEXANION" >> nmode$MNUMBER.dat
    	fi

	done

    echo "    ---------------------------------------------------------------------------
	" >> $LOG

done < $1
