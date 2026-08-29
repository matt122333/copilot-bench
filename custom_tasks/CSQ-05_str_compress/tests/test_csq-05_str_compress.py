import os
# SOL_PATH overridable for local testing; Harbor mounts solution at /workspace
SOL = os.environ.get('SOL_PATH', '/workspace/solution.py')
def _load():
    ns = {'__file__': SOL}
    exec(open(SOL).read(), ns)
    return ns
def test_solution():
    ns = _load()
    str_compress = ns['str_compress']
    assert (str_compress("aabcccccaaa")) == "a2b1c5a3", 'str_compress("aabcccccaaa")'
    assert (str_compress("abc")) == "abc", 'str_compress("abc")'
    assert (str_compress("")) == "", 'str_compress("")'
    assert (str_compress("zz")) == "zz", 'str_compress("zz")'
if __name__ == '__main__':
    test_solution()
    print('ALL TESTS PASSED')
