import alchemlyb.preprocessing
import pandas
import numpy as np


class Simple:
    dfs = None
    ddfs = None
    estimators = None
    t = None
    k_b = 8.3144621E-3

    def output(self,  estimators, t, ls):
        """
        Print a simple output.
        :param estimators: Series
            Series of estimators
        :param t: float
            temperature in K
        :param ls: Series
            Lambdas
        :return:
        """
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
