Flamel
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

Run ``flamel -h`` to see the full description of the options.

# Output
This script si a warpper around the 
[ABFE](https://alchemlyb.readthedocs.io/en/latest/workflows/alchemlyb.workflows.ABFE.html#alchemlyb.workflows.ABFE) 
workflow in [alchemlyb](https://github.com/alchemistry/alchemlyb). 
The script will generate the output from ABFE workflow, including 
[O_MBAR.pdf](https://alchemlyb.readthedocs.io/en/latest/visualisation.html#overlap-matrix-of-the-mbar),
[dF_t.pdf](https://alchemlyb.readthedocs.io/en/latest/visualisation.html#df-states-plots-between-different-estimators),
[dF_state.pdf](https://alchemlyb.readthedocs.io/en/latest/visualisation.html#overlap-matrix-of-the-mbar),
[dF_t.pdf](https://alchemlyb.readthedocs.io/en/latest/visualisation.html#forward-and-backward-convergence),
[dhdl_TI.pdf](https://alchemlyb.readthedocs.io/en/latest/visualisation.html#dhdl-plot-of-the-ti).

The script will also generate the `result.csv` ::

                      TI  TI_Error    BAR  BAR_Error   MBAR  MBAR_Error
    States 0 -- 1  0.962     0.007  0.956      0.007  0.964       0.006
           1 -- 2  0.567     0.006  0.558      0.006  0.558       0.004
           2 -- 3  0.264     0.005  0.258      0.005  0.254       0.004
           3 -- 4  0.035     0.004  0.035      0.004  0.030       0.003
    Stages fep     1.828     0.014  1.806      0.016  1.807       0.014
           TOTAL   1.828     0.014  1.806      0.011  1.807       0.014

# Name
In the tradition to associate free energy estimations with alchemistry it's 
named after: [Nicolas Flamel](https://en.wikipedia.org/wiki/Nicolas_Flamel)

### Copyright

Copyright (c) 2022, alchemistry


#### Acknowledgements
 
Project based on the 
[Computational Molecular Science Python Cookiecutter](https://github.com/molssi/cookiecutter-cms) version 1.1.
