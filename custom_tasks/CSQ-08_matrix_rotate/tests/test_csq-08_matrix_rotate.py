import os
# SOL_PATH overridable for local testing; Harbor mounts solution at /workspace
SOL = os.environ.get('SOL_PATH', '/workspace/solution.py')
def _load():
    ns = {'__file__': SOL}
    exec(open(SOL).read(), ns)
    return ns
def test_solution():
    ns = _load()
    rotate = ns['rotate']
    assert (rotate([[1,2],[3,4]]) == [[3,1],[4,2]]) == True, 'rotate([[1,2],[3,4]]) == [[3,1],[4,2]]'
    assert (rotate([[1,2,3],[4,5,6],[7,8,9]]) == [[7,4,1],[8,5,2],[9,6,3]]) == True, 'rotate([[1,2,3],[4,5,6],[7,8,9]]) == [[7,4,1],[8,5,2],[9,6,3]]'
if __name__ == '__main__':
    test_solution()
    print('ALL TESTS PASSED')
