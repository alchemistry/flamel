import alchemlyb.preprocessing
import pandas
import numpy as np


# Todo: Use interface here
class StatisticalInefficiencyDhdlAll:
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
        for dhdl_, df in zip(self.dhdls, dfs):
            dhdl_sum = dhdl_.sum(axis=1)
            uncorrelated_dfs.append(alchemlyb.preprocessing.statistical_inefficiency(df, dhdl_sum, lower, conservative=False))

        uncorrelated_df = pandas.concat(uncorrelated_dfs)
        uncorrelated_df.attrs = uncorrelated_dfs[0].attrs
        return uncorrelated_df


def get_plugin(*args):
    """
    :param args:
    :return:
        Statitical inefficiency uncorrelator using a sum of all dhdls
    """
    return StatisticalInefficiencyDhdlAll()
