# Introduction

This project made for G16 frequency analisys of vibronic anion-neutral excitation. Basically, it is useful to analyse Vibrational Feshbach Ressonance energies for low-energy electron-molecule process.

You can use this project to:
1. Calculate the anion-neutral vibronic excitation energies for both harminic and anharmonic calculations; 
2. Create geometries files for potential energy surface (PES) calculation using the normal coordinates given by G16 harmonic calculation; 
3. Plot the anion-neutral PES with harmonic staps (ZPE, overtones).

Here you can find a tiny tutorial to learn how you could employ this project:

# Tutorial

## Calculate the anion-neutral vibronic excitation energies

1. You shoud have the anion's and neutral's G16 frequency .log file and comp_table file (if you just have the anharmonic .log files, you also will need a single point .log file for each anion and neutral). The comp_table file exemple is in the exemple folder. Basically you shoud indicate the cgir orrepondence of neutral and anion normal modes. 

2. Creating nmode.dat files: 

For harmonic case: Use *split_frequencies.sh* script to each anion and neutral .log files to creatre the nmode.dat files
``` bash
./split_frequencies.sh neutral.log
mkdir neutral
mv nmode* neutral/

./split_frequencies.sh anion.log
mkdir anion
mv nmode* anion/
```

For anharmonic case: Use *split_anharm.sh* script to each anion and neutral .log files to creatre the nmode.dat files
``` bash
./split_anharm.sh neutral.log > freq_neutro.log

./split_anharm.sh anion.log > freq_anion.log
```

3. Creating the comparison file

For harmonic case: Use *join_data.sh* script to join anion and neutral infos 
``` bash
./join_sp.sh comp_table neutral/ anion/

./vibronic_excitation.py join_data.log neutral.log anion.log
```

For anharmonic case: Use *join_data.sh* script to join anion and neutral infos (here you can use single point .log files or harmonic .log files)
``` bash
./vibronic_excitation.py none sp_neutral.log sp_anion.log neutral.log anion.log
```

## Create .xyz files to PES calculation