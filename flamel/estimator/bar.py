import alchemlyb.estimators
import alchemlyb.preprocessing


# Todo: Use an interface here...
class Bar:
    name = 'BAR'
    needs_dhdls = False
    needs_u_nks = True

    dhdls = None
    u_nks = None

    delta_f = None
    d_delta_f = None

    def set_u_nks(self, u_nks):
        """
        Setter method for u_nks
        :param u_nks: 
        :return: 
        """
        self.u_nks = u_nks

    def estimate(self):
        """
        Estimate free energy differences with BAR
        :return:
        """
        bar_est = alchemlyb.estimators.bar_.BAR()
        bar_est.fit(self.u_nks)

        # Todo: Think about what data format we want to use here (current: DataFrame)
        self.delta_f, self.d_delta_f = bar_est.delta_f_, bar_est.d_delta_f_


def get_plugin():
    return Bar()

#c29613d34ffafa133c3dc5a90a92ce3a84cbcd0c
#03649d469383a55c305c1daa55de7792c88a22d3
#2d3a3ffc3dcf66f311c5c03a8a3214c0d0158554
#d38701718853261c7667ca50fcbe16ec501310b2