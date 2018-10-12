import os
import alchemlyb.parsing.gmx
import alchemlyb.preprocessing
import pandas
import numpy as np


# Todo: Use an interface here...
class Gmx:
    dhdls = None
    uks = None
    T = 300.0
    pre = ''
    post = '.xvg'

    def __init__(self, T, pre, post):
        self.T = T
        self.pre = pre
        self.post = post

    def get_files(self):
        ls = os.listdir()

        files = []
        for f in ls:
            if f[0:len(self.pre)] == self.pre and f[-len(self.post):] == self.post:
                files.append(int(f[len(self.pre):-len(self.post)]))

        nums = sorted(files)

        sorted_files = list(map(lambda x: self.pre + str(x) + self.post, nums))

        return sorted_files

    def get_dhdls(self):
        files = self.get_files()
        dhdls_ = []
        l_values_ = []

        for fname in files:
            print('Read %s' % fname)
            dhdl_ = alchemlyb.parsing.gmx.extract_dHdl(fname, self.T)
            dhdls_.append(dhdl_)
            l_values_.append(list(dhdl_.xs(0, level=0).index.values[0]))

        dl = np.gradient(np.array(l_values_))[0]

        uncorrelated_dhdls = []
        for dhdl_, l in zip(dhdls_, dl):
            ind = np.array(l, dtype=bool)
            ind = np.array(ind, dtype=int)
            dhdl_sum = dhdl_.dot(ind)
            uncorrelated_dhdls.append(alchemlyb.preprocessing.statistical_inefficiency(dhdl_, dhdl_sum, conservative=False))

        return pandas.concat(uncorrelated_dhdls)
            dhdls_.append(dhdl_)



def get_plugin(*args):
    return Gmx(*args)
