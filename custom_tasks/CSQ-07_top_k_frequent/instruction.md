# top-k frequent elements

Implement `top_k_frequent(items: list, k: int) -> list` in `/workspace/solution.py`.

**Spec:** return the `k` most frequent distinct elements, most frequent first. Ties
broken by first occurrence order.


<details>
<summary>Representative test cases — the real (hidden) grader is similar, with additional edge cases</summary>

```python
        assert (top_k_frequent([1,1,1,2,2,3], 2) == [1, 2]) == True, 'top_k_frequent([1,1,1,2,2,3], 2) == [1, 2]'
        assert (top_k_frequent([1,1,1,2,2,3], 1) == [1]) == True, 'top_k_frequent([1,1,1,2,2,3], 1) == [1]'
        assert (top_k_frequent([1], 1) == [1]) == True, 'top_k_frequent([1], 1) == [1]'
```
</details>

Only modify /workspace/solution.py. The grader loads it and runs tests like the above.
