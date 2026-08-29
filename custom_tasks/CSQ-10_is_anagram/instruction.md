# anagram check

Implement `is_anagram(a: str, b: str) -> bool` in `/workspace/solution.py`.

**Spec:** return True iff a and b contain the same characters with the same counts
(ignore case and whitespace).


<details>
<summary>Representative test cases — the real (hidden) grader is similar, with additional edge cases</summary>

```python
        assert (is_anagram("anagram", "nagaram")) == True, 'is_anagram("anagram", "nagaram")'
        assert (is_anagram("rat", "car")) == False, 'is_anagram("rat", "car")'
        assert (is_anagram("Hello", "ohell")) == True, 'is_anagram("Hello", "ohell")'
```
</details>

Only modify /workspace/solution.py. The grader loads it and runs tests like the above.
