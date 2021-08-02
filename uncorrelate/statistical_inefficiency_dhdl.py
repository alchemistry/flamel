import alchemlyb.preprocessing
import pandas
import numpy as np
from warnings import warn


# Todo: Use interface here
class StatisticalInefficiencyDhdl:
    name = 'dhdl'

    needs_dhdls = True
    needs_u_nks = False

    dhdl = None
    uncorr_threshold = None

    def __init__(self, uncorr_threshold):
        self.uncorr_threshold = uncorr_threshold

    def set_dhdls(self, dhdls):
        """
        :param dhdls: Series
            List of dH/dl values
        :return:
        """
        self.dhdls = dhdls

    def uncorrelate(self, dfs, lower):
        """
        :param dfs: Series
            List of data to uncorrelate
        :return: Dataframe
            uncorrelated Dataframe of `dfs`
        """
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
        print("Number of correlated and uncorrelated samples (Method=dHdl (all)):")
        print("\n State            N          N_k        N/N_k\n")
        for idx, (dhdl_, l, df) in enumerate(zip(self.dhdls, dl, dfs)):
            ind = np.array(l, dtype=bool)
            ind = np.array(ind, dtype=int)
            dhdl_sum = dhdl_.dot(ind)
            uncorrelated_df = alchemlyb.preprocessing.statistical_inefficiency(df, dhdl_sum, lower, conservative=False)
            N, N_k = len(df), len(uncorrelated_df)
            g = N/N_k
            print(f"{idx:>6} {N:>12} {N_k:>12} {g:>12.2f}")
            if N_k < self.uncorr_threshold:
                warn(f"Only {N_k} uncorrelated samples found at lambda number {idx}; proceeding with analysis using correlated samples...")
                uncorrelated_dfs.append(df)
            else:
                uncorrelated_dfs.append(uncorrelated_df)

        return uncorrelated_dfs


def get_plugin(*args):
    """
    :param args:
    :return:
        Statitical inefficiency uncorrelator
    """
    return StatisticalInefficiencyDhdl(*args)
