import alchemlyb.preprocessing
import pandas
import numpy as np


# Todo: Use interface here
class StatisticalInefficiencyDhdlAll:
    name = 'dhdl_all'

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

        uncorrelated_dfs = []
        print("Number of correlated and uncorrelated samples (Method=dHdl (all)):")
        print("\n State            N          N_k        N/N_k\n")
        for idx, (dhdl_, df) in enumerate(zip(self.dhdls, dfs)):
            dhdl_sum = dhdl_.sum(axis=1)
            uncorrelated_df = alchemlyb.preprocessing.statistical_inefficiency(df, dhdl_sum, lower, conservative=False)
            N, N_k = len(df), len(uncorrelated_df)
            g = N/N_k
            print(f"{idx:>6} {N:>12} {N_k:>12} {g:>12.2f}")
            if N_k < self.uncorr_threshold:
                print(f"WARNING: Only {N_k} uncorrelated samples found at lambda number {idx}; proceeding with analysis using correlated samples...")
                uncorrelated_dfs.append(df)
            else:
                uncorrelated_dfs.append(uncorrelated_df)

        return uncorrelated_dfs


def get_plugin(*args):
    """
    :param args:
    :return:
        Statitical inefficiency uncorrelator using a sum of all dhdls
    """
    return StatisticalInefficiencyDhdlAll(*args)
