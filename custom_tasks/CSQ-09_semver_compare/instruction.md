# semantic version compare

Implement `semver_compare(a: str, b: str) -> int` in `/workspace/solution.py`.

**Spec:** compare semantic versions 'major.minor.patch' (ignore pre-release).
Return 1 if a>b, -1 if a<b, 0 if equal.


<details>
<summary>Representative test cases — the real (hidden) grader is similar, with additional edge cases</summary>

```python
        assert (semver_compare("1.2.3", "1.2.3")) == 0, 'semver_compare("1.2.3", "1.2.3")'
        assert (semver_compare("2.0.0", "1.9.9")) == 1, 'semver_compare("2.0.0", "1.9.9")'
        assert (semver_compare("1.0.0", "1.0.1")) == -1, 'semver_compare("1.0.0", "1.0.1")'
        assert (semver_compare("1.10.0", "1.9.0")) == 1, 'semver_compare("1.10.0", "1.9.0")'
```
</details>

Only modify /workspace/solution.py. The grader loads it and runs tests like the above.
