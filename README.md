# Flamel
A plugin based free energy estimation tool based on [alchemlyb](https://github.com/alchemistry/alchemlyb)

# Installation
1. Download and install alchemlyb
```shell
git clone git@github.com:harlor/alchemlyb.git
cd alchemlyb
pip install .
```
2. Download flamel
```shell
git clone git@github.com:harlor/flamel.git
```

# Usage
Currently only Gromacs parser is supported:
```
usage: flamel.py [-h] [-t T] [-p PRE] [-s SUFFIX] [-e ESTIMATORS]
                 [-u UNCORRELATOR] [-o OUTPUT] [-parser PARSER]

Collect data and estimate free energy differences

optional arguments:
  -h, --help       show this help message and exit
  -t T             Temperature (default: 300.0)
  -p PRE           File prefix (default: )
  -s SUFFIX        File suffix (default: .xvg)
  -e ESTIMATORS    Comma separated Estimator methods (default: None)
  -u UNCORRELATOR  Data uncorrelation method (default:
                   statistical_inefficiency_dhdl)
  -o OUTPUT        Output methods (default: None)
  -parser PARSER   Parser (default: gmx)
```

To read enumerated xvg files lambda_0.xvg, lambda_1.xvg, ... use: 
```shell
flamel.py -p lambda_ -s .xvg -t 300
```

You should get a similar overview as [alchemical-analysis](https://github.com/MobleyLab/alchemical-analysis).

# How it works
- Step 1: Read the necessary data
- Step 2: Uncorrelate the data
- Step 3: Estimate Free energy differences
- Step 4: Output

Each step is performed in Plugins which can easyly be be replaced by other plugins. 

# Name
In the tradition to refer free energy estimations to alchemnistry it's named after: [Nicolas Flamel](https://en.wikipedia.org/wiki/Nicolas_Flamel)

# Example output:

``` 
------------ --------------------- --------------------- --------------------- 
   States           TI (kJ/mol)         MBAR (kJ/mol)     TI-CUBIC (kJ/mol)    
------------ --------------------- --------------------- --------------------- 
   0 -- 1         0.080  +-  0.001      0.078  +-  0.001      0.076  +-  0.001 
   1 -- 2         0.241  +-  0.002      0.242  +-  0.001      0.239  +-  0.002 
   2 -- 3         0.435  +-  0.003      0.437  +-  0.001      0.431  +-  0.003 
   3 -- 4         0.666  +-  0.004      0.665  +-  0.002      0.665  +-  0.004 
   4 -- 5         0.924  +-  0.006      0.921  +-  0.002      0.923  +-  0.006 
   5 -- 6         1.196  +-  0.008      1.189  +-  0.004      1.198  +-  0.008 
   6 -- 7         1.432  +-  0.013      1.420  +-  0.005      1.446  +-  0.013 
   7 -- 8         1.510  +-  0.018      1.514  +-  0.008      1.532  +-  0.018 
   8 -- 9         1.352  +-  0.021      1.364  +-  0.011      1.365  +-  0.021 
   9 -- 10        1.044  +-  0.021      1.027  +-  0.010      1.043  +-  0.021 
  10 -- 11        0.734  +-  0.018      0.727  +-  0.008      0.725  +-  0.018 
  11 -- 12        0.520  +-  0.014      0.553  +-  0.007      0.509  +-  0.014 
  12 -- 13        0.423  +-  0.011      0.449  +-  0.006      0.419  +-  0.011 
  13 -- 14        0.375  +-  0.010      0.374  +-  0.005      0.378  +-  0.010 
  14 -- 15        0.313  +-  0.010      0.312  +-  0.004      0.312  +-  0.010 
  15 -- 16        0.265  +-  0.010      0.261  +-  0.004      0.262  +-  0.010 
  16 -- 17        0.237  +-  0.009      0.218  +-  0.003      0.240  +-  0.009 
  17 -- 18        0.197  +-  0.009      0.182  +-  0.003      0.197  +-  0.009 
  18 -- 19        0.152  +-  0.008      0.149  +-  0.002      0.151  +-  0.008 
  19 -- 20        0.123  +-  0.006      0.121  +-  0.002      0.120  +-  0.006 
  20 -- 21       -0.135  +-  0.006     -0.129  +-  0.003     -0.132  +-  0.006 
  21 -- 22       -0.377  +-  0.005     -0.379  +-  0.003     -0.379  +-  0.005 
  22 -- 23       -0.625  +-  0.006     -0.644  +-  0.003     -0.618  +-  0.006 
  23 -- 24       -0.934  +-  0.008     -0.939  +-  0.004     -0.927  +-  0.008 
  24 -- 25       -1.313  +-  0.010     -1.288  +-  0.005     -1.313  +-  0.010 
  25 -- 26       -1.742  +-  0.012     -1.717  +-  0.006     -1.723  +-  0.012 
  26 -- 27       -1.471  +-  0.011     -1.437  +-  0.005     -1.469  +-  0.011 
  27 -- 28       -1.755  +-  0.014     -1.715  +-  0.006     -1.759  +-  0.014 
  28 -- 29       -2.032  +-  0.014     -2.029  +-  0.006     -2.022  +-  0.014 
  29 -- 30       -2.381  +-  0.014     -2.377  +-  0.007     -2.381  +-  0.014 
  30 -- 31       -2.752  +-  0.013     -2.750  +-  0.007     -2.752  +-  0.013 
  31 -- 32       -3.136  +-  0.012     -3.144  +-  0.008     -3.129  +-  0.012 
  32 -- 33       -3.569  +-  0.015     -3.561  +-  0.008     -3.571  +-  0.015 
  33 -- 34       -4.009  +-  0.016     -4.003  +-  0.009     -4.005  +-  0.016 
  34 -- 35       -4.479  +-  0.016     -4.474  +-  0.010     -4.480  +-  0.016 
  35 -- 36       -4.956  +-  0.017     -4.970  +-  0.011     -4.956  +-  0.017 
  36 -- 37       -5.475  +-  0.019     -5.480  +-  0.014     -5.457  +-  0.019 
------------ --------------------- --------------------- --------------------- 
    TOTAL:      -28.920  +-  0.104    -28.835  +-  0.092    -28.842  +-  0.104 
```

