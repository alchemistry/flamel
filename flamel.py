#!/usr/bin/env python

import argparse


def get_available_plugins(type):
    # Todo: Implement this

    if type == 'estimator':
        return ['ti', 'mbar']
    return ['simple', 'alchemical_analysis']


def load_plugin(type, name, *args):
    # Todo: think about a suitable plugin system
    mod = __import__("%s.%s" % (type, name), fromlist=['object'])
    return mod.get_plugin(*args)


def argsplit(arg):
    return [] if arg is None else arg.split(',')


def load_plugins(type, selected):
    available = get_available_plugins(type)
    plugin_names = []
    if selected:
        for plugin_name in selected:
            if plugin_name in available:
                plugin_names.append(plugin_name)

    else:
        plugin_names = available

    plugins = []
    for plugin_name in plugin_names:
        plugins.append(load_plugin(type, plugin_name))

    return plugins


def main():
    parser = argparse.ArgumentParser(description="""
                    Collect data and estimate free energy differences
                    """, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-t', dest='t', type=float, default='300.0', help="Temperature")
    parser.add_argument('-p', dest='pre', type=str, default='', help="File prefix")
    parser.add_argument('-s', dest='suffix', type=str, default='.xvg', help="File suffix")
    parser.add_argument('-e', dest='estimators', type=str, default=None, help="Comma separated Estimator methods")
    parser.add_argument('-u', dest='uncorrelator', type=str, default='statistical_ineffiency_dhdl', help="Data uncorrelation method")
    parser.add_argument('-o', dest='output', type=str, default=None, help="Output methods")
    parser.add_argument('-parser', dest='parser', type=str, default='gmx', help="Parser")
    args = parser.parse_args()

    parser = load_plugin('parser', args.parser, args.t, args.pre, args.suffix)
    uncorrelator = load_plugin('uncorrelate', args.uncorrelator)
    outputs = load_plugins('output', argsplit(args.output))
    estimators = load_plugins('estimator', argsplit(args.estimators))

    # Step 0: Check what data the selected estimators need
    do_dhdl = False
    do_uks = False
    for estimator in estimators:
        if estimator.needs_dhdls:
            do_dhdl = True
        if estimator.needs_uks:
            do_uks = True

    # Step 1: Read the necessary data
    dhdls = None
    uks = None
    if do_dhdl:
        dhdls = parser.get_dhdls()
    if do_uks:
        uks = parser.get_uks()

    # Step 2: Uncorrelate the data
    if uncorrelator.needs_dhdls:
        uncorrelator.set_dhdls(dhdls)
    if uncorrelator.needs_uks:
        uncorrelator.set_uks(uks)

    ls = None
    if do_dhdl:
        dhdls, ls = uncorrelator.uncorrelate(dhdls)
    if do_uks:
        uks, ls = uncorrelator.uncorrelate(uks)

    # Step 3: Estimate Free energy differences
    dfs = []
    ddfs = []

    for estimator in estimators:
        if estimator.needs_dhdls:
            estimator.set_dhdls(dhdls)
        if estimator.needs_uks:
            estimator.set_uks(uks)
        df, ddf = estimator.estimate()
        dfs.append(df)
        ddfs.append(ddf)

    # Step 4: Output
    for output in outputs:
        output.output(estimators, dfs, ddfs, args.t, ls)


main()
