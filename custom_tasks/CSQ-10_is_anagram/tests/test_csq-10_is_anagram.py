import os
def _load():
    ns = {'__file__': '/workspace/solution.py'}
    exec(open('/workspace/solution.py').read(), ns)
    return ns
def test_solution():
    ns = _load()
    is_anagram = ns['is_anagram']
    assert is_anagram("anagram", "nagaram") == True, 'is_anagram("anagram", "nagaram")'
    assert is_anagram("rat", "car") == False, 'is_anagram("rat", "car")'
    assert is_anagram("Hello", "ohell") == True, 'is_anagram("Hello", "ohell")'
