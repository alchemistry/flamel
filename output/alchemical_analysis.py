import numpy as np


class AlchemicalAnalysis:
    dfs = None
    ddfs = None
    estimators = None
    t = None
    k_b = 8.3144621E-3

    def lenr(self, text, l=21):
        return ' '*(l - len(text)) + text + ' '

    def lenc(self, text, l=21):
        lr = int((l - len(text)) / 2)
        ll = l - len(text) - lr
        return ' '*ll + text + ' '*lr + ' '

    def output(self,  estimators, dfs, ddfs, t, ls):
        beta = 1.0 / t / self.k_b
        out = ''

        out += self.lenc('-'*12, 12)
        for _ in estimators:
            out += self.lenc('-'*21)
        out += "\n"

        out += self.lenc('States', 12)
        for estimator in estimators:
            out += self.lenr(estimator.name + ' (kJ/mol)   ')
        out += "\n"
        out += self.lenc('-'*12, 12)
        for _ in estimators:
            out += self.lenc('-'*21)
        out += "\n"

        dls = np.gradient(np.array(ls))[0][:-1]

        for i, l in enumerate(dls):
            out += self.lenc(str(i) + ' -- ' + str(i+1), 12)

            for estimator, df, ddf in zip(estimators, dfs, ddfs):
                out += self.lenr('%0.3f  +-  %0.3f' % (df.values[i, i+1] / beta, ddf.values[i, i+1] / beta))
            out += "\n"

        out += self.lenc('-'*12, 12)
        for _ in estimators:
            out += self.lenc('-'*21)
        out += "\n"

        out += self.lenr('TOTAL:  ', 12)
        for df, ddf in zip(dfs, ddfs):
            out += self.lenr('%0.3f  +-  %0.3f' % (df.values[0, -1] / beta, ddf.values[0, -1] / beta))
        out += "\n"

        print(out)


def get_plugin(*args):
    return AlchemicalAnalysis()