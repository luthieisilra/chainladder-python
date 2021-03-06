import pytest
import numpy as np
import chainladder as cl


@pytest.fixture
def atol():
    return 1e-5


data = ['RAA', 'ABC', 'GenIns', 'MW2008', 'MW2014']


@pytest.mark.parametrize('data', data)
def test_benktander_to_chainladder(data, atol):
    tri = cl.load_sample(data)
    a = cl.Chainladder().fit(tri).ibnr_
    b = cl.Benktander(apriori=.8, n_iters=255).fit(tri, sample_weight=a).ibnr_
    xp = tri.get_array_module()
    assert xp.allclose(xp.nan_to_num(a.values), xp.nan_to_num(b.values), atol=atol)


def test_bf_eq_cl_when_using_cl_apriori():
    cl_ult = cl.Chainladder().fit(cl.load_sample('quarterly')).ultimate_
    cl_ult.rename('development', ['apriori'])
    bf_ult = cl.BornhuetterFerguson().fit(cl.load_sample('quarterly'),
                                          sample_weight=cl_ult).ultimate_
    xp = cl_ult.get_array_module()
    assert xp.allclose(cl_ult.values, bf_ult.values, atol=1e-5)
