class AlchemicalAnalysis:
    k_b = 8.3144621E-3

    @classmethod
    def lenr(self, text, l=21):
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
    def lenc(self, text, l=21):
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

    def output(self,  estimators, t, ls):
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
        for i, l in enumerate(ls[:-1]):
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
