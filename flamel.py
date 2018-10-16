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
        return ['ti', 'mbar', 'ti_cubic']
    if type == 'uncorrelate':
        return ['statistical_inefficiency_dhdl']
    if type == 'output':
        return ['simple', 'alchemical_analysis']


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
    parser.add_argument('-t', dest='t', type=float, default='300.0', help="Temperature")
    parser.add_argument('-p', dest='pre', type=str, default='dhdl', help="File prefix")
    parser.add_argument('-s', dest='suffix', type=str, default='xvg', help="File suffix")
    parser.add_argument('-e', dest='estimators', type=str, default=None, help="Comma separated Estimator methods")
    parser.add_argument('-u', dest='uncorrelator', type=str, default='dhdl', help="Data uncorrelation method")
    parser.add_argument('-o', dest='output', type=str, default=None, help="Output methods")
    parser.add_argument('-parser', dest='parser', type=str, default='gmx', help="Parser")
    args = parser.parse_args()

    parser = load_plugin('parser', args.parser, args.t, args.pre, args.suffix)
    uncorrelator = load_plugin_by_name('uncorrelate', args.uncorrelator)
    outputs = load_plugins('output', argsplit(args.output))
    estimators = load_plugins('estimator', argsplit(args.estimators))

    # Step 0: Check what data the uncorrelator and the selected estimators need
    do_dhdl = uncorrelator.needs_dhdls
    do_u_nks = uncorrelator.needs_uks
    for estimator in estimators:
        if estimator.needs_dhdls:
            do_dhdl = True
        if estimator.needs_uks:
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
    if uncorrelator.needs_uks:
        uncorrelator.set_u_nks(u_nks)

    ls = None
    if do_dhdl:
        dhdls, ls = uncorrelator.uncorrelate(dhdls)
    if do_u_nks:
        u_nks, ls = uncorrelator.uncorrelate(u_nks)

    # Step 3: Estimate Free energy differences
    for estimator in estimators:
        if estimator.needs_dhdls:
            estimator.set_dhdls(dhdls)
        if estimator.needs_uks:
            estimator.set_u_nks(u_nks)
        estimator.estimate()

    # Step 4: Output
    for output in outputs:
        output.output(estimators, args.t, ls)


main()
