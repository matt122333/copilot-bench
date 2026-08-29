import os
def _load():
    ns = {'__file__': '/workspace/solution.py'}
    exec(open('/workspace/solution.py').read(), ns)
    return ns
def test_solution():
    ns = _load()
    top_k_frequent = ns['top_k_frequent']
    assert top_k_frequent([1,1,1,2,2,3], 2) == [1, 2] == True, 'top_k_frequent([1,1,1,2,2,3], 2) == [1, 2]'
    assert top_k_frequent([1,1,1,2,2,3], 1) == [1] == True, 'top_k_frequent([1,1,1,2,2,3], 1) == [1]'
    assert top_k_frequent([1], 1) == [1] == True, 'top_k_frequent([1], 1) == [1]'
