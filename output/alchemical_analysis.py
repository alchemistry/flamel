import numpy as np


class AlchemicalAnalysis:
    name = 'alchemical-analysis'
    k_b = 8.3144621E-3

    @classmethod
    def lenr(cls, text, l=21):
        """
        Right aligned text in a string with length `l`
        :param text: str
            The text to align
        :param l: int
            desired length
        :return: str
            aligned text
        """
        return ' '*(l - len(text)) + text + ' '

    @classmethod
    def lenc(cls, text, l=21):
        """
        Center text in a string with length `l`
        :param text: str
            The text to center
        :param l: int
            desired length
        :return: str
            centered text
        """
        lr = int((l - len(text)) / 2)
        ll = l - len(text) - lr
        return ' '*ll + text + ' '*lr + ' '

    @classmethod
    def ls(cls, estimators):
        """
        Return a list of lambda values
        :param estimators: Series
            List of estimator plugins
        :return:
            The list of lambda values
        """
        ls = []
        if estimators:
            if estimators[0].needs_dhdls:
                means = estimators[0].dhdls.mean(level=estimators[0].dhdls.index.names[1:])
                ls = np.array(means.reset_index()[means.index.names[:]])
            elif estimators[0].needs_u_nks:
                means = estimators[0].u_nks.mean(level=estimators[0].u_nks.index.names[1:])
                ls = np.array(means.reset_index()[means.index.names[:]])

        return ls

    @classmethod
    def l_types(cls, estimators):
        """
        Return a list of lambda types
        :param estimators: Series
            List of estimator plugins
        :return:
            The list of lambda types
        """
        l_types = []
        if estimators:
            if estimators[0].needs_dhdls:
                l_types = estimators[0].dhdls.index.names[1:]
            elif estimators[0].needs_u_nks:
                l_types = estimators[0].u_nks.index.names[1:]

        return l_types

    @classmethod
    def segments(cls, estimators):
        segments = []
        l_types = cls.l_types(estimators)
        ls = cls.ls(estimators)
        if estimators:
            segstart = 0
            ill = [0] * len(l_types)
            nl = 0
            for i in range(len(ls)):
                l = ls[i]
                if (i < len(ls) - 1 and list(np.array(ls[i + 1], dtype=bool)).count(True) > nl) or i == len(ls) - 1:
                    if nl > 0:
                        inl = np.array(np.array(l, dtype=bool), dtype=int)
                        l_name = l_types[list(inl - ill).index(1)]
                        ill = inl
                        segments.append((segstart, i, l_name))

                    if i + 1 < len(ls):
                        nl = list(np.array(ls[i + 1], dtype=bool)).count(True)
                    segstart = i
        return segments

    def output(self,  estimators, t):
        """
        Print a alchemical-analysis like output.
        :param estimators: Series
            Series of estimators
        :param t: float
            temperature in K
        :param ls: Series
            Lambdas
        :return:
        """
        beta = 1.0 / t / self.k_b
        out = ''
        segments = self.segments(estimators)

        # First ----
        out += self.lenc('-'*12, 12)
        for _ in estimators:
            out += self.lenc('-'*21)
        out += "\n"

        # Labels
        out += self.lenc('States', 12)
        for estimator in estimators:
            out += self.lenr(estimator.name + ' (kJ/mol)   ')
        out += "\n"

        # Second ----
        out += self.lenc('-'*12, 12)
        for _ in estimators:
            out += self.lenc('-'*21)
        out += "\n"

        # Free Energy differences for each lambda state
        for i, l in enumerate(self.ls(estimators)[:-1]):
            out += self.lenc(str(i) + ' -- ' + str(i+1), 12)

            for estimator in estimators:
                df = estimator.delta_f
                ddf = estimator.d_delta_f
                out += self.lenr('%0.3f  +-  %0.3f' % (df.values[i, i+1] / beta, ddf.values[i, i+1] / beta))
            out += "\n"

        # Third ----
        out += self.lenc('-'*12, 12)
        for _ in estimators:
            out += self.lenc('-'*21)
        out += "\n"

        for segstart, segend, l_name in reversed(segments):
            # Segment Energies
            out += self.lenr('%s:  ' % l_name[:-7], 12)
            for estimator in estimators:
                df = estimator.delta_f
                ddf = estimator.d_delta_f
                out += self.lenr('%0.3f  +-  %0.3f' % (df.values[segstart, segend] / beta, ddf.values[segstart, segend] / beta))
            out += "\n"

        # TOTAL Energies
        out += self.lenr('TOTAL:  ', 12)
        for estimator in estimators:
            df = estimator.delta_f
            ddf = estimator.d_delta_f
            out += self.lenr('%0.3f  +-  %0.3f' % (df.values[0, -1] / beta, ddf.values[0, -1] / beta))
        out += "\n"

        print(out)


def get_plugin():
    """
    Get Alchemical analysis output plugin
    :return:
        Alchemical analysis output plugin
    """
    return AlchemicalAnalysis()
