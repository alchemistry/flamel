import alchemlyb.preprocessing
import pandas
import numpy as np
import pickle
import time
import os

class Pickle:
    name = 'pickle'
    k_b = 8.3144621E-3
    
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

    def output(self,  estimators, args):
        
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
        
        P = args
        
        P.datafile_directory = os.getcwd()
        P.when_analyzed = time.asctime()
        P.dFs = {}
        P.ddFs = {}
        P.dF = {}
        
        segments = self.segments(estimators)
        
        for estimator in estimators:
            
            data = {}
            
            df = estimator.delta_f
            ddf = estimator.d_delta_f
            
            for segstart, segend, l_name in reversed(segments):
                data[l_name] = (df.values[segstart, segend], ddf.values[segstart, segend])
            
            data['total'] = (df.values[0, -1], ddf.values[0, -1])
                
            P.dFs[estimator.name] = df
            P.ddFs[estimator.name] = ddf

            P.dF[estimator.name] = data
        
        pickle.dump(P,open(args.resultfilename + '.pickle','wb'))


def get_plugin():
    """
    Get simple output plugin
    :return:
        simple output plugin
    """
    return Pickle()
