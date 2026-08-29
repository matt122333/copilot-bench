import os
def _load():
    ns = {'__file__': '/workspace/solution.py'}
    exec(open('/workspace/solution.py').read(), ns)
    return ns
def test_solution():
    ns = _load()
    deep_merge = ns['deep_merge']
    assert deep_merge({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}, 'deep_merge({"a": 1}, {"b": 2})'
    assert deep_merge({"a": {"x": 1}}, {"a": {"y": 2}}) == {"a": {"x": 1, "y": 2}}, 'deep_merge({"a": {"x": 1}}, {"a": {"y": 2}})'
    assert deep_merge({"a": {"x": 1}}, {"a": 5}) == {"a": 5}, 'deep_merge({"a": {"x": 1}}, {"a": 5})'
    assert deep_merge({}, {"k": [1, 2]}) == {"k": [1, 2]}, 'deep_merge({}, {"k": [1, 2]})'
