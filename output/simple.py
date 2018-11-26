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
        for estimator in estimators:
            df = estimator.delta_f
            ddf = estimator.d_delta_f
            beta = 1.0 / t / self.k_b
            dfv = df.values[0, -1] / beta
            ddfv = ddf.values[0, -1] / beta
            print("%s: %f +- %f" % (estimator.name, dfv, ddfv))


def get_plugin():
    """
    Get simple output plugin
    :return:
        simple output plugin
    """
    return Simple()
