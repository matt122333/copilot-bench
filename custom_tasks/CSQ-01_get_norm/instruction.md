# Implement `get_norm`

Implement the function `get_norm` in `/workspace/solution.py` so that the provided
test file (below) passes.

**Specification:**
`get_norm(values: list[int | float]) -> float` returns the Euclidean (L2) norm of the list:
`sqrt(sum(x_i ** 2))`. Returns `0.0` for an empty list. Round the result to **3 decimal places**.

You may edit only `/workspace/solution.py`. Do not modify the test file.

<details>
<summary>Representative test cases — the real (hidden) grader is similar, with additional edge cases</summary>

```python
from math import isclose
from solution import get_norm

assert isclose(get_norm([3.0, 4.0]), 5.0, rel_tol=1e-6)
assert isclose(get_norm([]), 0.0)
assert isclose(get_norm([0.0, -3.0, 4.0]), 5.0, rel_tol=1e-6)
assert isclose(get_norm([2.0]), 2.0)
assert get_norm([1.0, 1.0, 1.0]) == round(3**0.5, 3)
print("ALL TESTS PASSED")
```
</details>