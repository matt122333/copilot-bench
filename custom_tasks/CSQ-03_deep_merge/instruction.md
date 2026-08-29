# Recursive nested-dict merge

Implement `deep_merge(base: dict, override: dict) -> dict` in `/workspace/solution.py`.

**Spec:** return a new dict recursively merging `override` into `base`. Scalars and
lists are replaced by `override`; nested dicts are merged recursively. Do not mutate inputs.


<details>
<summary>Reference tests (run against your /workspace/solution.py)</summary>

```python
        assert deep_merge({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}, 'deep_merge({"a": 1}, {"b": 2})'
        assert deep_merge({"a": {"x": 1}}, {"a": {"y": 2}}) == {"a": {"x": 1, "y": 2}}, 'deep_merge({"a": {"x": 1}}, {"a": {"y": 2}})'
        assert deep_merge({"a": {"x": 1}}, {"a": 5}) == {"a": 5}, 'deep_merge({"a": {"x": 1}}, {"a": 5})'
        assert deep_merge({}, {"k": [1, 2]}) == {"k": [1, 2]}, 'deep_merge({}, {"k": [1, 2]})'
```
</details>

Only modify /workspace/solution.py. The grader loads it and runs tests like the above.
