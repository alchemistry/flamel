import alchemlyb.preprocessing
import pandas
import numpy as np


class Simple:
    dfs = None
    ddfs = None
    estimators = None
    t = None
    k_b = 8.3144621E-3

    def output(self,  estimators, dfs, ddfs, t, ls):
        for estimator, df, ddf in zip(estimators, dfs, ddfs):
            print(estimator.name)

            beta = 1.0 / t / self.k_b
            print(df.values[0, -1] / beta)
            print(ddf.values[0, -1] / beta)


def get_plugin(*args):
    return Simple()