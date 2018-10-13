import alchemlyb.estimators
import alchemlyb.preprocessing


# Todo: Use an interface here...
class Mbar:
    name = 'MBAR'
    needs_dhdls = False
    needs_uks = True

    dhdls = None
    uks = None

    def set_uks(self, uks):
        self.uks = uks

    def estimate(self):
        mbar_est = alchemlyb.estimators.mbar_.MBAR()
        mbar_est.fit(self.uks)

        # Todo: Think about what data format we want to use here (current: DataFrame)
        return mbar_est.delta_f_, mbar_est.d_delta_f_


def get_plugin():
    return Mbar()
