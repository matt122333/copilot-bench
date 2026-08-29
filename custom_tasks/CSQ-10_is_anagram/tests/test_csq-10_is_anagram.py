import os
# SOL_PATH overridable for local testing; Harbor mounts solution at /workspace
SOL = os.environ.get('SOL_PATH', '/workspace/solution.py')
def _load():
    ns = {'__file__': SOL}
    exec(open(SOL).read(), ns)
    return ns
def test_solution():
    ns = _load()
    is_anagram = ns['is_anagram']
    assert (is_anagram("anagram", "nagaram")) == True, 'is_anagram("anagram", "nagaram")'
    assert (is_anagram("rat", "car")) == False, 'is_anagram("rat", "car")'
    assert (is_anagram("Hello", "ohell")) == True, 'is_anagram("Hello", "ohell")'
if __name__ == '__main__':
    test_solution()
    print('ALL TESTS PASSED')
