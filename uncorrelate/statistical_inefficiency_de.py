import alchemlyb.preprocessing
import pandas


# Todo: Test this, correct this, documentation
class StatisticalInefficiencyUnks:
    name = 'dE'
    needs_dhdls = False
    needs_u_nks = True

    uks = None

    def set_u_nks(self, u_nks):
        self.uks = u_nks

    def uncorrelate(self, dfs, lower):
        l_values_ = []

        for uk_ in self.uks:
            l_values_.append(list(uk_.xs(0, level=0).index.values[0]))

        i = 0
        uncorrelated_dfs = []
        statinefs = []
        for uk, df in zip(self.uks, dfs):
            if i + 1 < len(self.uks):
                s = uk.iloc[:, 0:i + 2]
            else:
                s = uk.iloc[:, 0:i]

            uncorrelated_df, statinef = alchemlyb.preprocessing.statistical_inefficiency(df, s, lower, conservative=False)
            uncorrelated_dfs.append(uncorrelated_df)
            statinefs.append(statinef)
            i += 1

        return pandas.concat(uncorrelated_dfs)


def get_plugin(*args):
    return StatisticalInefficiencyUnks()
