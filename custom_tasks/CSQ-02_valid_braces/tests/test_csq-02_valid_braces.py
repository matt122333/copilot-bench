import os
def _load():
    ns = {'__file__': '/workspace/solution.py'}
    exec(open('/workspace/solution.py').read(), ns)
    return ns
def test_solution():
    ns = _load()
    is_valid_brackets = ns['is_valid_brackets']
    assert is_valid_brackets("()[]{}") == True, 'is_valid_brackets("()[]{}")'
    assert is_valid_brackets("([{}])") == True, 'is_valid_brackets("([{}])")'
    assert is_valid_brackets("(]") == False, 'is_valid_brackets("(]")'
    assert is_valid_brackets("([)]") == False, 'is_valid_brackets("([)]")'
    assert is_valid_brackets("") == True, 'is_valid_brackets("")'
    assert is_valid_brackets("{{{{") == False, 'is_valid_brackets("{{{{")'
