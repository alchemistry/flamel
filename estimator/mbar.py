import alchemlyb.estimators
import alchemlyb.preprocessing


# Todo: Use an interface here...
class Mbar:
    name = 'MBAR'
    needs_dhdls = False
    needs_uks = True

    dhdls = None
    uks = None

    delta_f = None
    d_delta_f = None

    def set_u_nks(self, u_nks):
        """
        Setter method for u_nks
        :param u_nks: 
        :return: 
        """
        self.uks = u_nks

    def estimate(self):
        """
        Estimate free energy differences with MBAR
        :return:
        """
        mbar_est = alchemlyb.estimators.mbar_.MBAR()
        mbar_est.fit(self.uks)

        # Todo: Think about what data format we want to use here (current: DataFrame)
        self.delta_f, self.d_delta_f = mbar_est.delta_f_, mbar_est.d_delta_f_


def get_plugin():
    return Mbar()
