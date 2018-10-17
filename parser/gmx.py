import os
import alchemlyb.parsing.gmx
import alchemlyb.preprocessing


# Todo: Use an interface here...
class Gmx:
    name = 'Gromacs'
    dhdls = None
    uks = None
    T = 300.0
    prefix = ''
    suffix = 'xvg'

    def __init__(self, T, prefix, suffix):
        """
        :param T: float
            Temperature in K
        :param prefix: str
            File prefix
        :param suffix: str
            File suffix
        """
        self.T = T
        self.prefix = prefix
        self.suffix = suffix

    def get_files(self):
        """
        Get a list of files with the given prefix and suffix
        :return: Series
            The list of files
        """
        ls = os.listdir()

        # Build a list of tuples with name and a number
        files = []
        for f in ls:
            if f[0:len(self.prefix)] == self.prefix and f[-len(self.suffix):] == self.suffix:
                name = f[len(self.prefix):-len(self.suffix)]
                num = int(''.join([c for c in name if c.isdigit()]))
                files.append((f, num))

        # Sort the list by of tuples by the number
        sorted_files = sorted(files, key=lambda tup: tup[1])

        # Return only the file names
        return [f[0] for f in sorted_files]

    def get_dhdls(self):
        """
        Read dH/dl values from files
        :return: Series
            List of dH/dl data frames
        """
        files = self.get_files()
        dhdls_ = []

        for fname in files:
            print('Read %s' % fname)
            dhdl_ = alchemlyb.parsing.gmx.extract_dHdl(fname, self.T)
            dhdls_.append(dhdl_)

        return dhdls_

    def get_u_nks(self):
        """
        Read u_nk values from files
        :return:
            List of u_nk data frames
        """
        files = self.get_files()
        uks_ = []

        for fname in files:
            print('Read %s' % fname)

            uk = alchemlyb.parsing.gmx.extract_u_nk(fname, self.T)

            uk_ = uk.copy()
            uks_.append(uk_)

        return uks_


def get_plugin(*args):
    """
    Get the GMX parser plugin
    :param T: float
        Temperature in K
    :param prefix: str
        File prefix
    :param suffix: str
        File suffix
    :return: Parser
        The GMX parser
    """
    return Gmx(*args)
