import os
# SOL_PATH overridable for local testing; Harbor mounts solution at /workspace
SOL = os.environ.get('SOL_PATH', '/workspace/solution.py')
def _load():
    ns = {'__file__': SOL}
    exec(open(SOL).read(), ns)
    return ns
def test_solution():
    ns = _load()
    is_valid_brackets = ns['is_valid_brackets']
    assert (is_valid_brackets("()[]{}")) == True, 'is_valid_brackets("()[]{}")'
    assert (is_valid_brackets("([{}])")) == True, 'is_valid_brackets("([{}])")'
    assert (is_valid_brackets("(]")) == False, 'is_valid_brackets("(]")'
    assert (is_valid_brackets("([)]")) == False, 'is_valid_brackets("([)]")'
    assert (is_valid_brackets("")) == True, 'is_valid_brackets("")'
    assert (is_valid_brackets("{{{{")) == False, 'is_valid_brackets("{{{{")'
if __name__ == '__main__':
    test_solution()
    print('ALL TESTS PASSED')
