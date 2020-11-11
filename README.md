# Flamel

The aim of this project is to develop the foundation for a new version of [alchemical-analysis](https://github.com/MobleyLab/alchemical-analysis)
that uses the well tested [alchemlyb](https://github.com/alchemistry/alchemlyb) library.

# Installation
1. Download and install alchemlyb
```shell
git clone git@github.com:alchemistry/alchemlyb.git
cd alchemlyb
pip install .
```
2. Download flamel
```shell
git clone git@github.com:alchemistry/flamel.git
```

# Usage
Currently only Gromacs parser and uncorrelation by dH/dl is supported!
```
usage: flamel.py [-h] [-t TEMPERATURE] [-p PREFIX] [-d DATAFILE_DIRECTORY]
                 [-q SUFFIX] [-e ESTIMATORS] [-n UNCORR] [-j RESULTFILENAME]
                 [-u UNIT] [-r DECIMAL] [-o OUTPUT] [-a SOFTWARE]
                 [-s EQUILTIME]

Collect data and estimate free energy differences

optional arguments:
  -h, --help            show this help message and exit
  -t TEMPERATURE, --temperature TEMPERATURE
                        Temperature in K. Default: 298 K. (default: 298.0)
  -p PREFIX, --prefix PREFIX
                        Prefix for datafile sets, i.e.'dhdl' (default).
                        (default: dhdl)
  -d DATAFILE_DIRECTORY, --dir DATAFILE_DIRECTORY
                        Directory in which data files are stored. Default:
                        Current directory. (default: .)
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
  -j RESULTFILENAME, --resultfilename RESULTFILENAME
                        custom defined result filename prefix. Default:
                        results (default: results)
  -u UNIT, --unit UNIT  Unit to report energies: 'kJ', 'kcal', and 'kT'.
                        Default: 'kJ' (default: kJ)
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

You also get a text file `results.txt` with the state overview, as well as a pickle file `results.pickle` with full precision values as well as complementary information about the analysis. 

Example:
```
>>> import pandas as pd
>>> data = pd.read_pickle('results.pickle')
>>> data.
data.dF                  data.datafile_directory  data.decimal             data.estimators          data.prefix              data.software            data.temperature         data.unit
data.dFs                 data.ddFs                data.equiltime           data.output              data.resultfilename      data.suffix              data.uncorr              data.when_analyzed
>>> data.when_analyzed
'Wed Nov 11 15:22:32 2020'
>>> data.equiltime
0
>>> data.software
'Gromacs'
>>> data.dF['TI']
{'coul-lambda': (-15.633404527627823, 0.03466623342555742), 'vdw-lambda': (3.8237866774171514, 0.02952686840637163), 'total': (-11.809617850210671, 0.04553661930581169)}
>>> data.dF['MBAR']['coul-lambda']
(-15.617280704605726, 0.03241377327730135)
>>> 
```

# How it works
- Step 1: Read the necessary data
- Step 2: Uncorrelate the data
- Step 3: Estimate Free energy differences
- Step 4: Output

Each step is performed in Plugins which can easily be replaced by other plugins. 

# Name
In the tradition to associate free energy estimations with alchemy, the ancient craft of transmutating one element into another, it's named after: [Nicolas Flamel](https://en.wikipedia.org/wiki/Nicolas_Flamel).

# State of development
Eventhough alchemical-analysis is not fully covered by Flamel, it can already reproduce some results calculated using alchemical-analysis:

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

# Planned features
- [ ] **plotting** 
Add support for plotting the dHdls of states and the BAR/MBAR overlap matrix (preliminary feature in alchemlyb).
- [x] **pickle and txt output**
alchemical-analysis outputs the simple result table as a text file as well as the full precision calculations as a numpy-compatible pickle file.
- [ ] **Output of statistical inefficiencies**
alchemical-analysis offers information about the statistical inefficiencies of the input datasets.
- [ ] **Uncorrelation threshold**
In alchemical-analysis it is possible to specify a threshold for the number of samples to keep in the uncorrelation process.
