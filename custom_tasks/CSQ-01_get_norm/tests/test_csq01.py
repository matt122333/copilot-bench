import sys, runpy

def test_get_norm():
    # load the agent's /workspace/solution.py in an isolated namespace
    ns = {"__file__": "/workspace/solution.py"}
    exec(open("/workspace/solution.py").read(), ns)
    get_norm = ns["get_norm"]

    from math import isclose
    assert isclose(get_norm([3.0, 4.0]), 5.0, rel_tol=1e-6)
    assert get_norm([]) == 0.0
    assert isclose(get_norm([0.0, -3.0, 4.0]), 5.0, rel_tol=1e-6)
    assert get_norm([2.0]) == 2.0
    assert get_norm([1.0, 1.0, 1.0]) == round(3 ** 0.5, 3)
    # negative root-case: must not leak round to wrong precision
    assert get_norm([6.0, 8.0]) == 10.0
