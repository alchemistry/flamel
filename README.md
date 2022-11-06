flamel
==============================
[//]: # (Badges)
[![GitHub Actions Build Status](https://github.com/alchemistry/flamel/workflows/CI/badge.svg)](https://github.com/alchemistry/flamel/actions?query=workflow%3ACI)
[![codecov](https://codecov.io/gh/alchemistry/flamel/branch/main/graph/badge.svg)](https://codecov.io/gh/alchemistry/flamel/branch/main)


The aim of the project is to develop a **command line interface (CLI) to 
[alchemlyb](https://github.com/alchemistry/alchemlyb)**, the well-tested and 
actively developed library for alchemical free energy calculations. It is 
supposed to [become the successor](https://github.com/alchemistry/alchemlyb/wiki/Roadmap#librarify-alchemical-analysis-functionality) 
of the now unsupported [alchemical-analysis](https://github.com/MobleyLab/alchemical-analysis) script.

# Installation

Clone flamel and install
```shell
git clone git@github.com:alchemistry/flamel.git
cd flamel
pip install .
```

# Usage

The analysis could be invoked with the following command

```shell
flamel -a GROMACS -d dhdl_data -f 10 -g -i 50 -j result.csv -m TI,BAR,MBAR -n dE -o out_data -p dhdl -q xvg -r 3 -s 50 -t 298 -v  -w
```

Currently only GROMACS and AMBER parser are supported!
```
usage: flamel [-h] [-a SOFTWARE] [-d DATAFILE_DIRECTORY] [-f BFORWREV] [-g] 
              [-i UNCORR_THRESHOLD] [-j RESULTFILENAME] [-m METHODS] 
              [-n UNCORR] [-o OUTPUT_DIRECTORY] [-p PREFIX] [-q SUFFIX] 
              [-r DECIMAL] [-s EQUILTIME] [-t TEMPERATURE] [-u UNITS] [-v] [-w]

Collect data and estimate free energy differences

options:
  -h, --help            show this help message and exit
  -a SOFTWARE, --software SOFTWARE
                        Package's name the data files come from: Gromacs or 
                        AMBER. Default: Gromacs.
  -d DATAFILE_DIRECTORY, --dir DATAFILE_DIRECTORY
                        Directory in which data files are stored. Default: 
                        Current directory.
  -f BFORWREV, --forwrev BFORWREV
                        Plot the free energy change as a function of time in 
                        both directions, with the specified number of points in
                         the time plot. The number of time points (an integer) 
                         must be provided. Default: 0.
  -g, --breakdown       Plot the free energy differences evaluated for each 
                        pair of adjacent states for all methods, including the 
                        dH/dlambda curve for TI. Default: True.
  -i UNCORR_THRESHOLD, --threshold UNCORR_THRESHOLD
                        Proceed with correlated samples if the number of 
                        uncorrelated samples is found to be less than this 
                        number. If 0 is given, the time series analysis will
                        not be performed at all. Default: 50. 
  -j RESULTFILENAME, --resultfilename RESULTFILENAME
                        custom defined result filename prefix. Default: 
                        results.csv
  -m METHODS, --methods METHODS
                        A comma separated list of the methods to estimate the 
                        free energy with. Default: TI,BAR,MBAR. 
  -n UNCORR, --uncorr UNCORR
                        The observable to be used for the autocorrelation 
                        analysis; either 'all' (obtained as a sum over all 
                        energy components) or 'dE'. In the latter case the
                        energy differences dE_{i,i+1} (dE_{i,i-1} for the last 
                        lambda) are used. (default: dE)
  -o OUTPUT_DIRECTORY, --out OUTPUT_DIRECTORY
                        Directory in which the output files produced by this 
                        script will be stored. Default: Same as 
                        datafile_directory.
  -p PREFIX, --prefix PREFIX
                        Prefix for datafile sets, i.e.'dhdl' (default).
  -q SUFFIX, --suffix SUFFIX
                        Suffix for datafile sets, i.e. 'xvg' (default).
  -r DECIMAL, --decimal DECIMAL
                        The number of decimal places the free energies are to 
                        be reported with. No worries, this is for the text 
                        output only; the full-precision data will be stored in 
                        'results.pickle'. Default: 3.
  -s EQUILTIME, --skiptime EQUILTIME
                        Discard data prior to this specified time as 
                        'equilibration' data. Units picoseconds. Default: 0 ps.
  -t TEMPERATURE, --temperature TEMPERATURE
                        Temperature in K. Default: 298 K. 
  -u UNITS, --units UNITS
                        Units to report energies: 'kJ/mol', 'kcal/mol', and 
                        'kT'. Default: 'kcal/mol'
  -v, --verbose         Verbose option. Default: False. 
  -w, --overlap         Print out and plot the overlap matrix. Default: True.
```

# Name
In the tradition to associate free energy estimations with alchemistry it's 
named after: [Nicolas Flamel](https://en.wikipedia.org/wiki/Nicolas_Flamel)

### Copyright

Copyright (c) 2022, alchemistry


#### Acknowledgements
 
Project based on the 
[Computational Molecular Science Python Cookiecutter](https://github.com/molssi/cookiecutter-cms) version 1.1.
