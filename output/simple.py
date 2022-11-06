import alchemlyb.postprocessors.units as units

class Simple:
    name = 'simple'

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

        for estimator in estimators:
            df = units.get_unit_converter(args.unit)(estimator.delta_f)
            ddf = units.get_unit_converter(args.unit)(estimator.d_delta_f)

            dfv = df.values[0, -1]
            ddfv = ddf.values[0, -1]
            print("%s: %f +- %f" % (estimator.name, dfv, ddfv))


def get_plugin():
    """
    Get simple output plugin
    :return:
        simple output plugin
    """
    return Simple()
