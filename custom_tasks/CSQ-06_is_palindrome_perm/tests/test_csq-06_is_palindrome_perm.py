import os
def _load():
    ns = {'__file__': '/workspace/solution.py'}
    exec(open('/workspace/solution.py').read(), ns)
    return ns
def test_solution():
    ns = _load()
    is_palindrome_perm = ns['is_palindrome_perm']
    assert is_palindrome_perm("Tact Coa") == True, 'is_palindrome_perm("Tact Coa")'
    assert is_palindrome_perm("abc") == False, 'is_palindrome_perm("abc")'
    assert is_palindrome_perm("aa") == True, 'is_palindrome_perm("aa")'
    assert is_palindrome_perm("a") == True, 'is_palindrome_perm("a")'
