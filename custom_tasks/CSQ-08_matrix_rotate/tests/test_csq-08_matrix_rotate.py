import os
def _load():
    ns = {'__file__': '/workspace/solution.py'}
    exec(open('/workspace/solution.py').read(), ns)
    return ns
def test_solution():
    ns = _load()
    rotate = ns['rotate']
    assert rotate([[1,2],[3,4]]) == [[3,1],[4,2]] == True, 'rotate([[1,2],[3,4]]) == [[3,1],[4,2]]'
    assert rotate([[1,2,3],[4,5,6],[7,8,9]]) == [[7,4,1],[8,5,2],[9,6,3]] == True, 'rotate([[1,2,3],[4,5,6],[7,8,9]]) == [[7,4,1],[8,5,2],[9,6,3]]'
