import numpy as np
import time
import os

class Text:
    name = 'text'
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
        """
        Collect and prepare values from different `estimators` into a series of values.
         :param estimators: Series
            List of estimator plugins
        :return:
            Segments of values to output
        """
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

    @classmethod
    def prepare_value(cls, value, decimal):
        """
        Convert `value` to a str with `decimal` precision.
        :param value: float
            Value to convert
        :param decimal:
            Precision
        :return: str
            str of `value` with `decimal` precision
        """
        value_str = str(round(value, decimal))
        if np.isnan(value):
            return str(value) + ' '*(decimal - 1)
        return value_str + '0'*(decimal - len(value_str.split('.')[1]))

    def output(self,  estimators, args):
        """
        Print a alchemical-analysis like output.
        :param estimators: Series
            Series of estimators
        :param args: argparse obj
            arguments from argparse
        :param ls: Series
            Lambdas
        :return:
        """
        t = args.temperature

        if args.unit == 'kT':
            conversion = 1.0
            args.unit = 'kT'
        elif args.unit == 'kJ' or args.unit == 'kJ/mol':
            conversion = 1.0 / (t * self.k_b)
            args.unit = 'kJ/mol'
        elif args.unit == 'kcal' or args.unit == 'kcal/mol':
            conversion = 0.239006 / (t * self.k_b)
            args.unit = 'kcal/mol'
        
        seglen = 2 * args.decimal + 15
        out = ''
        segments = self.segments(estimators)
        
        out += "Free Energy analysis; Text output from flamel.py invoked at: " + time.asctime()
        
        out += os.getcwd()
        
        # First ----
        out += self.lenc('-'*12, 12)
        for _ in estimators:
            out += self.lenc('-'*seglen)
        out += "\n"

        # Labels
        out += self.lenc('States', 12)
        for estimator in estimators:
            out += self.lenr(estimator.name + ' (' + args.unit + ')' + ' '*args.decimal, seglen)
        out += "\n"

        # Second ----
        out += self.lenc('-'*12, 12)
        for _ in estimators:
            out += self.lenc('-'*seglen)
        out += "\n"

        # Free Energy differences for each lambda state
        for i, l in enumerate(self.ls(estimators)[:-1]):
            out += self.lenc(str(i) + ' -- ' + str(i+1), 12)

            for estimator in estimators:
                df = estimator.delta_f
                ddf = estimator.d_delta_f
                out += self.lenr('%s  +-  %s' % (
                    self.prepare_value(df.values[i, i+1] * conversion, args.decimal),
                    self.prepare_value(ddf.values[i, i+1] * conversion, args.decimal)
                ), seglen)
            out += "\n"

        # Third ----
        out += self.lenc('-'*12, 12)
        for _ in estimators:
            out += self.lenc('-'*seglen)
        out += "\n"

        for segstart, segend, l_name in reversed(segments):
            # Segment Energies
            out += self.lenr('%s:  ' % l_name[:-7], 12)
            for estimator in estimators:
                df = estimator.delta_f
                ddf = estimator.d_delta_f
                out += self.lenr('%s  +-  %s' % (
                    self.prepare_value(df.values[segstart, segend] * conversion, args.decimal),
                    self.prepare_value(ddf.values[segstart, segend] * conversion, args.decimal)
                ), seglen)
            out += "\n"

        # TOTAL Energies
        out += self.lenr('TOTAL:  ', 12)
        for estimator in estimators:
            df = estimator.delta_f
            ddf = estimator.d_delta_f
            out += self.lenr('%s  +-  %s' % (
                self.prepare_value(df.values[0, -1] * conversion, args.decimal),
                self.prepare_value(ddf.values[0, -1] * conversion, args.decimal)
            ), seglen)
        out += "\n"

        txt_file = open(args.resultfilename+'.txt','w')
        txt_file.write(out)
        txt_file.close()


def get_plugin():
    """
    Get Alchemical analysis output plugin
    :return:
        Alchemical analysis output plugin
    """
    return Text()
