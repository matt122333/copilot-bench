import os
# SOL_PATH overridable for local testing; Harbor mounts solution at /workspace
SOL = os.environ.get('SOL_PATH', '/workspace/solution.py')
def _load():
    ns = {'__file__': SOL}
    exec(open(SOL).read(), ns)
    return ns
def test_solution():
    ns = _load()
    lru = ns['lru']
    assert (lru(2, [("put",1,1),("put",2,2),("get",1),("put",3,3),("get",2),("get",3)]) == [1, -1, 3]) == True, 'lru(2, [("put",1,1),("put",2,2),("get",1),("put",3,3),("get",2),("get",3)]) == [1, -1, 3]'
    assert (lru(1, [("put",1,1),("put",2,2),("get",1),("get",2)]) == [-1, 2]) == True, 'lru(1, [("put",1,1),("put",2,2),("get",1),("get",2)]) == [-1, 2]'
if __name__ == '__main__':
    test_solution()
    print('ALL TESTS PASSED')
