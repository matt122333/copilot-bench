import os
def _load():
    ns = {'__file__': '/workspace/solution.py'}
    exec(open('/workspace/solution.py').read(), ns)
    return ns
def test_solution():
    ns = _load()
    str_compress = ns['str_compress']
    assert str_compress("aabcccccaaa") == "a2b1c5a3", 'str_compress("aabcccccaaa")'
    assert str_compress("abc") == "abc", 'str_compress("abc")'
    assert str_compress("") == "", 'str_compress("")'
    assert str_compress("zz") == "zz", 'str_compress("zz")'
