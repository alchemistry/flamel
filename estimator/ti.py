import alchemlyb.estimators


# Todo: Use an interface here...
class Ti:
    needs_dhdls = True
    needs_uks = False

    dhdls = None
    uks = None

    def set_dhdls(self, dhdls):
        self.dhdls = dhdls

    def estimate(self):
        ti_est = alchemlyb.estimators.ti_.TI()
        ti_est.fit(self.dhdls)

        # Todo: Think about what data format we want to use here (current: DataFrame)
        return ti_est.delta_f_, ti_est.d_delta_f_


def get_plugin():
    return Ti()
