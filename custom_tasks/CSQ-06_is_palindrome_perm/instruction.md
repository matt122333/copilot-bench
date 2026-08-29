# palindrome permutation

Implement `is_palindrome_perm(s: str) -> bool` in `/workspace/solution.py`.

**Spec:** return True iff some permutation of `s` is a palindrome (after removing
whitespace, ignoring case). A palindrome-perm has at most one char with odd count.


<details>
<summary>Representative test cases — the real (hidden) grader is similar, with additional edge cases</summary>

```python
        assert (is_palindrome_perm("Tact Coa")) == True, 'is_palindrome_perm("Tact Coa")'
        assert (is_palindrome_perm("abc")) == False, 'is_palindrome_perm("abc")'
        assert (is_palindrome_perm("aa")) == True, 'is_palindrome_perm("aa")'
        assert (is_palindrome_perm("a")) == True, 'is_palindrome_perm("a")'
```
</details>

Only modify /workspace/solution.py. The grader loads it and runs tests like the above.
