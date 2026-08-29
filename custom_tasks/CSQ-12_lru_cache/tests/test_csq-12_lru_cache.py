import os
def _load():
    ns = {'__file__': '/workspace/solution.py'}
    exec(open('/workspace/solution.py').read(), ns)
    return ns
def test_solution():
    ns = _load()
    lru = ns['lru']
    assert lru(2, [("put",1,1),("put",2,2),("get",1),("put",3,3),("get",2),("get",3)]) == [1, -1, 3] == True, 'lru(2, [("put",1,1),("put",2,2),("get",1),("put",3,3),("get",2),("get",3)]) == [1, -1, 3]'
    assert lru(1, [("put",1,1),("put",2,2),("get",1),("get",2)]) == [-1, 2] == True, 'lru(1, [("put",1,1),("put",2,2),("get",1),("get",2)]) == [-1, 2]'
