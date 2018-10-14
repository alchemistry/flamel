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

        for fname in files:
            print('Read %s' % fname)
            dhdl_ = alchemlyb.parsing.gmx.extract_dHdl(fname, self.T)
            dhdls_.append(dhdl_)

        return dhdls_

    def get_uks(self):
        files = self.get_files()
        uks_ = []

        for fname in files:
            print('Read %s' % fname)

            uk = alchemlyb.parsing.gmx.extract_u_nk(fname, self.T)

            uk_ = uk.copy()
            uks_.append(uk_)

        return uks_


def get_plugin(*args):
    return Gmx(*args)
