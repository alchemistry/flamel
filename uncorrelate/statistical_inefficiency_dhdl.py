import alchemlyb.preprocessing
import pandas
import numpy as np
from uncorrelate.statistical_inefficiency import StatisticalInefficiency


class StatisticalInefficiencyDhdl(StatisticalInefficiency):
    name = 'dhdl'

    needs_dhdls = True
    needs_u_nks = False

    dhdl = None

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
        print(f"Number of correlated and uncorrelated samples (Method={self.name}):")
        print("\n State            N          N_k        N/N_k\n")
        for idx, (dhdl_, l, df) in enumerate(zip(self.dhdls, dl, dfs)):
            ind = np.array(l, dtype=bool)
            ind = np.array(ind, dtype=int)
            dhdl_sum = dhdl_.dot(ind)
            uncorrelated_df = alchemlyb.preprocessing.statistical_inefficiency(df, dhdl_sum, lower, conservative=False)
            if self.check_sample_size(idx, df, uncorrelated_df):
                uncorrelated_dfs.append(uncorrelated_df)
            else:
                uncorrelated_dfs.append(df)
            
        return uncorrelated_dfs


def get_plugin(*args):
    """
    :param args:
    :return:
        Statitical inefficiency uncorrelator
    """
    return StatisticalInefficiencyDhdl(*args)
