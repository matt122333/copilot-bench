import os
# SOL_PATH overridable for local testing; Harbor mounts solution at /workspace
SOL = os.environ.get('SOL_PATH', '/workspace/solution.py')
def _load():
    ns = {'__file__': SOL}
    exec(open(SOL).read(), ns)
    return ns
def test_solution():
    ns = _load()
    top_k_frequent = ns['top_k_frequent']
    assert (top_k_frequent([1,1,1,2,2,3], 2) == [1, 2]) == True, 'top_k_frequent([1,1,1,2,2,3], 2) == [1, 2]'
    assert (top_k_frequent([1,1,1,2,2,3], 1) == [1]) == True, 'top_k_frequent([1,1,1,2,2,3], 1) == [1]'
    assert (top_k_frequent([1], 1) == [1]) == True, 'top_k_frequent([1], 1) == [1]'
if __name__ == '__main__':
    test_solution()
    print('ALL TESTS PASSED')
