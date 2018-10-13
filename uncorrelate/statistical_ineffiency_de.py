import alchemlyb.preprocessing
import pandas
import numpy as np


# Todo: Use interface here
class StatisticalIneffiencyUks:
    needs_dhdls = False
    needs_uks = True

    uks = None

    def set_uks(self, uks):
        self.uks = uks

    def uncorrelate(self, dfs):
        l_values_ = []

        for uk_ in self.uks:
            l_values_.append(list(uk_.xs(0, level=0).index.values[0]))

        i = 0
        uncorrelated_dfs = []
        for uk, df in zip(self.uks, dfs):
            if i + 1 < len(self.uks):
                s = uk.iloc[:, 0:i + 2]
            else:
                s = uk.iloc[:, 0:i]

            uncorrelated_dfs.append(alchemlyb.preprocessing.statistical_inefficiency(df, s, conservative=False))
            i += 1

        return pandas.concat(uncorrelated_dfs), l_values_


def get_plugin(*args):
    return StatisticalIneffiencyUks()
