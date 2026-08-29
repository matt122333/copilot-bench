import os
def _load():
    ns = {'__file__': '/workspace/solution.py'}
    exec(open('/workspace/solution.py').read(), ns)
    return ns
def test_solution():
    ns = _load()
    find_dupes = ns['find_dupes']
    assert find_dupes([1,2,2,3,3,3]) == [2, 3] == True, 'find_dupes([1,2,2,3,3,3]) == [2, 3]'
    assert find_dupes([1,2,3]) == [] == True, 'find_dupes([1,2,3]) == []'
    assert find_dupes([5,5,5,1]) == [5] == True, 'find_dupes([5,5,5,1]) == [5]'
