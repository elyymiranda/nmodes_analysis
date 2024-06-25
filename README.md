# Introduction

This project made for G16 frequency analisys of vibronic anion-neutral excitation. Basically, it is useful to analyse Vibrational Feshbach Ressonance energies for low-energy electron-molecule process.

You can use this project to:
1. Calculate the anion-neutral vibronic excitation energies for both harminic and anharmonic calculations; 
2. Create geometries files for potential energy surface (PES) calculation using the normal coordinates given by G16 harmonic calculation; 
3. Plot the anion-neutral PES with harmonic staps (ZPE, overtones).

Here you can find a tiny tutorial to learn how you could employ this project:

# Tutorial

## Calculate the anion-neutral vibronic excitation energies

1. You shoud have the anion's and neutral's G16 frequency .log file and comp_table file. The comp_table file exemple is in the exemple folder. Basically you shoud indicate the cgir orrepondence of neutral and anion normal modes. 

2. For harmonic case: Use *split_frequencies.sh* script to each anion and neutral .log files to creatre the nmode.dat files
``$ ./split_frequencies.sh neutral.log``
``$ mkdir neutral``
``$ mv nmode* neutral/``

``$ ./split_frequencies.sh anion.log``
``$ mkdir anion``
``$ mv nmode* anion/``

For anharmonic case: