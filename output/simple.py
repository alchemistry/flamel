import alchemlyb.preprocessing
import pandas
import numpy as np


class Simple:
    name = 'simple'
    k_b = 8.3144621E-3

    def output(self,  estimators, args):
        """
        Print a alchemical-analysis like output.
        :param estimators: Series
            Series of estimators
        :param args: argparse obj
            arguments from argparse
        :param ls: Series
            Lambdas
        :return:
        """
        t = args.temperature

        if args.unit == 'kT':
            conversion = 1.0
            args.unit = 'kT'
        elif args.unit == 'kJ' or args.unit == 'kJ/mol':
            conversion = 1.0 / (t * self.k_b)
            args.unit = 'kJ/mol'
        elif args.unit == 'kcal' or args.unit == 'kcal/mol':
            conversion = 0.239006 / (t * self.k_b)
            args.unit = 'kcal/mol'
        
        for estimator in estimators:
            df = estimator.delta_f
            ddf = estimator.d_delta_f
            
            dfv = df.values[0, -1] * conversion
            ddfv = ddf.values[0, -1] * conversion
            print("%s: %f +- %f" % (estimator.name, dfv, ddfv))


def get_plugin():
    """
    Get simple output plugin
    :return:
        simple output plugin
    """
    return Simple()
