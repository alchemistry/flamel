"""Provide the primary functions."""

import argparse
import logging
import pathlib
import pickle
import sys

from alchemlyb.workflows import ABFE

def main():
    parser = argparse.ArgumentParser(description="""
                    Collect data and estimate free energy differences
                    """, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-a', '--software', dest='software',
                        help='Package\'s name the data files come from: '
                             'GROMACS or AMBER. Default: GROMACS.',
                        default='GROMACS')
    parser.add_argument('-d', '--dir', dest='datafile_directory',
                        help='Directory in which data files are stored. '
                             'Default: Current directory.', default='./')
    parser.add_argument('-f', '--forwrev', dest='forwrev',
                        help='Plot the free energy change as a function of '
                             'time in both directions, with the specified '
                             'number of points in the time plot. The number '
                             'of time points (an integer) must be provided. '
                             'Default: 0', default=0, type=int)
    parser.add_argument('-g', '--breakdown', dest='breakdown',
                        help='Plot the free energy differences evaluated for '
                             'each pair of adjacent states for all methods, '
                             'including the dH/dlambda curve for TI.'
                             'Default: True.', default=True, action='store_true')
    parser.add_argument('-i', '--threshold', dest='uncorr_threshold',
                      help='Proceed with correlated samples if the number of '
                           'uncorrelated samples is found to be less than this'
                           ' number. If 0 is given, the time series analysis '
                           'will not be performed at all. Default: 50.',
                      default=50, type=int)
    parser.add_argument('-j', '--resultfilename', dest='resultfilename',
                      help='custom defined result filename prefix. '
                           'Default: results.csv',
                      default='results.csv')

    parser.add_argument('-m', '--methods', dest='methods',
                      help='A comma separated list of the methods to estimate '
                           'the free energy with. Default: TI,BAR,MBAR.',
                      default='TI,BAR,MBAR')
    parser.add_argument('-n', '--uncorr', dest='uncorr',
                        help='The observable to be used for the '
                             'autocorrelation analysis; either \'all\' '
                             '(obtained as a sum over all energy components) '
                             'or \'dE\'. In the latter case the energy '
                             'differences dE_{i,i+1} (dE_{i,i-1} for the last '
                             'lambda) are used.',
                        default='dE')
    parser.add_argument('-o', '--out', dest='output_directory',
                      help='Directory in which the output files produced by '
                           'this script will be stored. Default: Same as '
                           'datafile_directory.',
                      default='')
    parser.add_argument('-p', '--prefix', dest='prefix',
                        help='Prefix for datafile sets, i.e.\'dhdl\' (default).',
                        default='dhdl')
    parser.add_argument('-q', '--suffix', dest='suffix',
                        help='Suffix for datafile sets, i.e. \'xvg\' (default).',
                        default='xvg')
    parser.add_argument('-r', '--decimal', dest='decimal',
                        help='The number of decimal places the free energies '
                             'are to be reported with. No worries, this is for '
                             'the text output only; the full-precision data '
                             'will be stored in \'results.pickle\'. Default: 3.',
                        default=3, type=int)
    parser.add_argument('-s', '--skiptime', dest='equiltime',
                        help='Discard data prior to this specified time as '
                             '\'equilibration\' data. Units picoseconds. '
                             'Default: 0 ps.',
                        default=0, type=float)
    parser.add_argument('-t', '--temperature', dest='temperature',
                        help="Temperature in K. Default: 298 K.",
                        default=298.0, type=float)
    parser.add_argument('-u', '--units', dest='units',
                      help='Units to report energies: \'kJ/mol\', \'kcal/mol\', and \'kT\'. Default: \'kcal/mol\'',
                      default='kcal/mol')
    parser.add_argument('-v', '--verbose', dest='verbose',
                      help='Verbose option. Default: False.', default=False,
                      action='store_true')
    parser.add_argument('-w', '--overlap', dest='overlap',
                      help='Print out and plot the overlap matrix. Default: True.',
                      default=True, action='store_true')

    args = parser.parse_args(sys.argv[1:])

    # Print the logging to the console
    if args.verbose:
        logging.getLogger().addHandler(logging.StreamHandler())

    if args.output_directory == '':
        out = args.datafile_directory
    else:
        out = args.output_directory
    if args.overlap:
        overlap = 'O_MBAR.pdf'
    else:
        overlap = ''

    workflow = ABFE(T=args.temperature, units=args.units, software=args.software,
                    dir=args.datafile_directory, prefix=args.prefix, suffix=args.suffix,
                    outdirectory=out)
    workflow.run(skiptime=args.equiltime, uncorr=args.uncorr,
                 threshold=args.uncorr_threshold, estimators=args.methods.split(','),
                 overlap=overlap, breakdown=args.breakdown,
                 forwrev=args.forwrev)
    summary = workflow.summary
    pickle.dump(summary, open(pathlib.Path(out) / 'result.p', 'wb'))
    summary.round(args.decimal).to_csv(pathlib.Path(out) / args.resultfilename)

if __name__ == "__main__":
    main()
