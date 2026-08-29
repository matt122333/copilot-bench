import os
# SOL_PATH overridable for local testing; Harbor mounts solution at /workspace
SOL = os.environ.get('SOL_PATH', '/workspace/solution.py')
def _load():
    ns = {'__file__': SOL}
    exec(open(SOL).read(), ns)
    return ns
def test_solution():
    ns = _load()
    is_palindrome_perm = ns['is_palindrome_perm']
    assert (is_palindrome_perm("Tact Coa")) == True, 'is_palindrome_perm("Tact Coa")'
    assert (is_palindrome_perm("abc")) == False, 'is_palindrome_perm("abc")'
    assert (is_palindrome_perm("aa")) == True, 'is_palindrome_perm("aa")'
    assert (is_palindrome_perm("a")) == True, 'is_palindrome_perm("a")'
if __name__ == '__main__':
    test_solution()
    print('ALL TESTS PASSED')
