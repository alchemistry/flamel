from abc import ABC, abstractmethod
from warnings import warn

class StatisticalInefficiency(ABC):

    uncorr_threshold = None

    def __init__(self, uncorr_threshold):
        self.uncorr_threshold = uncorr_threshold

    def check_sample_size(self, idx, df, uncorrelated_df):
        N, N_k = len(df), len(uncorrelated_df)
        g = N/N_k
        print(f"{idx:>6} {N:>12} {N_k:>12} {g:>12.2f}")
        if N_k < self.uncorr_threshold:
            warn(f"Only {N_k} uncorrelated samples found at lambda number {idx}; proceeding with analysis using correlated samples...")
            return False
        return True

    @abstractmethod
    def uncorrelate(self, dfs, lower):
        pass
