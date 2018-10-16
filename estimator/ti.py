import alchemlyb.estimators


# Todo: Use an interface here...
class Ti:
    name = 'TI'
    needs_dhdls = True
    needs_u_nks = False

    dhdls = None
    u_nks = None

    delta_f = None
    d_delta_f = None

    def set_dhdls(self, dhdls):
        """
        Setter method for dH/dl values
        :param dhdls:
        :return:
        """
        self.dhdls = dhdls

    def estimate(self):
        """
        Estimate free energy differences using Trapezoid thermodynamic integration
        :return:
        """
        ti_est = alchemlyb.estimators.ti_.TI()
        ti_est.fit(self.dhdls)

        # Todo: Think about what data format we want to use here (current: DataFrame)
        self.delta_f, self.d_delta_f = ti_est.delta_f_, ti_est.d_delta_f_


def get_plugin():
    return Ti()
