# run-length compression

Implement `str_compress(s: str) -> str` in `/workspace/solution.py`.

**Spec:** lossless run-length encode: output char followed by its run count, but if the
compressed string is not shorter, return the original string.


<details>
<summary>Representative test cases — the real (hidden) grader is similar, with additional edge cases</summary>

```python
        assert (str_compress("aabcccccaaa")) == "a2b1c5a3", 'str_compress("aabcccccaaa")'
        assert (str_compress("abc")) == "abc", 'str_compress("abc")'
        assert (str_compress("")) == "", 'str_compress("")'
        assert (str_compress("zz")) == "zz", 'str_compress("zz")'
```
</details>

Only modify /workspace/solution.py. The grader loads it and runs tests like the above.
