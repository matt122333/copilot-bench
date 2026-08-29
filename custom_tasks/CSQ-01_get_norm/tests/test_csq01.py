import os
def _load():
    SOL = os.environ.get('SOL_PATH', '/workspace/solution.py')
    ns = {'__file__': SOL}
    exec(open(SOL).read(), ns)
    return ns
def test_solution():
    ns = _load()
    get_norm = ns['get_norm']
    from math import isclose
    assert isclose(get_norm([3.0, 4.0]), 5.0, rel_tol=1e-6)
    assert get_norm([]) == 0.0
    assert isclose(get_norm([0.0, -3.0, 4.0]), 5.0, rel_tol=1e-6)
    assert get_norm([2.0]) == 2.0
    assert get_norm([1.0, 1.0, 1.0]) == round(3 ** 0.5, 3)
    assert get_norm([6.0, 8.0]) == 10.0
if __name__ == '__main__':
    test_solution()
    print('ALL TESTS PASSED')