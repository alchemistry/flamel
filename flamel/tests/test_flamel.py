"""
Unit and regression test for the flamel package.
"""

# Import package, test suite, and other packages as needed
import sys
import pathlib
import pickle

import pytest
from numpy.testing import assert_approx_equal


from flamel import main
from alchemtest.gmx import load_benzene

class TestFlamel():
    @staticmethod
    @pytest.fixture(scope='session')
    def setup(tmp_path_factory, session_mocker):
        out = tmp_path_factory.mktemp('out')
        in_path = pathlib.Path(load_benzene().data['Coulomb'][0]).parents[1]
        session_mocker.patch('sys.argv',
                     new=f"flamel -a GROMACS -d {in_path} -f 10 -g -i 50 -j result.csv -m TI,BAR,MBAR -n dE -o {out} -p dhdl -q xvg.bz2 -r 3 -s 50 -t 298 -v -w".split(
                                ' '))
        main()
        return out

    def test_overlap(self, setup):
        assert (setup / 'O_MBAR.pdf').exists()

    def test_dF_t(self, setup):
        assert (setup / 'dF_t.pdf').exists()

    def test_dF_state(self, setup):
        assert (setup / 'dF_state.pdf').exists()

    def test_result_csv(self, setup):
        assert (setup / 'result.csv').exists()

    def test_result_p(self, setup):
        df = pickle.load(open(setup / 'result.p', 'rb'))
        assert_approx_equal(df['MBAR']['Stages']['TOTAL'], 1.8, significant=1)

    def test_dF_state_long(self, setup):
        assert (setup / 'dF_state_long.pdf').exists()

    def test_dhdl_TI(self, setup):
        assert (setup / 'dhdl_TI.pdf').exists()
