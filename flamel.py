#!/usr/bin/env python

import argparse


def get_available_estimators():
    # Todo: Implement this

    return ['ti', 'mbar']


def load_plugin(type, name, *args):
    # Todo: think about a suitable plugin system
    mod = __import__("%s.%s" % (type, name), fromlist=['object'])
    return mod.get_plugin(*args)


def main():
    parser = argparse.ArgumentParser(description="""
                    Collect data and estimate free energy differences
                    """, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-t', dest='t', type=float, default='300.0', help="Temperature")
    parser.add_argument('-p', dest='pre', type=str, default='', help="File prefix")
    parser.add_argument('-s', dest='suffix', type=str, default='.xvg', help="File suffix")
    parser.add_argument('-e', dest='estimators', type=str, default=None, help="Comma separated Estimator methods")
    parser.add_argument('-parser', dest='parser', type=str, default='gmx', help="Parser")
    args = parser.parse_args()

    # Todo: Use parser interface
    parser = load_plugin('parser', args.parser, args.t, args.pre, args.suffix)

    estimators = []
    available_estimators = get_available_estimators()
    if args.estimators is not None:
        for estimator in args.estimators.split(','):
            if estimator in available_estimators:
                estimators.append(estimator)

    else:
        estimators = available_estimators

    # Todo: Use estimator interface
    for estimator in estimators:
        estimator_plugin = load_plugin('estimator', estimator)
        if estimator_plugin.needs_dhdls:
            estimator_plugin.set_dhdls(parser.get_dhdls())
        if estimator_plugin.needs_uks:
            estimator_plugin.set_uks(parser.get_uks())
        df, ddf = estimator_plugin.estimate()

        k_b = 8.3144621E-3
        beta = 1.0 / args.t / k_b
        print(df.values[0, -1] / beta)
        print(ddf.values[0, -1] / beta)

    # Todo: Implement output


main()
