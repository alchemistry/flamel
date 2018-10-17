#!/usr/bin/env python

import argparse


def get_available_plugin_ids(type):
    """
    Get a list of available plugins of a cetrain type
    :param type: str
        Type of the plugin
    :return: Series
        List of available plugin names
    """
    # Todo: Implement this

    if type == 'estimator':
        return ['ti', 'ti_cubic', 'mbar']
    if type == 'uncorrelate':
        return ['statistical_inefficiency_dhdl']
    if type == 'output':
        return ['simple', 'alchemical_analysis']
    if type == 'parser':
        return ['gmx']


def load_plugin_by_name(type, name, *args):
    """
    Load a plugin by its name
    :param type: str
        Plugin type
    :param name: str
        Plugin name
    :param args:
        Args passed to the plugin
    :return:
        The plugin
    """
    return load_plugins(type, [name], *args)[0]


def load_plugin(type, id, *args):
    """
    Load a specific plugin
    :param type: str
        Type of the plugin
    :param id: str
        Name of the plugin
    :param args:
        Args passed to the plugin
    :return:
        The plugin
    """
    # Todo: think about a suitable plugin system
    mod = __import__("%s.%s" % (type, id), fromlist=['object'])
    return mod.get_plugin(*args)


def argsplit(arg):
    """
    Helper method to split a comma separated string to a list
    :param arg: str
        Input string
    :return: Series
        List of sections in the string
    """
    return [] if arg is None else arg.split(',')


def load_plugins(type, selected, *args):
    """
    Load multiple plugins
    :param type:
        Type of the plugins to load
    :param selected:
        List of selected plugins - if empty every available plugin will be used
    :return: Series
        The list of plugins
    """
    available = get_available_plugin_ids(type)
    plugins = []
    for plugin_id in available:
        plugin = load_plugin(type, plugin_id, *args)
        if selected:
            if plugin.name in selected:
                plugins.append(plugin)
        else:
            plugins.append(plugin)

    return plugins


def main():
    parser = argparse.ArgumentParser(description="""
                    Collect data and estimate free energy differences
                    """, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-t', '--temperature', dest='temperature', help="Temperature in K. Default: 298 K.", default=298.0, type=float)
    parser.add_argument('-p', '--prefix', dest='prefix', help='Prefix for datafile sets, i.e.\'dhdl\' (default).', default='dhdl')
    parser.add_argument('-q', '--suffix', dest='suffix', help='Suffix for datafile sets, i.e. \'xvg\' (default).', default='xvg')
    parser.add_argument('-e', dest='estimators', type=str, default=None, help="Comma separated Estimator methods")
    parser.add_argument('-n', '--uncorr', dest='uncorr', help='The observable to be used for the autocorrelation analysis; either \'dhdl_all\' (obtained as a sum over all energy components) or \'dhdl\' (obtained as a sum over those energy components that are changing; default) or \'dE\'. In the latter case the energy differences dE_{i,i+1} (dE_{i,i-1} for the last lambda) are used.', default='dhdl')
    parser.add_argument('-o', '--output', dest='output', type=str, default=None, help="Output methods")
    parser.add_argument('-a', '--software', dest='software', help='Package\'s name the data files come from: Gromacs, Sire, Desmond, or AMBER. Default: Gromacs.', default='Gromacs')
    parser.add_argument('-s', '--skiptime', dest='equiltime', help='Discard data prior to this specified time as \'equilibration\' data. Units picoseconds. Default: 0 ps.', default=0, type=float)
    args = parser.parse_args()

    parser = load_plugin_by_name('parser', args.software, args.temperature, args.prefix, args.suffix)
    uncorrelator = load_plugin_by_name('uncorrelate', args.uncorr)
    outputs = load_plugins('output', argsplit(args.output))
    estimators = load_plugins('estimator', argsplit(args.estimators))

    # Step 0: Check what data the uncorrelator and the selected estimators need
    do_dhdl = uncorrelator.needs_dhdls
    do_u_nks = uncorrelator.needs_u_nks
    for estimator in estimators:
        if estimator.needs_dhdls:
            do_dhdl = True
        if estimator.needs_u_nks:
            do_u_nks = True

    # Step 1: Read the necessary data
    dhdls = None
    u_nks = None
    if do_dhdl:
        dhdls = parser.get_dhdls()
    if do_u_nks:
        u_nks = parser.get_u_nks()

    # Step 2: Uncorrelate the data
    if uncorrelator.needs_dhdls:
        uncorrelator.set_dhdls(dhdls)
    if uncorrelator.needs_u_nks:
        uncorrelator.set_u_nks(u_nks)

    if do_dhdl:
        dhdls = uncorrelator.uncorrelate(dhdls, args.equiltime)
    if do_u_nks:
        u_nks = uncorrelator.uncorrelate(u_nks, args.equiltime)

    # Step 3: Estimate Free energy differences
    for estimator in estimators:
        if estimator.needs_dhdls:
            estimator.set_dhdls(dhdls)
        if estimator.needs_u_nks:
            estimator.set_u_nks(u_nks)
        estimator.estimate()

    # Step 4: Output
    for output in outputs:
        output.output(estimators, args.temperature)


main()
