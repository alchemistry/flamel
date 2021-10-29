# Flamel

The aim of the project is to develop a **command line interface (CLI) to [alchemlyb](https://github.com/alchemistry/alchemlyb)**, the well-tested and actively developed library for alchemical free energy calculations. 
It is supposed to [become the successor](https://github.com/alchemistry/alchemlyb/wiki/Roadmap#librarify-alchemical-analysis-functionality) of the now unsupported [alchemical-analysis](https://github.com/MobleyLab/alchemical-analysis) script.

----

This project is currently *dormant* due to lack of developers. If you are **interested in contributing** please raise issues/open pull requests and ping [@orbeckst](https://github.com/orbeckst) and [@xiki-tempula](https://github.com/xiki-tempula) to get our attention. 
We are happy to see new contributors!

Please read the [proposed future directions](https://github.com/alchemistry/alchemlyb/discussions/159#discussioncomment-1560486), which form the informal roadmap for developments.

----


# Installation
1. Download and install alchemlyb
```shell
pip install alchemlyb
```
2. Download flamel
```shell
git clone git@github.com:alchemistry/flamel.git
```

# Usage
Currently only Gromacs parser and uncorrelation by dH/dl is supported!
```
usage: flamel.py [-h] [-t TEMPERATURE] [-p PREFIX] [-q SUFFIX] [-e ESTIMATORS]
                 [-n UNCORR] [-r DECIMAL] [-o OUTPUT] [-a SOFTWARE]
                 [-s EQUILTIME]

Collect data and estimate free energy differences

optional arguments:
  -h, --help            show this help message and exit
  -t TEMPERATURE, --temperature TEMPERATURE
                        Temperature in K. Default: 298 K. (default: 298.0)
  -p PREFIX, --prefix PREFIX
                        Prefix for datafile sets, i.e.'dhdl' (default).
                        (default: dhdl)
  -q SUFFIX, --suffix SUFFIX
                        Suffix for datafile sets, i.e. 'xvg' (default).
                        (default: xvg)
  -e ESTIMATORS         Comma separated Estimator methods (default: None)
  -n UNCORR, --uncorr UNCORR
                        The observable to be used for the autocorrelation
                        analysis; either 'dhdl_all' (obtained as a sum over
                        all energy components) or 'dhdl' (obtained as a sum
                        over those energy components that are changing;
                        default) or 'dE'. In the latter case the energy
                        differences dE_{i,i+1} (dE_{i,i-1} for the last
                        lambda) are used. (default: dhdl)
  -r DECIMAL, --decimal DECIMAL
                        The number of decimal places the free energies are to
                        be reported with. No worries, this is for the text
                        output only; the full-precision data will be stored in
                        'results.pickle'. Default: 3. (default: 3)
  -o OUTPUT, --output OUTPUT
                        Output methods (default: None)
  -a SOFTWARE, --software SOFTWARE
                        Package's name the data files come from: Gromacs,
                        Sire, Desmond, or AMBER. Default: Gromacs. (default:
                        Gromacs)
  -s EQUILTIME, --skiptime EQUILTIME
                        Discard data prior to this specified time as
                        'equilibration' data. Units picoseconds. Default: 0
                        ps. (default: 0)
```

To read enumerated xvg files lambda_0.xvg, lambda_1.xvg, ... use: 
```shell
flamel.py -p lambda_
```

You should get a similar overview as [alchemical-analysis](https://github.com/MobleyLab/alchemical-analysis).

# How it works
- Step 1: Read the necessary data
- Step 2: Uncorrelate the data
- Step 3: Estimate Free energy differences
- Step 4: Output

Each step is performed in Plugins which can easyly be be replaced by other plugins. 

# Name
In the tradition to associate free energy estimations with alchemistry it's named after: [Nicolas Flamel](https://en.wikipedia.org/wiki/Nicolas_Flamel)

# State of development:
Eventhoug alchemical-analysis is not fully covered by Flamel, it can already reproduce some results calculated using alchemical-analysis:

In fact for TI, BAR, MBAR you should get exactly the same results:

Example Flamel output for the [water_particle/without_energy](https://github.com/alchemistry/alchemtest/tree/master/src/alchemtest/gmx/water_particle/without_energy) dataset:
``` 
------------ --------------------- --------------------- --------------------- 
   States           TI (kJ/mol)          BAR (kJ/mol)         MBAR (kJ/mol)    
------------ --------------------- --------------------- --------------------- 
   0 -- 1         0.074  +-  0.005      0.073  +-  0.005      0.071  +-  0.003 
...
  36 -- 37       -5.472  +-  0.038     -5.475  +-  0.038     -5.457  +-  0.028 
------------ --------------------- --------------------- --------------------- 
     coul:      -41.067  +-  0.129    -41.022  +-  nan      -41.096  +-  0.170 
      vdw:       11.912  +-  0.113     11.954  +-  nan       12.022  +-  0.142 
    TOTAL:      -29.154  +-  0.172    -29.067  +-  nan      -29.074  +-  0.220 
```

Alchemical Analysis with the same input files:
```
------------ --------------------- --------------------- --------------------- 
   States           TI (kJ/mol)          BAR (kJ/mol)         MBAR (kJ/mol)    
------------ --------------------- --------------------- --------------------- 
   0 -- 1         0.074  +-  0.005      0.073  +-  0.005      0.071  +-  0.003 
...
  36 -- 37       -5.472  +-  0.038     -5.475  +-  0.038     -5.457  +-  0.028 
------------ --------------------- --------------------- --------------------- 
  Coulomb:      -41.067  +-  0.180    -41.022  +-  0.129    -41.096  +-  0.170 
  vdWaals:       11.912  +-  0.160     11.954  +-  0.111     12.022  +-  0.139 
    TOTAL:      -29.154  +-  0.241    -29.067  +-  0.170    -29.074  +-  0.220
```

# Planed features:
- **Output of statistical inefficiencies**
alchemical-analysis offers information about the statistical inefficiencies of the input datasets.
- **Uncorrelation threshold**
In alchemical-analysis it is possible to specify a threshold for the number of samples to keep in the uncorrelation process.
