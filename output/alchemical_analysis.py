import numpy as np


class AlchemicalAnalysis:
    dfs = None
    ddfs = None
    estimators = None
    t = None
    k_b = 8.3144621E-3

    def output(self,  estimators, dfs, ddfs, t, ls):
        beta = 1.0 / t / self.k_b
        out = ''


        for estimator in estimators:
            out += estimator.name + ' '

        out += "\n"

        dls = np.gradient(np.array(ls))[0][:-1]

        # print(len(dls))
        for i, l in enumerate(dls):
            out += str(i) + ' '
            out += str(l) + ' '

            for estimator, df, ddf in zip(estimators, dfs, ddfs):
                out += str(round(df.values[i, i+1] / beta, 3)) + ' +- '
                out += str(round(ddf.values[i, i+1] / beta, 3)) + ' '

            out += "\n"

        for df, ddf in zip(dfs, ddfs):
            out += str(round(df.values[0, -1] / beta, 3)) + ' +- '
            out += str(round(ddf.values[0, -1] / beta, 3)) + ' '

        out += "\n"

        print(out)


def get_plugin(*args):
    return AlchemicalAnalysis(*args)