import alchemlyb.preprocessing
import pandas
import numpy as np


# Todo: Use interface here
class StatisticalIneffiencyDhdl:
    needs_dhdls = True
    needs_uks = False

    dhdl = None

    def set_dhdls(self, dhdls):
        self.dhdls = dhdls

    def uncorrelate(self, dfs):
        l_values_ = []

        for dhdl_ in self.dhdls:
            if len(dhdl_.columns) == 1:
                l_values_.append(list([dhdl_.xs(0, level=0).index.values[0]]))
            else:
                l_values_.append(list(dhdl_.xs(0, level=0).index.values[0]))

        dl = []
        for i, l in enumerate(l_values_):
            dli = []
            for j, lij in enumerate(l):
                dlij = False
                if i < len(l_values_) - 1:
                    if l_values_[i+1][j] != lij:
                        dlij = True
                if i > 0:
                    if l_values_[i - 1][j] != lij:
                        dlij = True
                dli.append(dlij)
            dl.append(dli)

        uncorrelated_dfs = []
        for dhdl_, l, df in zip(self.dhdls, dl, dfs):
            ind = np.array(l, dtype=bool)
            ind = np.array(ind, dtype=int)
            dhdl_sum = dhdl_.dot(ind)
            uncorrelated_dfs.append(alchemlyb.preprocessing.statistical_inefficiency(df, dhdl_sum, conservative=False))

        return pandas.concat(uncorrelated_dfs), l_values_


def get_plugin(*args):
    return StatisticalIneffiencyDhdl()