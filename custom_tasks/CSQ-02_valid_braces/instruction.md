# Validate bracket nesting

Implement `is_valid_brackets(s: str) -> bool` in `/workspace/solution.py`.

**Spec:** return True iff `s` consists only of `()[]{}` and every open bracket is
closed by a matching bracket of the same type, in correct nesting order.


<details>
<summary>Reference tests (run against your /workspace/solution.py)</summary>

```python
        assert is_valid_brackets("()[]{}") == True, 'is_valid_brackets("()[]{}")'
        assert is_valid_brackets("([{}])") == True, 'is_valid_brackets("([{}])")'
        assert is_valid_brackets("(]") == False, 'is_valid_brackets("(]")'
        assert is_valid_brackets("([)]") == False, 'is_valid_brackets("([)]")'
        assert is_valid_brackets("") == True, 'is_valid_brackets("")'
        assert is_valid_brackets("{{{{") == False, 'is_valid_brackets("{{{{")'
```
</details>

Only modify /workspace/solution.py. The grader loads it and runs tests like the above.
