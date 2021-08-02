import alchemlyb.preprocessing
import pandas
import numpy as np
from uncorrelate.statistical_inefficiency import StatisticalInefficiency


class StatisticalInefficiencyDhdlAll(StatisticalInefficiency):
    name = 'dhdl_all'

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

        uncorrelated_dfs = []
        print(f"Number of correlated and uncorrelated samples (Method=f{self.name}):")
        print("\n State            N          N_k        N/N_k\n")
        for idx, (dhdl_, df) in enumerate(zip(self.dhdls, dfs)):
            dhdl_sum = dhdl_.sum(axis=1)
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
        Statitical inefficiency uncorrelator using a sum of all dhdls
    """
    return StatisticalInefficiencyDhdlAll(*args)
